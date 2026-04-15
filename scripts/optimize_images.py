"""Convert source PNG illustrations to web-optimized WebP.

Source: ../illustrations/CS_Scene*.png
Output: ../images/scene_01.webp ... scene_10.webp
Target: 1600px max width, quality 82.
"""
import re
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT.parent / "illustrations"
DST = ROOT / "images"
DST.mkdir(parents=True, exist_ok=True)

MAX_W = 1600
QUALITY = 82

def scene_number(p: Path) -> int:
    m = re.search(r"(\d+)", p.stem)
    return int(m.group(1)) if m else 0

files = sorted(SRC.glob("CS_Scene*.png"), key=scene_number)
print(f"Found {len(files)} source images")

for src in files:
    n = scene_number(src)
    out = DST / f"scene_{n:02d}.webp"
    img = Image.open(src)
    if img.width > MAX_W:
        ratio = MAX_W / img.width
        new_size = (MAX_W, int(img.height * ratio))
        img = img.resize(new_size, Image.LANCZOS)
    img.save(out, "WEBP", quality=QUALITY, method=6)
    src_mb = src.stat().st_size / 1_000_000
    out_kb = out.stat().st_size / 1_000
    print(f"  {src.name} ({src_mb:.1f} MB) -> {out.name} ({out_kb:.0f} KB, {img.width}x{img.height})")

total_out = sum(p.stat().st_size for p in DST.glob("*.webp")) / 1_000_000
print(f"\nTotal output: {total_out:.2f} MB across {len(list(DST.glob('*.webp')))} files")
