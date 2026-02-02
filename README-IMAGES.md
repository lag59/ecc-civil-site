Image rename and responsive generation

What I changed in the project:
- Updated `index.html` to reference safer image filenames (hyphens instead of `&`).
- Added `loading`/`decoding`/`width`/`height` attributes for logos and service icons.
- Added `scripts/generate_images.py` to rename original files to safe names and generate resized WebP/JPEG variants.

How to run (Windows):
1. Install Pillow if you don't have it:

```powershell
python -m pip install --upgrade pip
python -m pip install pillow
```

2. Run the script from the project root (where `index.html` sits):

```powershell
python .\scripts\generate_images.py
```

3. The script will:
- Look in the `IMAGES` folder for the mapped source filenames (case-insensitive)
- Rename files to safe names (e.g. `clearing&grubbing.jpg` -> `clearing-grubbing.jpg`)
- Produce resized variants: `basename-320.webp`, `basename-640.webp`, `basename-1200.webp` and JPEG equivalents.

Notes & safety:
- Make a backup of your `IMAGES` folder before running.
- The script will skip existing target files to avoid overwriting.
- After running, preview `index.html` in a browser — the new responsive files will be available for `srcset`/`picture` use.

If you want, I can also:
- Automatically update `styles.css` to use the generated responsive background files (currently I replaced background elements with `<picture>` tags in the HTML so the script output will match).
- Convert additional images or output different sizes/qualities.
