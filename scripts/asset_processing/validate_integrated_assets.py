"""Validate the integrated Phase 2.5 assets and their JSON references."""
from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    manifest = load(PUBLIC / "assets/manifest/asset_manifest.json")
    characters = load(ROOT / "data/characters.json")["characters"]
    scenes = load(ROOT / "data/scenes.json")["scenes"]
    failures: list[str] = []
    image_count = 0
    total_bytes = 0

    def check_file(relative: str, expected_format: str | None = None,
                   expected_size: tuple[int, int] | None = None,
                   alpha: bool = False) -> None:
        nonlocal image_count, total_bytes
        path = PUBLIC / relative
        if not path.is_file():
            failures.append(f"missing: {relative}")
            return
        total_bytes += path.stat().st_size
        image_count += 1
        try:
            with Image.open(path) as im:
                im.verify()
            with Image.open(path) as im:
                if expected_format and im.format != expected_format:
                    failures.append(f"format: {relative} ({im.format}, expected {expected_format})")
                if expected_size and im.size != expected_size:
                    failures.append(f"dimensions: {relative} ({im.size}, expected {expected_size})")
                if alpha:
                    if im.mode != "RGBA":
                        failures.append(f"alpha mode: {relative} ({im.mode})")
                    else:
                        lo, hi = im.getchannel("A").getextrema()
                        if lo != 0 or hi != 255:
                            failures.append(f"alpha range: {relative} ({lo}, {hi})")
        except Exception as exc:  # image decoder diagnostics
            failures.append(f"unreadable: {relative} ({exc})")

    backgrounds = manifest["backgrounds"]
    for asset_id, relative in backgrounds.items():
        check_file(relative, "WEBP", (2752, 1536))
    for relative in manifest["eventCG"].values():
        check_file(relative, "WEBP", (2752, 1536))

    for character_id, entry in manifest["characters"].items():
        check_file(entry["designSheet"], "PNG", (928, 1152))
        for relative in entry["expressionSprites"].values():
            check_file(relative, "PNG", (1450, 1800), alpha=True)
        data_character = next((c for c in characters if c["characterId"] == character_id), None)
        if data_character is None:
            failures.append(f"character not found in data/characters.json: {character_id}")
        elif data_character["spriteAssets"] != entry["expressionSprites"]:
            failures.append(f"sprite map mismatch: {character_id}")

    for relative in manifest["ui"].values():
        path = PUBLIC / relative
        if not path.is_file():
            failures.append(f"missing UI: {relative}")
        else:
            try:
                ET.parse(path)
            except ET.ParseError as exc:
                failures.append(f"invalid SVG: {relative} ({exc})")

    for scene in scenes:
        if scene.get("backgroundPath"):
            relative = scene["backgroundPath"]
            if not (PUBLIC / relative).is_file():
                failures.append(f"scene path missing: {scene['sceneId']} {relative}")
        if scene.get("eventCG") and scene["eventCG"] not in manifest["eventCG"]:
            failures.append(f"event CG not registered: {scene['sceneId']} {scene['eventCG']}")
        if scene.get("eventCG") and scene["eventCG"] in {
            item["asset"] for item in manifest.get("consistencyReview", [])
        }:
            failures.append(f"unapproved event CG active in scene: {scene['sceneId']} {scene['eventCG']}")

    result = {
        "status": "passed" if not failures else "failed",
        "image_files_checked": image_count,
        "total_integrated_image_bytes": total_bytes,
        "backgrounds_registered": len(backgrounds),
        "event_cg_registered": len(manifest["eventCG"]),
        "character_design_sheets": len(manifest["characters"]),
        "character_sprites": sum(len(c["expressionSprites"]) for c in manifest["characters"].values()),
        "ui_svgs": len(manifest["ui"]),
        "review_required": manifest.get("reviewRequired", []),
        "consistency_review": manifest.get("consistencyReview", []),
        "failures": failures,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
