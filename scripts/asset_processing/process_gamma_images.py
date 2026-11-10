"""Convert preserved Gamma JPEG originals to optimized, opaque WebP game assets.

Install Pillow from requirements.txt, then run this script from any directory.
Source images remain untouched under output/imagegen/.
"""
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
ASSETS = {
    "bg_main_menu.jpg": "public/assets/backgrounds/main_menu/bg_main_menu.webp",
    "bg_scene01.jpg": "public/assets/backgrounds/scenes/bg_scene01.webp",
    "bg_scene02.jpg": "public/assets/backgrounds/scenes/bg_scene02.webp",
    "cg_scene05.jpg": "public/assets/backgrounds/cg/cg_scene05.webp",
}


def main() -> None:
    source_dir = ROOT / "output" / "imagegen"
    for source_name, output_name in ASSETS.items():
        source = source_dir / source_name
        output = ROOT / output_name
        if not source.is_file():
            raise FileNotFoundError(source)
        output.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(source) as image:
            if image.size != (2752, 1536):
                raise ValueError(f"Unexpected image dimensions for {source}: {image.size}")
            image.convert("RGB").save(output, "WEBP", quality=90, method=6)
        print(f"{output.relative_to(ROOT)} — {output.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
