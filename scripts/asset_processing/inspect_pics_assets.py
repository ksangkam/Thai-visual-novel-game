"""Audit the user-supplied Phase 2.5 images and write visual contact sheets.

Install Pillow from requirements.txt. The script is read-only for pics/ and
public/assets/; review sheets and a JSON inventory go under tmp/pics_review/.
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
PICS = ROOT / "pics" / "assets"
OUT = ROOT / "tmp" / "pics_review"
CHARACTERS = {
    "phlai_ngam": ["normal", "happy", "sad", "surprised", "worried"],
    "wantong": ["normal", "happy", "sad", "worried", "crying"],
    "khunchang": ["normal", "angry", "suspicious", "surprised", "smirk"],
    "khunphaen": ["normal", "confident", "serious", "angry", "surprised"],
    "thongprasi": ["normal", "happy", "surprised", "sad"],
    "khrua_nak": ["normal", "happy", "serious"],
    "hongphrai": ["normal", "mysterious", "alert"],
}
BACKGROUNDS = ["bg_main_menu", *(f"bg_scene{i:02d}" for i in range(1, 9))]
CGS = [f"cg_scene{i:02d}" for i in (1, 3, 5, 8)]


def describe(path: Path) -> dict:
    with Image.open(path) as im:
        im.load()
        result = {
            "file": path.relative_to(ROOT).as_posix(),
            "format": im.format,
            "mode": im.mode,
            "width": im.width,
            "height": im.height,
            "bytes": path.stat().st_size,
        }
        if "A" in im.getbands():
            alpha = im.getchannel("A")
            result["alpha_extrema"] = list(alpha.getextrema())
            result["alpha_bbox"] = list(alpha.getbbox()) if alpha.getbbox() else None
        else:
            result["alpha_extrema"] = None
            result["alpha_bbox"] = None
        return result


def make_sheet(entries: list[tuple[str, Path]], out_path: Path, *, cols: int,
               cell: tuple[int, int], transparent: bool = False) -> None:
    cw, ch = cell
    rows = (len(entries) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cw, rows * ch), "#eee8dc")
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 15)
    except OSError:
        font = ImageFont.load_default()
    for index, (label, path) in enumerate(entries):
        x, y = (index % cols) * cw, (index // cols) * ch
        thumb_w, thumb_h = cw - 16, ch - 44
        if transparent:
            tile = Image.new("RGB", (thumb_w, thumb_h), "#f7f3ea")
            td = ImageDraw.Draw(tile)
            step = 16
            for yy in range(0, thumb_h, step):
                for xx in range(0, thumb_w, step):
                    if (xx // step + yy // step) % 2:
                        td.rectangle((xx, yy, xx + step, yy + step), fill="#ddd8d0")
            with Image.open(path) as im:
                im.thumbnail((thumb_w - 10, thumb_h - 10), Image.Resampling.LANCZOS)
                rgba = im.convert("RGBA")
                tile.paste(rgba, ((thumb_w - rgba.width) // 2, (thumb_h - rgba.height) // 2), rgba)
            sheet.paste(tile, (x + 8, y + 4))
        else:
            with Image.open(path) as im:
                im = im.convert("RGB")
                im.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
                sheet.paste(im, (x + 8 + (thumb_w - im.width) // 2,
                                 y + 4 + (thumb_h - im.height) // 2))
        draw.text((x + 8, y + ch - 32), label, fill="#201815", font=font)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out_path, "PNG", optimize=True)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    inventory: list[dict] = []
    design_entries = []
    sprite_entries = []
    missing = []
    unexpected_sprites = []

    for character, expressions in CHARACTERS.items():
        folder = PICS / "characters" / character
        sheet = folder / "design_sheet.jpg"
        if sheet.is_file():
            design_entries.append((f"{character} design", sheet))
            inventory.append({**describe(sheet), "asset": f"{character}/design_sheet"})
        else:
            missing.append(sheet.relative_to(ROOT).as_posix())
        actual_sprite_names = set()
        for expression in expressions:
            canonical = folder / f"{character}_{expression}.png"
            alternates = [canonical]
            if character == "khunchang":
                alternates.append(folder / f"khunchan_{expression}.png")
            if character == "wantong":
                alternates.append(folder / f"wantong_ {expression}.png")
            found = next((p for p in alternates if p.is_file()), None)
            if found is None:
                missing.append(canonical.relative_to(ROOT).as_posix())
                continue
            actual_sprite_names.add(found.name)
            inventory.append({**describe(found), "asset": f"{character}/{expression}"})
            sprite_entries.append((f"{character} — {expression}", found))
        for candidate in folder.glob("*.png"):
            if candidate.name != "design_sheet.png" and candidate.name not in actual_sprite_names:
                unexpected_sprites.append(candidate.relative_to(ROOT).as_posix())

    background_entries = []
    cg_entries = []
    for asset in BACKGROUNDS:
        folder = PICS / "backgrounds" / ("main_menu" if asset == "bg_main_menu" else "scenes")
        files = [folder / f"{asset}.webp", folder / f"{asset}.jpg", folder / f"{asset}.png"]
        found = next((p for p in files if p.is_file()), None)
        if found is None:
            missing.append((folder / f"{asset}.webp").relative_to(ROOT).as_posix())
        else:
            background_entries.append((asset, found))
            inventory.append({**describe(found), "asset": asset})
    for asset in CGS:
        folder = PICS / "backgrounds" / "cg"
        files = [folder / f"{asset}.webp", folder / f"{asset}.jpg", folder / f"{asset}.png"]
        found = next((p for p in files if p.is_file()), None)
        if found is None:
            missing.append((folder / f"{asset}.webp").relative_to(ROOT).as_posix())
        else:
            cg_entries.append((asset, found))
            inventory.append({**describe(found), "asset": asset})

    make_sheet(design_entries, OUT / "character_design_sheets.png", cols=4, cell=(360, 430))
    make_sheet(sprite_entries, OUT / "character_sprites.png", cols=5, cell=(300, 340), transparent=True)
    make_sheet(background_entries, OUT / "backgrounds.png", cols=3, cell=(520, 330))
    make_sheet(cg_entries, OUT / "event_cg.png", cols=2, cell=(680, 425))
    report = {
        "source": "pics/assets",
        "expected_sprites": sum(map(len, CHARACTERS.values())),
        "found_design_sheets": len(design_entries),
        "found_sprites": len(sprite_entries),
        "found_backgrounds": len(background_entries),
        "found_event_cg": len(cg_entries),
        "missing": missing,
        "unexpected_sprites": unexpected_sprites,
        "images": inventory,
        "review_sheets": [
            p.relative_to(ROOT).as_posix()
            for p in OUT.glob("*.png")
        ],
    }
    (OUT / "inspection.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("found_design_sheets", "found_sprites",
                                             "expected_sprites", "found_backgrounds",
                                             "found_event_cg", "missing", "unexpected_sprites",
                                             "review_sheets")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
