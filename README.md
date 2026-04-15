
```
██████╗  ██████╗  ██████╗ ██╗  ██╗    ██████╗     ██████╗ ██████╗ ███╗   ███╗██╗ ██████╗
██╔══██╗██╔═══██╗██╔═══██╗██║ ██╔╝    ╚════██╗   ██╔════╝██╔═══██╗████╗ ████║██║██╔════╝
██████╔╝██║   ██║██║   ██║█████╔╝      █████╔╝   ██║     ██║   ██║██╔████╔██║██║██║
██╔══██╗██║   ██║██║   ██║██╔═██╗     ██╔═══╝    ██║     ██║   ██║██║╚██╔╝██║██║██║
██████╔╝╚██████╔╝╚██████╔╝██║  ██╗    ███████╗   ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║╚██████╗
╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝    ╚══════╝    ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝ ╚═════╝
```

<div align="center">

### ✦ *Feed it a book. Get back an anime comic.* ✦

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?style=for-the-badge&logo=fastapi)
![HuggingFace](https://img.shields.io/badge/🤗_Animagine_XL_3.1-SDXL-orange?style=for-the-badge)
![GROQ](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-red?style=for-the-badge)
![SLURM](https://img.shields.io/badge/HPC-SLURM_GPU-purple?style=for-the-badge)

</div>

---

## ┌─────────────────────────────────────────┐
## │  CHAPTER 1 — THE ORIGIN STORY           │
## └─────────────────────────────────────────┘

> 💬 *"What if every book you read... could come alive as an anime?"*

**Book2Comic** is an AI pipeline that takes any book chapter as input and transforms it into a **manga-style anime comic** — complete with illustrated panels, speech bubbles, and caption bars.

You give it text. It gives you **art**.

No drawing skills required. No artists harmed. Just pure AI sorcery. ⚡

---

## ┌─────────────────────────────────────────┐
## │  CHAPTER 2 — THE PIPELINE (aka THE ARC) │
## └─────────────────────────────────────────┘

```
 ╔══════════════════════════════════════════════════════════════════════╗
 ║                                                                      ║
 ║   [ YOUR BOOK CHAPTER ]                                              ║
 ║         │                                                            ║
 ║         │  "A long time ago in a land..."                            ║
 ║         ▼                                                            ║
 ║  ┌─────────────────┐   POW!    LLaMA 3.3 70B via Groq               ║
 ║  │  SCENE          │ ━━━━━━━►  Reads the chapter like a director     ║
 ║  │  EXTRACTOR      │          Extracts 4-6 key dramatic scenes       ║
 ║  └────────┬────────┘          Characters · Dialogue · Mood · Setting ║
 ║           │                                                          ║
 ║           │  scene JSON                                              ║
 ║           ▼                                                          ║
 ║  ┌─────────────────┐   ZAP!   Animagine XL 3.1 + IP-Adapter         ║
 ║  │  IMAGE          │ ━━━━━━━►  Anime-tuned SDXL generates each panel ║
 ║  │  GENERATOR      │          IP-Adapter keeps characters consistent ║
 ║  └────────┬────────┘          Running on A100 GPU (Northeastern HPC) ║
 ║           │                                                          ║
 ║           │  panel images                                            ║
 ║           ▼                                                          ║
 ║  ┌─────────────────┐   BAM!   Pillow                                 ║
 ║  │  PANEL          │ ━━━━━━━►  Stitches panels into comic grid       ║
 ║  │  ASSEMBLER      │          Adds speech bubbles + caption bars     ║
 ║  └────────┬────────┘          Exports as final PNG                   ║
 ║           │                                                          ║
 ║           ▼                                                          ║
 ║     [ YOUR ANIME COMIC ]  🎌                                         ║
 ║                                                                      ║
 ╚══════════════════════════════════════════════════════════════════════╝
```

---

## ┌─────────────────────────────────────────┐
## │  CHAPTER 3 — THE SPECIAL POWERS         │
## └─────────────────────────────────────────┘

### ⚡ Character Consistency via IP-Adapter

> 💬 *"Wait... Naruto looks different in every panel!"*
> 💬 *"Not anymore."*

The #1 problem in AI comic generation is characters looking different each panel. We solve this with **IP-Adapter**:

```
Panel 1 → Naruto appears for the first time
           └─► Generated freely, saved as Naruto's visual reference 📸

Panel 3 → Naruto appears again
           └─► IP-Adapter injects reference into generation
               Same face. Same style. New pose. ✅

Panel 5 → Sasuke appears for the first time
           └─► Generated freely, saved as Sasuke's visual reference 📸
```

Each character gets their own reference on first appearance. Every subsequent panel featuring them is **conditioned** on that reference — same face, new scene.

---

### 🎨 Three Comic Styles

| Style | Vibe | Best For |
|-------|------|----------|
| `manga` | Black & white, screentones, bold ink | Shounen action, drama |
| `anime` | Vibrant colors, cel shading, key visual | Fantasy, adventure |
| `noir` | High contrast, deep shadows, hatching | Mystery, thriller |

---

### 🤖 Models Under the Hood

| Stage | Model | Why This One |
|-------|-------|-------------|
| Scene Extraction | **LLaMA 3.3 70B** (Groq) | Best open-source LLM for structured JSON |
| Image Generation | **Animagine XL 3.1** | Anime-tuned SDXL — miles better than plain SDXL for anime |
| Character Lock | **IP-Adapter SDXL** | Injects visual reference without retraining |
| Panel Assembly | **Pillow** | Battle-tested image processing |

---

## ┌─────────────────────────────────────────┐
## │  CHAPTER 4 — THE ORIGIN (SETUP)         │
## └─────────────────────────────────────────┘

### Prerequisites

```bash
# You need:
# ✅ Python 3.10+
# ✅ GROQ API Key  →  https://console.groq.com
# ✅ GPU (8GB+ VRAM) or HPC access
```

### 1. Clone the Repo

```bash
git clone https://github.com/Aayush99000/book-reading-to-storytelling
cd book-reading-to-storytelling
```

### 2. Set Up Environment

```bash
# On HPC (Northeastern Explorer)
sbatch setup_hpc.sh

# Local (with conda)
conda create -n book2comic python=3.10
conda activate book2comic
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# backend/.env
GROQ_API_KEY=your_groq_api_key_here
MANGA_LORA_ID=                        # optional: HuggingFace manga LoRA repo
HF_HOME=/scratch/$USER/hf_cache       # HuggingFace model cache path
```

---

## ┌─────────────────────────────────────────┐
## │  CHAPTER 5 — UNLEASH THE POWER (USAGE)  │
## └─────────────────────────────────────────┘

### Run Locally

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Run on HPC (SLURM)

```bash
sbatch slurm_job.sh
# Monitor: squeue -u $USER
# Logs:    tail -f logs/book2comic_<jobid>.out
```

### Generate Your Comic

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "chapter_text": "It was a dark and stormy night...",
    "style": "manga"
  }'

# Returns job_id → poll for status
curl http://localhost:8000/status/<job_id>

# When done → grab your comic
curl http://localhost:8000/output/comic_<job_id>.png --output my_comic.png
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/generate` | Submit a chapter for comic generation |
| `GET` | `/status/{job_id}` | Poll job progress (0–100%) |
| `GET` | `/output/{file}` | Download the finished comic PNG |

---

## ┌─────────────────────────────────────────┐
## │  CHAPTER 6 — THE TEAM (PROJECT STRUCTURE│
## └─────────────────────────────────────────┘

```
book-to-storytelling/
│
├── backend/
│   ├── main.py              ← FastAPI server + job orchestration
│   ├── models.py            ← Pydantic data models
│   ├── scene_extractor.py   ← LLM scene parsing + prompt building
│   ├── image_generator.py   ← Diffusers pipeline + IP-Adapter
│   └── panel_assembler.py   ← Pillow comic layout engine
│
├── slurm_job.sh             ← HPC GPU job submission
├── setup_hpc.sh             ← One-shot HPC environment setup
└── requirements.txt         ← Python dependencies
```

---

## ┌─────────────────────────────────────────┐
## │         ...TO BE CONTINUED              │
## └─────────────────────────────────────────┘

<div align="center">

```
  ╔══════════════════════════════════════════╗
  ║                                          ║
  ║   What started as text on a page...      ║
  ║                                          ║
  ║        ...becomes a world.               ║
  ║                                          ║
  ╚══════════════════════════════════════════╝
```

*Built with 🍜 and way too much GPU time.*

**[⭐ Star this repo](https://github.com/Aayush99000/book-reading-to-storytelling)** if you want to see more arcs!

</div>
