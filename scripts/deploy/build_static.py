"""Assemble a lean, host-agnostic static deployment in dist/."""
from __future__ import annotations

import json
import os
import shutil
import stat
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / "dist"
DATA_FILES = ("scenes.json", "characters.json", "choices.json", "vocabulary.json", "quiz.json")


def remove_readonly(func, path: str, _exc_info) -> None:
    """Allow Windows/OneDrive to remove read-only generated output files."""
    os.chmod(path, stat.S_IREAD | stat.S_IWRITE)
    func(path)


def main() -> None:
    if DIST.exists():
        resolved_root = ROOT.resolve()
        resolved_dist = DIST.resolve()
        if resolved_dist.parent != resolved_root or resolved_dist.name != "dist":
            raise RuntimeError(f"Refusing to replace unexpected output path: {resolved_dist}")
        shutil.rmtree(resolved_dist, onerror=remove_readonly)

    (DIST / "src/styles").mkdir(parents=True)
    (DIST / "data").mkdir()
    shutil.copy2(ROOT / "index.html", DIST / "index.html")
    shutil.copy2(ROOT / "src/app.js", DIST / "src/app.js")
    shutil.copy2(ROOT / "src/styles/phase3.css", DIST / "src/styles/phase3.css")
    for filename in DATA_FILES:
        source = ROOT / "data" / filename
        json.loads(source.read_text(encoding="utf-8"))
        shutil.copy2(source, DIST / "data" / filename)
    shutil.copytree(
        ROOT / "public/assets",
        DIST / "public/assets",
        ignore=shutil.ignore_patterns("desktop.ini", "README.md"),
    )

    required = [
        DIST / "index.html",
        DIST / "src/app.js",
        DIST / "src/styles/phase3.css",
        *(DIST / "data" / name for name in DATA_FILES),
        DIST / "public/assets/manifest/asset_manifest.json",
    ]
    missing = [str(path.relative_to(DIST)) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"Deployment output is missing: {missing}")

    print(json.dumps({
        "status": "ready",
        "output": str(DIST),
        "data_files": len(DATA_FILES),
        "asset_files": sum(path.is_file() for path in (DIST / "public/assets").rglob("*")),
        "size_bytes": sum(path.stat().st_size for path in DIST.rglob("*") if path.is_file()),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
