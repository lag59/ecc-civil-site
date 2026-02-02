#!/usr/bin/env python3
"""
generate_images.py

Renames specified image files to safer names, generates resized PNG/JPEG/WebP variants,
and places them under the same IMAGES folder.

Requirements:
  pip install pillow

Usage (Windows PowerShell):
  python .\scripts\generate_images.py

This script will:
- Rename files mapped in `RENAME_MAP` (if the source exists)
- Generate resized versions for sizes in `SIZES` (widths)
- Save WebP and JPEG outputs as: basename-<width>.webp and basename-<width>.jpg
- NOT overwrite existing files without prompt (it will skip existing targets)

Be sure you have a backup of your IMAGES folder before running.
"""
from PIL import Image
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
IMAGES_DIR = ROOT / 'IMAGES'

# Map of current filenames (as in your repo) -> safe target basename (without extension)
RENAME_MAP = {
    'clearing&grubbing.jpg': 'clearing-grubbing',
    'grading&siteprep.jpg': 'grading-siteprep',
    'drainage&erosioncontrol.jpg': 'drainage-erosioncontrol',
    'earth&earthwork.png': 'earth-earthwork',
    'tophalfofpagebackground.png': 'tophalf',
    'bottomhalfpagebackground.png': 'bottomhalf',
    'imageslogo.png': 'imageslogo'
}

# Output sizes (target widths)
SIZES = [320, 640, 1200]

FORMATS = ['webp', 'jpg']

def ensure_images_dir():
    if not IMAGES_DIR.exists():
        raise SystemExit(f'IMAGES directory not found at {IMAGES_DIR}')

def find_source(name):
    p = IMAGES_DIR / name
    return p if p.exists() else None

def safe_rename(src: Path, target_basename: str):
    ext = src.suffix.lower()
    target = IMAGES_DIR / (f"{target_basename}{ext}")
    if src.name == target.name:
        return target
    if target.exists():
        print(f"Target already exists, skipping rename: {target.name}")
        return target
    print(f"Renaming {src.name} -> {target.name}")
    shutil.move(str(src), str(target))
    return target


def make_resizes(src: Path, target_basename: str):
    try:
        img = Image.open(src)
    except Exception as e:
        print(f"Could not open {src.name}: {e}")
        return

    for w in SIZES:
        # compute height preserving aspect ratio
        h = int(img.height * (w / img.width))
        resized = img.resize((w, h), Image.LANCZOS)
        for fmt in FORMATS:
            out = IMAGES_DIR / f"{target_basename}-{w}.{fmt}"
            if out.exists():
                print(f"Skipping existing file: {out.name}")
                continue
            try:
                if fmt == 'jpg':
                    resized.convert('RGB').save(out, 'JPEG', quality=85)
                else:
                    resized.save(out, 'WEBP', quality=85)
                print(f"Wrote {out.name}")
            except Exception as e:
                print(f"Failed to write {out.name}: {e}")


def main():
    ensure_images_dir()

    # Process rename and generate resizes
    for src_name, base in RENAME_MAP.items():
        src_path = find_source(src_name)
        if not src_path:
            # try case-insensitive search
            found = None
            for p in IMAGES_DIR.iterdir():
                if p.name.lower() == src_name.lower():
                    found = p
                    break
            if found:
                src_path = found
            else:
                print(f"Source not found (skipping): {src_name}")
                continue

        target = safe_rename(src_path, base)
        make_resizes(target, base)

    print('Done. Check IMAGES/ for generated files.')

if __name__ == '__main__':
    main()
