from pydantic import BaseModel
from typing import Optional

class Character(BaseModel):
    name: str
    appearance: str
    action: str

class Dialogue(BaseModel):
    speaker: str
    text: str
    bubble_type: str  # speech | thought | narration

class Scene(BaseModel):
    scene_number: int
    panel_caption: str
    setting: str
    characters: list[Character]
    dialogue: list[Dialogue]
    mood: str
    image_prompt: str

class ChapterRequest(BaseModel):
    chapter_text: str
    style: str = "western_comic"  # western_comic | manga | noir

class JobStatus(BaseModel):
    job_id: str
    status: str           # pending | processing | done | failed
    progress: int         # 0-100
    result_url: Optional[str] = None
    scenes: Optional[list] = None
    error: Optional[str] = None