"""
Run this first before starting the server.
Confirms Groq API key works and scene extraction is functioning.

Usage:
    cd backend
    python test_groq.py
"""

import os, json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

key = os.environ.get("GROQ_API_KEY")
if not key:
    print("❌ GROQ_API_KEY not found in .env — please add it first")
    exit(1)

print(f"✅ GROQ_API_KEY found: {key[:8]}...")

client = Groq(api_key=key)

SAMPLE_CHAPTER = """
The old lighthouse keeper, Silas, climbed the spiral staircase with a lantern in hand.
A storm was rolling in fast from the east, waves crashing against the rocks below.
At the top, he found a young girl huddled by the glass, soaking wet and shivering.
'Who are you?' he asked, setting down the lantern.
She looked up with wide silver eyes. 'I came from the sea,' she whispered.
Silas stepped back, heart hammering. The lantern flickered violently in the wind.
"""

print("\n📤 Sending test chapter to Groq (llama-3.1-8b-instant)...")

try:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a comic book storyboard artist. "
                    "Extract 3 key scenes from the chapter. "
                    "Return ONLY a valid JSON object with a 'scenes' array. "
                    "Each scene needs: scene_number, panel_caption, setting, mood, image_prompt."
                )
            },
            {
                "role": "user",
                "content": f"Extract scenes from:\n\n{SAMPLE_CHAPTER}"
            }
        ],
        temperature=0.4,
        max_tokens=1024,
        response_format={"type": "json_object"}
    )

    raw = response.choices[0].message.content
    data = json.loads(raw)
    scenes = data.get("scenes", [])

    print(f"\n✅ Groq responded successfully!")
    print(f"✅ Extracted {len(scenes)} scenes\n")

    for s in scenes:
        print(f"  Scene {s.get('scene_number')}: {s.get('panel_caption')}")
        print(f"  Mood   : {s.get('mood')}")
        print(f"  Prompt : {s.get('image_prompt', '')[:80]}...")
        print()

    print("🎉 Groq is working correctly — you're ready to start the server!\n")
    print("Next step: uvicorn main:app --reload --port 8000")

except Exception as e:
    print(f"\n❌ Groq test failed: {e}")
    print("Check your GROQ_API_KEY in .env and try again.")