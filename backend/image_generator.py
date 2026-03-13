import os, asyncio
import os
from dotenv import load_dotenv
load_dotenv()

# SDXL model — reliable comic-style output
MODEL = "stability-ai/sdxl:39ed52f2319f9c5cdaefd5e7d8020d8f10f8b7e0b5e9a2d7a6b2b0e7b5c1a4f"

NEGATIVE_PROMPT = (
    "realistic, photographic, 3d render, blurry, dark background, watermark, "
    "signature, text, extra limbs, deformed face, ugly, low quality, grainy"
)


async def generate_image(prompt: str) -> str:
    """Run Replicate image generation in a thread (it's a sync SDK)."""
    loop = asyncio.get_event_loop()

    output = await loop.run_in_executor(
        None,
        lambda: replicate.run(
            MODEL,
            input={
                "prompt": prompt,
                "negative_prompt": NEGATIVE_PROMPT,
                "width": 768,
                "height": 512,
                "num_inference_steps": 30,
                "guidance_scale": 7.5,
                "scheduler": "K_EULER",
            }
        )
    )

    return output[0] if isinstance(output, list) else str(output)


async def generate_all_images(prompts: list[str]) -> list[str]:
    """Generate all panel images in parallel."""
    return await asyncio.gather(*[generate_image(p) for p in prompts])