
import os, json
from groq import Groq
from dotenv import load_dotenv
from models import Scene

load_dotenv()  # ← this loads your .env file

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Swap to "llama-3.1-70b-versatile" on demo day for best quality
MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """
You are a comic book storyboard artist. Given a book chapter, extract 4 to 6 key scenes.
Return ONLY a valid JSON object with a "scenes" array. No explanation, no preamble.

Each scene must follow this exact structure:
{
  "scene_number": 1,
  "panel_caption": "Short narrator caption (max 10 words)",
  "setting": "Detailed visual description of location and time of day",
  "characters": [
    {
      "name": "Character name",
      "appearance": "Hair color, clothing, expression, body language",
      "action": "What they are physically doing in this panel"
    }
  ],
  "dialogue": [
    {
      "speaker": "Character name",
      "text": "What they say (max 15 words)",
      "bubble_type": "speech"
    }
  ],
  "mood": "tense | joyful | mysterious | dark | hopeful",
  "image_prompt": "comic book panel, flat colors, bold ink outlines, [setting], [characters + action]"
}

Rules:
- bubble_type must be: speech, thought, or narration
- Return ONLY the JSON object, nothing else
- If no dialogue in a scene, set dialogue to []
- Keep character appearance identical across ALL scenes for visual consistency
"""

def extract_scenes(chapter_text: str) -> list[dict]:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Extract comic scenes from:\n\n{chapter_text}"}
        ],
        temperature=0.4,
        max_tokens=2048,
        response_format={"type": "json_object"}
    )

    raw = response.choices[0].message.content
    data = json.loads(raw)

    # handle {"scenes": [...]} or {"panels": [...]} or direct list
    if isinstance(data, dict):
        scenes_raw = data.get("scenes") or data.get("panels") or list(data.values())[0]
    else:
        scenes_raw = data

    # validate with Pydantic
    return [Scene(**s).model_dump() for s in scenes_raw]


def build_image_prompt(scene: dict, style: str = "western_comic") -> str:
    style_prefixes = {
        "western_comic": "comic book panel, flat colors, bold ink outlines, vibrant palette, clean linework, DC/Marvel style",
        "manga":         "manga panel, black and white, screen tones, clean linework, expressive faces, shounen style",
        "noir":          "noir comic panel, high contrast, deep shadows, limited palette, 1940s detective style",
    }
    prefix = style_prefixes.get(style, style_prefixes["western_comic"])
    mood   = scene.get("mood", "neutral")
    base   = scene.get("image_prompt", "")
    return f"{prefix}, {mood} atmosphere, {base}, no text, no watermark, no speech bubbles"