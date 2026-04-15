import uuid, asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from models import ChapterRequest, JobStatus
from scene_extractor import extract_scenes
from image_generator import generate_all_images, reset_character_store
from panel_assembler import assemble_comic

app = FastAPI(title="Book2Comic API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://your-frontend.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# serve finished comics as static files
app.mount("/output", StaticFiles(directory="output"), name="output")

# in-memory job store (fine for hackathon)
jobs: dict[str, dict] = {}


@app.get("/")
def root():
    return {"message": "Book2Comic API is running"}


@app.post("/generate", response_model=JobStatus)
async def generate(req: ChapterRequest):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "status": "pending",
        "progress": 0,
        "result_url": None,
        "scenes": None,
        "error": None,
    }
    asyncio.create_task(run_pipeline(job_id, req.chapter_text, req.style))
    return JobStatus(job_id=job_id, status="pending", progress=0)


@app.get("/status/{job_id}", response_model=JobStatus)
def get_status(job_id: str):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobStatus(job_id=job_id, **job)


async def run_pipeline(job_id: str, chapter_text: str, style: str):
    try:
        # ── Stage 1: scene extraction via Groq ───────────────────────────
        jobs[job_id].update({"status": "processing", "progress": 10})
        scenes = extract_scenes(chapter_text)
        jobs[job_id].update({"scenes": scenes, "progress": 30})

        # ── Stage 2: image generation via diffusers + IP-Adapter ────────
        reset_character_store()          # clear refs from any previous job
        jobs[job_id]["progress"] = 40
        image_urls = await generate_all_images(scenes, style)
        jobs[job_id]["progress"] = 80

        # ── Stage 3: panel assembly via Pillow ───────────────────────────
        output_path = f"output/comic_{job_id[:8]}.png"
        assemble_comic(scenes, image_urls, output_path)
        jobs[job_id].update({
            "status": "done",
            "progress": 100,
            "result_url": f"/output/comic_{job_id[:8]}.png",
        })

    except Exception as e:
        jobs[job_id].update({"status": "failed", "progress": 0, "error": str(e)})
        print(f"[Pipeline error] {job_id}: {e}")