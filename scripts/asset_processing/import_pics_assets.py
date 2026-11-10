"""Import reviewed Phase 2.5 images from pics/assets into public/assets.

Source files in pics/ are never modified. Transparent sprites are downsampled
from 5800x7200 to 1450x1800 RGBA PNGs; opaque scene art becomes quality-90
WebP. The scene06 background is intentionally excluded because it contains
people, but is retained for the user's approved Phase 3 prototype.

Install Pillow from scripts/asset_processing/requirements.txt before running.
"""
from __future__ import annotations

import json
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "pics" / "assets"
PUBLIC = ROOT / "public" / "assets"
PREVIEW_SIZE = (1450, 1800)
CHARACTERS = {
    "phlai_ngam": ["normal", "happy", "sad", "surprised", "worried"],
    "wantong": ["normal", "happy", "sad", "worried", "crying"],
    "khunchang": ["normal", "angry", "suspicious", "surprised", "smirk"],
    "khunphaen": ["normal", "confident", "serious", "angry", "surprised"],
    "thongprasi": ["normal", "happy", "surprised", "sad"],
    "khrua_nak": ["normal", "happy", "serious"],
    "hongphrai": ["normal", "mysterious", "alert"],
}
BACKGROUND_IDS = ["bg_main_menu", *(f"bg_scene{i:02d}" for i in range(1, 9))]
CG_IDS = [f"cg_scene{i:02d}" for i in (1, 3, 5, 8)]
UI_IDS = {
    "dialogue_box_frame": "dialogue-box-frame.svg",
    "name_plate": "name-plate.svg",
    "choice_panel_frame": "choice-panel-frame.svg",
    "vocabulary_icon": "vocabulary-icon.svg",
    "next_dialogue_icon": "next-dialogue-icon.svg",
    "menu_decoration": "menu-decoration.svg",
    "chapter_transition_decoration": "chapter-transition-decoration.svg",
}
CONSISTENCY_REVIEW: list[dict] = []


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def first_existing(paths: list[Path]) -> Path | None:
    return next((path for path in paths if path.is_file()), None)


def sprite_source(character: str, expression: str) -> Path:
    folder = SOURCE / "characters" / character
    candidates = [folder / f"{character}_{expression}.png"]
    if character == "khunchang":
        candidates.append(folder / f"khunchan_{expression}.png")
    if character == "wantong":
        candidates.append(folder / f"wantong_ {expression}.png")
    found = first_existing(candidates)
    if not found:
        raise FileNotFoundError(f"Missing sprite: {character}/{expression}")
    return found


def background_source(asset_id: str, folder: Path) -> Path:
    found = first_existing([folder / f"{asset_id}.{ext}" for ext in ("webp", "jpg", "png")])
    if not found:
        raise FileNotFoundError(f"Missing background: {asset_id}")
    return found


def save_webp(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as image:
        if image.size != (2752, 1536):
            raise ValueError(f"Expected 2752x1536 for {source}, found {image.size}")
        image = image.convert("RGB")
        image.save(destination, "WEBP", quality=90, method=6)


def main() -> None:
    PUBLIC.mkdir(parents=True, exist_ok=True)
    char_manifest: dict[str, dict] = {}
    imported = []

    # Replace the old tiny Canva preview with the new sheet, retaining the preview.
    for character, expressions in CHARACTERS.items():
        folder = SOURCE / "characters" / character
        source_sheet = folder / "design_sheet.jpg"
        if not source_sheet.is_file():
            raise FileNotFoundError(source_sheet)
        output_dir = PUBLIC / "characters" / character
        output_dir.mkdir(parents=True, exist_ok=True)
        old_sheet = output_dir / "design_sheet.png"
        preview = output_dir / "design_sheet_preview.png"
        if old_sheet.is_file() and not preview.exists():
            with Image.open(old_sheet) as old_image:
                if old_image.size == (149, 199):
                    shutil.copy2(old_sheet, preview)
        design_sheet = output_dir / "design_sheet.png"
        with Image.open(source_sheet) as image:
            image.convert("RGB").save(design_sheet, "PNG", optimize=True, compress_level=9)
            sheet_size = image.size
        imported.append(design_sheet)

        sprite_paths: dict[str, str] = {}
        for expression in expressions:
            source_sprite = sprite_source(character, expression)
            destination = output_dir / f"{character}_{expression}.png"
            with Image.open(source_sprite) as image:
                rgba = image.convert("RGBA")
                alpha = rgba.getchannel("A")
                extrema = alpha.getextrema()
                if extrema[0] != 0 or extrema[1] != 255:
                    raise ValueError(f"Sprite is not transparently cut out: {source_sprite} alpha={extrema}")
                rgba = rgba.resize(PREVIEW_SIZE, Image.Resampling.LANCZOS)
                rgba.save(destination, "PNG", optimize=True, compress_level=9)
            imported.append(destination)
            sprite_paths[expression] = f"assets/characters/{character}/{destination.name}"

        char_manifest[character] = {
            "designSheet": f"assets/characters/{character}/design_sheet.png",
            "width": sheet_size[0],
            "height": sheet_size[1],
            "bytes": design_sheet.stat().st_size,
            "status": "integrated_reference_sheet",
            "previousPreview": f"assets/characters/{character}/design_sheet_preview.png" if preview.exists() else None,
            "expressionSprites": sprite_paths,
        }

    backgrounds: dict[str, str] = {}
    menu_source = background_source("bg_main_menu", SOURCE / "backgrounds" / "main_menu")
    menu_dest = PUBLIC / "backgrounds" / "main_menu" / "bg_main_menu.webp"
    save_webp(menu_source, menu_dest)
    imported.append(menu_dest)
    backgrounds["bg_main_menu"] = "assets/backgrounds/main_menu/bg_main_menu.webp"

    missing_backgrounds = []
    for scene_no in range(1, 9):
        asset_id = f"bg_scene{scene_no:02d}"
        source = background_source(asset_id, SOURCE / "backgrounds" / "scenes")
        destination = PUBLIC / "backgrounds" / "scenes" / f"{asset_id}.webp"
        save_webp(source, destination)
        imported.append(destination)
        backgrounds[asset_id] = f"assets/backgrounds/scenes/{destination.name}"

    event_cg: dict[str, str] = {}
    for asset_id in CG_IDS:
        source = background_source(asset_id, SOURCE / "backgrounds" / "cg")
        destination = PUBLIC / "backgrounds" / "cg" / f"{asset_id}.webp"
        save_webp(source, destination)
        imported.append(destination)
        event_cg[asset_id] = f"assets/backgrounds/cg/{destination.name}"

    ui_manifest: dict[str, str] = {}
    for ui_id, filename in UI_IDS.items():
        source = SOURCE / "ui" / filename
        ET.parse(source)  # Fail before import if malformed XML/SVG.
        destination = PUBLIC / "ui" / filename
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        imported.append(destination)
        ui_manifest[ui_id] = f"assets/ui/{filename}"

    # Update project manifests only after all images have been written successfully.
    asset_manifest_path = PUBLIC / "manifest" / "asset_manifest.json"
    asset_manifest_path.parent.mkdir(parents=True, exist_ok=True)
    asset_manifest = {
        "schemaVersion": 1,
        "status": "complete" if not missing_backgrounds else "partial",
        "backgrounds": backgrounds,
        "eventCG": event_cg,
        "characters": char_manifest,
        "ui": ui_manifest,
        "reviewRequired": missing_backgrounds,
        "consistencyReview": CONSISTENCY_REVIEW,
    }
    write_json(asset_manifest_path, asset_manifest)
    write_json(PUBLIC / "manifest" / "character_manifest.json", {
        "schemaVersion": 1,
        "characters": char_manifest,
    })

    data_characters_path = ROOT / "data" / "characters.json"
    data_characters = read_json(data_characters_path)
    for character in data_characters["characters"]:
        cid = character["characterId"]
        character["designSheetPath"] = char_manifest[cid]["designSheet"]
        character["spriteAssets"] = char_manifest[cid]["expressionSprites"]
    write_json(data_characters_path, data_characters)

    data_scenes_path = ROOT / "data" / "scenes.json"
    data_scenes = read_json(data_scenes_path)
    cgs_needing_review = {item["asset"] for item in CONSISTENCY_REVIEW}
    for scene in data_scenes["scenes"]:
        scene_no = int(scene["sceneId"][-2:])
        bg_id = f"bg_scene{scene_no:02d}"
        if bg_id in backgrounds:
            scene["backgroundPath"] = backgrounds[bg_id]
        else:
            scene.pop("backgroundPath", None)
        cg_id = f"cg_scene{scene_no:02d}"
        if cg_id in event_cg and cg_id not in cgs_needing_review:
            scene["eventCG"] = cg_id
        else:
            scene.pop("eventCG", None)
    write_json(data_scenes_path, data_scenes)

    print(json.dumps({
        "imported_files": len(imported),
        "character_design_sheets": len(char_manifest),
        "character_sprites": sum(len(c["expressionSprites"]) for c in char_manifest.values()),
        "registered_backgrounds": len(backgrounds),
        "registered_event_cg": len(event_cg),
        "registered_ui": len(ui_manifest),
        "review_required": missing_backgrounds,
        "consistency_review": CONSISTENCY_REVIEW,
        "preserved_sources": "pics/assets",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
