import time
import io
import requests
import streamlit as st
from PIL import Image

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Book2Comic",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0f0f0f; }

    /* Title */
    h1 {
        font-family: 'Georgia', serif;
        font-size: 3rem !important;
        color: #FFD700 !important;
        text-shadow: 3px 3px 0px #000, -1px -1px 0px #000;
        letter-spacing: 2px;
    }

    /* Subheader */
    .subtitle {
        color: #aaa;
        font-size: 1.1rem;
        margin-top: -10px;
        margin-bottom: 20px;
        font-style: italic;
    }

    /* Panel cards for scenes */
    .scene-card {
        background: #1a1a1a;
        border: 2px solid #FFD700;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
        color: #eee;
        font-size: 0.85rem;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #1a1a1a;
        border-right: 2px solid #FFD700;
    }
    section[data-testid="stSidebar"] * { color: #eee !important; }

    /* Buttons */
    .stButton > button {
        background-color: #FFD700 !important;
        color: #000 !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 4px !important;
        font-size: 1rem !important;
    }
    .stButton > button:hover { background-color: #FFC200 !important; }

    /* Text area */
    textarea {
        background-color: #1a1a1a !important;
        color: #eee !important;
        border: 1px solid #444 !important;
        border-radius: 6px !important;
        font-family: 'Georgia', serif !important;
    }

    /* Progress bar */
    .stProgress > div > div { background-color: #FFD700 !important; }

    /* Stage badges */
    .stage-badge {
        display: inline-block;
        background: #FFD700;
        color: #000;
        font-weight: bold;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        margin-right: 6px;
    }

    /* Download button */
    .stDownloadButton > button {
        background-color: #222 !important;
        color: #FFD700 !important;
        border: 2px solid #FFD700 !important;
        font-weight: bold !important;
    }

    /* Divider color */
    hr { border-color: #333 !important; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    backend_url = st.text_input(
        "Backend URL",
        value="http://localhost:8000",
        help="URL of the running FastAPI server (local or HPC via ngrok)",
    )
    st.markdown("---")
    st.markdown("## 🎨 Style Guide")
    st.markdown("""
| Style | Vibe |
|-------|------|
| `manga` | B&W, screentones, shounen |
| `anime` | Vibrant color, cel-shading |
| `noir` | High contrast, deep shadows |
    """)
    st.markdown("---")
    st.markdown("## 🔧 Pipeline")
    st.markdown("""
1. **Scene Extractor**
   LLaMA 3.3 70B via Groq
   → characters, mood, dialogue

2. **Image Generator**
   Animagine XL 3.1 + IP-Adapter
   → consistent anime panels

3. **Panel Assembler**
   Pillow layout engine
   → speech bubbles + captions
    """)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("# 📖 Book2Comic")
st.markdown('<p class="subtitle">Feed it a book chapter. Get back an anime comic.</p>',
            unsafe_allow_html=True)
st.markdown("---")

# ── Input section ─────────────────────────────────────────────────────────────
col_input, col_options = st.columns([3, 1])

with col_input:
    chapter_text = st.text_area(
        "Paste your book chapter",
        height=280,
        placeholder=(
            "The morning mist hung low over the village as the hero burst through\n"
            "the gates, sword in hand...\n\n"
            "(Paste any book chapter — 200 to 2000 words works best)"
        ),
    )

with col_options:
    style = st.selectbox(
        "Comic Style",
        options=["manga", "anime", "noir"],
        index=0,
    )
    st.markdown("<br>", unsafe_allow_html=True)
    generate_btn = st.button("⚡ Generate Comic", use_container_width=True)

# ── Validation ────────────────────────────────────────────────────────────────
if generate_btn:
    if not chapter_text.strip():
        st.warning("Please paste a book chapter first.")
        st.stop()

    if len(chapter_text.split()) < 30:
        st.warning("Chapter is very short — try pasting at least a few paragraphs for better results.")

    # ── Submit job ────────────────────────────────────────────────────────────
    st.markdown("---")
    try:
        with st.spinner("Connecting to backend..."):
            resp = requests.post(
                f"{backend_url}/generate",
                json={"chapter_text": chapter_text, "style": style},
                timeout=15,
            )
            resp.raise_for_status()
            job = resp.json()
            job_id = job["job_id"]
    except requests.exceptions.ConnectionError:
        st.error(f"Cannot reach backend at `{backend_url}`. Is the FastAPI server running?")
        st.stop()
    except Exception as e:
        st.error(f"Failed to submit job: {e}")
        st.stop()

    st.success(f"Job submitted — ID: `{job_id}`")

    # ── Progress tracking ─────────────────────────────────────────────────────
    progress_bar  = st.progress(0)
    status_text   = st.empty()
    scenes_holder = st.empty()

    STAGE_LABELS = {
        range(0,  30): ("🧠", "Stage 1 — Extracting scenes via LLaMA 3.3 70B..."),
        range(30, 80): ("🎨", "Stage 2 — Generating anime panels via Animagine XL..."),
        range(80, 100):("🖼️", "Stage 3 — Assembling comic panels..."),
    }

    def stage_label(progress: int) -> str:
        for r, (icon, label) in STAGE_LABELS.items():
            if progress in r:
                return f"{icon} {label}"
        return "✅ Finishing up..."

    while True:
        try:
            status_resp = requests.get(f"{backend_url}/status/{job_id}", timeout=10)
            status      = status_resp.json()
        except Exception:
            status_text.warning("Lost connection — retrying...")
            time.sleep(3)
            continue

        pct = status.get("progress", 0)
        progress_bar.progress(pct / 100)
        status_text.info(stage_label(pct))

        # Show extracted scenes as soon as they arrive
        if status.get("scenes") and pct >= 30:
            with scenes_holder.container():
                st.markdown("#### 📋 Extracted Scenes")
                for s in status["scenes"]:
                    chars = ", ".join(c["name"] for c in s.get("characters", []))
                    mood  = s.get("mood", "")
                    caption = s.get("panel_caption", "")
                    st.markdown(
                        f'<div class="scene-card">'
                        f'<b>Scene {s["scene_number"]}</b> — {caption}<br>'
                        f'<small>👤 {chars} &nbsp;|&nbsp; 🎭 {mood}</small>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

        if status["status"] == "done":
            progress_bar.progress(1.0)
            status_text.success("✅ Comic generated!")
            break

        if status["status"] == "failed":
            status_text.error(f"❌ Pipeline failed: {status.get('error', 'unknown error')}")
            st.stop()

        time.sleep(3)

    # ── Display comic ─────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## 🎌 Your Anime Comic")

    comic_url = f"{backend_url}{status['result_url']}"
    try:
        comic_bytes = requests.get(comic_url, timeout=30).content
        comic_image = Image.open(io.BytesIO(comic_bytes))
    except Exception as e:
        st.error(f"Could not fetch comic image: {e}")
        st.stop()

    st.image(comic_image, use_container_width=True)

    st.download_button(
        label="⬇️ Download Comic PNG",
        data=comic_bytes,
        file_name=f"book2comic_{job_id[:8]}.png",
        mime="image/png",
        use_container_width=True,
    )

    st.markdown("---")
    st.caption("Built with Animagine XL 3.1 · LLaMA 3.3 70B · IP-Adapter · Pillow")

# ── Empty state ───────────────────────────────────────────────────────────────
else:
    st.markdown("""
<div style="text-align:center; padding: 60px 0; color: #555;">
    <div style="font-size: 5rem;">📖</div>
    <div style="font-size: 1.2rem; margin-top: 12px;">
        Paste a chapter above and hit <b style="color:#FFD700">Generate Comic</b>
    </div>
    <div style="font-size: 0.9rem; margin-top: 8px;">
        Works with any book genre — fantasy, thriller, romance, sci-fi
    </div>
</div>
""", unsafe_allow_html=True)
