from PIL import Image, ImageDraw, ImageFont
import requests, io, math, os, textwrap

PANEL_W      = 400
PANEL_H      = 300
BORDER       = 6
GAP          = 14
COLS         = 2
BG_COLOR     = (255, 255, 255)
BORDER_COLOR = (15, 15, 15)
CAPTION_BG   = (255, 255, 180)
FONT_PATH    = "assets/Bangers-Regular.ttf"   # comic font — download from Google Fonts
FONT_SMALL   = 13
FONT_BUBBLE  = 14


def get_font(size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except OSError:
        return ImageFont.load_default()


def load_image_from_url(url: str) -> Image.Image:
    resp = requests.get(url, timeout=20)
    img  = Image.open(io.BytesIO(resp.content)).convert("RGB")
    return img.resize((PANEL_W, PANEL_H), Image.LANCZOS)


def draw_caption_bar(draw: ImageDraw, text: str):
    """Yellow narrator bar at the top of each panel."""
    font = get_font(FONT_SMALL)
    draw.rectangle([0, 0, PANEL_W, 26], fill=CAPTION_BG)
    draw.text((8, 5), text[:55], fill=BORDER_COLOR, font=font)


def draw_speech_bubble(draw: ImageDraw, text: str, x: int, y: int,
                        bubble_type: str, max_width: int = 160):
    """Draw a speech or thought bubble with wrapped text."""
    font    = get_font(FONT_BUBBLE)
    wrapped = textwrap.fill(text, width=18)
    lines   = wrapped.split("\n")
    lh      = 18
    pad     = 10
    bw      = max_width
    bh      = len(lines) * lh + pad * 2

    # clamp bubble inside panel
    bx = min(x, PANEL_W - bw - 4)
    by = min(y, PANEL_H - bh - 4)

    if bubble_type == "thought":
        draw.ellipse([bx, by, bx + bw, by + bh],
                     fill=(255, 255, 255), outline=BORDER_COLOR, width=2)
    else:
        draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=10,
                                fill=(255, 255, 255), outline=BORDER_COLOR, width=2)

    for i, line in enumerate(lines):
        draw.text((bx + pad, by + pad + i * lh), line,
                  fill=BORDER_COLOR, font=font)


def create_panel(scene: dict, image_url: str) -> Image.Image:
    panel = load_image_from_url(image_url)
    draw  = ImageDraw.Draw(panel)

    # caption bar
    caption = scene.get("panel_caption", "")
    if caption:
        draw_caption_bar(draw, caption)

    # speech bubbles — max 2 per panel to avoid clutter
    y_offset = 35
    for dlg in scene.get("dialogue", [])[:2]:
        speaker  = dlg.get("speaker", "")
        text     = dlg.get("text", "")
        btype    = dlg.get("bubble_type", "speech")
        label    = f"{speaker}: {text}" if speaker else text
        draw_speech_bubble(draw, label, x=10, y=y_offset, bubble_type=btype)
        y_offset += 80

    # panel border
    draw.rectangle([0, 0, PANEL_W - 1, PANEL_H - 1],
                   outline=BORDER_COLOR, width=BORDER)
    return panel


def assemble_comic(scenes: list[dict], image_urls: list[str],
                   output_path: str = "output/comic.png") -> str:
    panels   = [create_panel(s, url) for s, url in zip(scenes, image_urls)]
    rows     = math.ceil(len(panels) / COLS)
    canvas_w = COLS * PANEL_W + (COLS + 1) * GAP
    canvas_h = rows * PANEL_H + (rows + 1) * GAP
    canvas   = Image.new("RGB", (canvas_w, canvas_h), BG_COLOR)

    for i, panel in enumerate(panels):
        row, col = divmod(i, COLS)
        x = GAP + col * (PANEL_W + GAP)
        y = GAP + row * (PANEL_H + GAP)
        canvas.paste(panel, (x, y))

    os.makedirs("output", exist_ok=True)
    canvas.save(output_path, quality=95)
    return output_path