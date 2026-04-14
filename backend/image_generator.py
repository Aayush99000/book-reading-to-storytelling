import os, asyncio, uuid
import torch
from diffusers import StableDiffusionXLPipeline
from dotenv import load_dotenv

load_dotenv()

# Animagine XL 3.1 — anime-tuned SDXL checkpoint on HuggingFace
MODEL_ID = "cagliostrolab/animagine-xl-3.1"

# Optional: manga panel style LoRA (SDXL-compatible HuggingFace repo ID)
# Example: "Linaqruf/manga-pencil-xl"
# Leave empty to run Animagine without LoRA
MANGA_LORA_ID = os.getenv("MANGA_LORA_ID", "")
LORA_SCALE    = 0.75

# Animagine XL quality booster tags
QUALITY_TAGS = "masterpiece, best quality, very aesthetic, absurdres"

NEGATIVE_PROMPT = (
    "nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, "
    "extra digit, fewer digits, cropped, worst quality, low quality, "
    "normal quality, jpeg artifacts, signature, watermark, username, "
    "blurry, artist name, 3d render, realistic, photographic"
)

# Singleton pipeline — loaded once, reused for all generations
_pipe = None


def _load_pipeline() -> StableDiffusionXLPipeline:
    global _pipe
    if _pipe is not None:
        return _pipe

    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype  = torch.float16 if device == "cuda" else torch.float32

    print(f"[image_generator] Loading Animagine XL 3.1 on {device} ({dtype})...")

    _pipe = StableDiffusionXLPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=dtype,
        use_safetensors=True,
    ).to(device)

    if MANGA_LORA_ID:
        print(f"[image_generator] Loading manga LoRA: {MANGA_LORA_ID}")
        _pipe.load_lora_weights(MANGA_LORA_ID)
        _pipe.fuse_lora(lora_scale=LORA_SCALE)

    # Memory optimisations for GPU
    if device == "cuda":
        _pipe.enable_attention_slicing()

    print("[image_generator] Pipeline ready.")
    return _pipe


def _generate_sync(prompt: str) -> str:
    """Synchronous generation — runs in a thread pool."""
    pipe = _load_pipeline()

    result = pipe(
        prompt=f"{QUALITY_TAGS}, {prompt}",
        negative_prompt=NEGATIVE_PROMPT,
        width=768,
        height=512,
        num_inference_steps=30,
        guidance_scale=7.0,
    )

    os.makedirs("output/images", exist_ok=True)
    img_path = f"output/images/{uuid.uuid4().hex[:8]}.png"
    result.images[0].save(img_path)
    return img_path


async def generate_image(prompt: str) -> str:
    """Async wrapper — offloads blocking diffusers call to thread pool."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _generate_sync, prompt)


async def generate_all_images(prompts: list[str]) -> list[str]:
    """Generate panels sequentially — single GPU handles one at a time."""
    results = []
    for prompt in prompts:
        results.append(await generate_image(prompt))
    return results
