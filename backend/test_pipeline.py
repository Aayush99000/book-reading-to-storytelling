"""
Standalone pipeline test — runs end-to-end without the FastAPI server.
Saves the finished comic to output/test_comic.png
"""

import asyncio, os, sys

# Make sure we can import from backend/
sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

from scene_extractor import extract_scenes
from image_generator import generate_all_images, reset_character_store
from panel_assembler import assemble_comic

SAMPLE_CHAPTER = """
The morning mist hung low over the Hidden Leaf Village as Naruto Uzumaki burst through
the academy doors, his orange jacket catching the early light. He was late again.

Iruka-sensei stood at the front of the class, arms crossed, his scar creasing as he
frowned. "Naruto. You're twenty minutes late," he said firmly.

Naruto scratched the back of his head and grinned, his whisker marks stretching with
his smile. "Sorry, sensei! I was training by the lake. I think I almost got it —
the Shadow Clone Jutsu!"

A sharp laugh cut through the class. Sasuke Uchiha sat at the back row, arms folded,
dark eyes cold. "Almost doesn't count, dead last," he said without looking up.

Naruto's grin vanished. He clenched his fists and locked eyes with Sasuke across
the room. The air between them crackled with rivalry. One day, he swore to himself.
One day I'll surpass you.

Iruka sighed and gestured to an empty seat. "Enough. Sit down, Naruto. Today we
practice chakra control — and everyone will be tested before sundown."
"""

async def main():
    os.makedirs("output", exist_ok=True)
    os.makedirs("output/images", exist_ok=True)

    print("\n" + "="*60)
    print("  BOOK2COMIC — PIPELINE TEST")
    print("="*60)

    # Stage 1 — Scene extraction
    print("\n[Stage 1] Extracting scenes via Groq...")
    scenes = extract_scenes(SAMPLE_CHAPTER)
    print(f"  Extracted {len(scenes)} scenes:")
    for s in scenes:
        chars = [c["name"] for c in s["characters"]]
        print(f"  Scene {s['scene_number']}: {s['panel_caption']} | chars: {chars}")

    # Stage 2 — Image generation
    print(f"\n[Stage 2] Generating {len(scenes)} panel images via Animagine XL + IP-Adapter...")
    print("  (First run downloads models — this may take a few minutes)")
    reset_character_store()
    image_paths = await generate_all_images(scenes, style="manga")
    print(f"  Generated images: {image_paths}")

    # Stage 3 — Panel assembly
    print("\n[Stage 3] Assembling comic panels...")
    output_path = "output/test_comic.png"
    assemble_comic(scenes, image_paths, output_path)
    print(f"  Comic saved to: {output_path}")

    print("\n" + "="*60)
    print("  DONE! Comic saved to output/test_comic.png")
    print("="*60 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
