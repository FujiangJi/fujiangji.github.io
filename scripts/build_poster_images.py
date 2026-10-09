"""Render conference posters for a lightweight gallery and detailed reading.

Run with the bundled Python environment (Pillow) and Poppler installed.
Initial import: pass --sources with a JSON list containing poster metadata and
local source PDF paths. Rebuilds use the copied PDFs and existing manifest.
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'assets/data/posters.json'
PDFS = ROOT / 'assets/posters'
IMAGES = ROOT / 'assets/images/posters'


def resized(image, destination, edge, quality):
    result = image.copy()
    result.thumbnail((edge, edge), Image.Resampling.LANCZOS)
    result.save(destination, 'WEBP', quality=quality, method=5)
    return result.size


def build(sources):
    entries = json.loads(sources.read_text())
    PDFS.mkdir(parents=True, exist_ok=True)
    IMAGES.mkdir(parents=True, exist_ok=True)
    output = []
    for entry in entries:
        entry = dict(entry)
        identifier = entry['id']
        pdf = PDFS / f'{identifier}.pdf'
        source = Path(entry.pop('source')) if 'source' in entry else pdf
        if source.resolve() != pdf.resolve():
            shutil.copy2(source, pdf)
        info = subprocess.check_output(['pdfinfo', str(pdf)], text=True)
        pages = next(int(line.split(':', 1)[1]) for line in info.splitlines() if line.startswith('Pages:'))
        if pages != 1:
            raise ValueError(f'{pdf.name}: expected a single-page poster')
        folder = IMAGES / identifier
        folder.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='poster-render-') as scratch:
            prefix = Path(scratch) / 'poster'
            subprocess.run([
                'pdftoppm', '-f', '1', '-singlefile', '-scale-to', '8000',
                '-png', str(pdf), str(prefix)
            ], check=True)
            with Image.open(prefix.with_suffix('.png')) as opened:
                image = opened.convert('RGB')
                width, height = image.size
                # Lossless WebP retains the full rendering, including fine text.
                image.save(folder / 'full.webp', 'WEBP', lossless=True, quality=80, method=4)
                thumb_width, thumb_height = resized(image, folder / 'thumb.webp', 960, 86)
                resized(image, folder / 'preview.webp', 2000, 90)
        entry.update({
            'pdf': '../' + pdf.relative_to(ROOT).as_posix(),
            'thumb': '../' + (folder / 'thumb.webp').relative_to(ROOT).as_posix(),
            'preview': '../' + (folder / 'preview.webp').relative_to(ROOT).as_posix(),
            'full': '../' + (folder / 'full.webp').relative_to(ROOT).as_posix(),
            'width': width, 'height': height,
            'thumbWidth': thumb_width, 'thumbHeight': thumb_height,
            'pdfBytes': pdf.stat().st_size,
            'fullBytes': (folder / 'full.webp').stat().st_size,
            'pdfSha256': hashlib.sha256(pdf.read_bytes()).hexdigest(),
        })
        output.append(entry)
        print(f"{entry['title']}: {width} × {height}, full {entry['fullBytes'] / 1_000_000:.2f} MB", flush=True)
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    thumbnail_bytes = sum((IMAGES / entry['id'] / 'thumb.webp').stat().st_size for entry in output)
    print(f'All five thumbnails: {thumbnail_bytes / 1_000_000:.2f} MB', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sources', type=Path, default=MANIFEST)
    build(parser.parse_args().sources)
