import os, asyncio, uuid
import torch
from PIL import Image
from diffusers import StableDiffusionXLPipeline
from dotenv import load_dotenv

from scene_extractor import build_image_prompt

load_dotenv()

# ── Model config ──────────────────────────────────────────────────────────────
MODEL_ID       = "cagliostrolab/animagine-xl-3.1"
IP_ADAPTER_REPO    = "h94/IP-Adapter"
IP_ADAPTER_SUBFOLDER = "sdxl_models"
IP_ADAPTER_WEIGHT  = "ip-adapter_sdxl.bin"

# How strongly the reference image influences the output (0.0 = off, 1.0 = max)
# 0.6 keeps the character recognisable while still following the scene prompt
IP_ADAPTER_SCALE = 0.6

MANGA_LORA_ID = os.getenv("MANGA_LORA_ID", "")
LORA_SCALE    = 0.75

QUALITY_TAGS = "masterpiece, best quality, very aesthetic, absurdres"
NEGATIVE_PROMPT = (
    "nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, "
    "extra digit, fewer digits, cropped, worst quality, low quality, "
    "normal quality, jpeg artifacts, signature, watermark, username, "
    "blurry, artist name, 3d render, realistic, photographic"
)


# ── Character reference store ─────────────────────────────────────────────────

class CharacterReferenceStore:
    """
    Stores the first generated panel for each character as their visual reference.
    IP-Adapter uses this reference to keep the character consistent across panels.
    """

    def __init__(self):
        self._refs: dict[str, Image.Image] = {}

    def has(self, name: str) -> bool:
        return name.lower() in self._refs

    def get(self, name: str) -> Image.Image:
        return self._refs[name.lower()]

    def set(self, name: str, image: Image.Image):
        self._refs[name.lower()] = image

    def get_first_available(self, names: list[str]) -> Image.Image | None:
        """Return the reference image for the first character in the list that has one."""
        for name in names:
            if self.has(name):
                return self.get(name)
        return None

    def reset(self):
        self._refs.clear()


# Module-level singletons — loaded once, reused across all panels in a job
_pipe: StableDiffusionXLPipeline | None = None
_character_store = CharacterReferenceStore()


# ── Pipeline loader ───────────────────────────────────────────────────────────

def _load_pipeline() -> StableDiffusionXLPipeline:
    global _pipe
    if _pipe is not None:
        return _pipe

    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype  = torch.float16 if device == "cuda" else torch.float32
    print(f"[image_generator] Device: {device} | dtype: {dtype}", flush=True)
    print(f"[image_generator] Step 1/4 — from_pretrained Animagine XL 3.1...", flush=True)

    _pipe = StableDiffusionXLPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=dtype,
        use_safetensors=True,
    )
    print(f"[image_generator] Step 2/4 — moving pipeline to {device}...", flush=True)
    _pipe = _pipe.to(device)
    print(f"[image_generator] Step 2/4 — done.", flush=True)

    # Optional manga style LoRA
    if MANGA_LORA_ID:
        print(f"[image_generator] Loading manga LoRA: {MANGA_LORA_ID}", flush=True)
        _pipe.load_lora_weights(MANGA_LORA_ID)
        _pipe.fuse_lora(lora_scale=LORA_SCALE)

    # IP-Adapter for character consistency
    print("[image_generator] Step 3/4 — loading IP-Adapter (SDXL)...", flush=True)
    _pipe.load_ip_adapter(
        IP_ADAPTER_REPO,
        subfolder=IP_ADAPTER_SUBFOLDER,
        weight_name=IP_ADAPTER_WEIGHT,
    )
    print("[image_generator] Step 3/4 — done.", flush=True)

    # NOTE: do NOT call enable_attention_slicing() — it replaces IP-Adapter's
    # attention processors with SlicedAttnProcessor, which can't handle the tuple
    # encoder_hidden_states that IP-Adapter produces, causing an AttributeError.
    # The L40S has 46 GB VRAM, so slicing isn't needed anyway.

    # SDXL VAE is numerically unstable in fp16 and produces corrupted outputs.
    # Setting force_upcast=True makes the pipeline cast both the VAE weights
    # AND the latents to fp32 right before decode, then restore fp16 after.
    # This is safer than manually calling vae.to(float32) which mismatches dtypes.
    if device == "cuda":
        _pipe.vae.config.force_upcast = True
        print("[image_generator] VAE force_upcast=True for stable fp32 decode.", flush=True)

    print("[image_generator] Step 4/4 — Pipeline ready.", flush=True)
    return _pipe


# ── Core generation ───────────────────────────────────────────────────────────

def _generate_sync(prompt: str, character_names: list[str]) -> str:
    pipe = _load_pipeline()
    full_prompt = f"{QUALITY_TAGS}, {prompt}"

    reference = _character_store.get_first_available(character_names)
    device    = "cuda" if torch.cuda.is_available() else "cpu"

    if reference is not None:
        pipe.set_ip_adapter_scale(IP_ADAPTER_SCALE)
        ip_image = reference
        print(f"[image_generator] Using reference for: {character_names}", flush=True)
    else:
        pipe.set_ip_adapter_scale(0.0)
        ip_image = Image.new("RGB", (224, 224), color=(128, 128, 128))
        print(f"[image_generator] First appearance, generating freely: {character_names}", flush=True)

    # Pass image directly — IPAdapterAttnProcessor2_0 (set by load_ip_adapter) handles
    # the tuple encoder_hidden_states correctly, so pre-encoding is not needed.
    result = pipe(
        prompt=full_prompt,
        negative_prompt=NEGATIVE_PROMPT,
        ip_adapter_image=ip_image,
        width=768,
        height=512,
        num_inference_steps=30,
        guidance_scale=7.0,
    )

    generated_image = result.images[0]

    # Register first-seen characters using this panel as their reference
    for name in character_names:
        if not _character_store.has(name):
            _character_store.set(name, generated_image)
            print(f"[image_generator] Registered reference for: {name}")

    os.makedirs("output/images", exist_ok=True)
    img_path = f"output/images/{uuid.uuid4().hex[:8]}.png"
    generated_image.save(img_path)
    return img_path


# ── Public API ────────────────────────────────────────────────────────────────

def reset_character_store():
    """Call at the start of each new chapter/job to clear character references."""
    _character_store.reset()
    print("[image_generator] Character reference store cleared.")


async def generate_image(prompt: str, character_names: list[str]) -> str:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _generate_sync, prompt, character_names)


async def generate_all_images(scenes: list[dict], style: str = "manga") -> list[str]:
    """
    Generate one panel image per scene, maintaining character consistency
    across panels via IP-Adapter reference injection.
    """
    results = []
    for scene in scenes:
        prompt          = build_image_prompt(scene, style)
        character_names = [c["name"] for c in scene.get("characters", [])]
        results.append(await generate_image(prompt, character_names))
    return results
