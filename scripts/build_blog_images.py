"""Build responsive blog photographs without changing the original files.

Run with a Python environment containing Pillow. Collection information and
photo order are maintained in pages/blogs_pages/albums-source.json.
"""
import json
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'pages/blogs_pages/albums-source.json'
OUTPUT = ROOT / 'assets/images/blogs'


def derivative(image, destination, edge, quality, profile):
    resized = image.copy()
    resized.thumbnail((edge, edge), Image.Resampling.LANCZOS)
    options = {'quality': quality, 'method': 5}
    if profile:
        options['icc_profile'] = profile
    resized.save(destination, 'WEBP', **options)
    return resized.size


def main():
    collections = json.loads(SOURCE.read_text())
    manifest = []
    for collection in collections:
        folder = OUTPUT / collection['id']
        folder.mkdir(parents=True, exist_ok=True)
        album = {key: value for key, value in collection.items() if key != 'originals'}
        album['photos'] = []
        for index, original in enumerate(collection['originals'], 1):
            source = ROOT / 'pages' / original
            if not source.is_file():
                raise FileNotFoundError(source)
            with Image.open(source) as opened:
                profile = opened.info.get('icc_profile')
                image = ImageOps.exif_transpose(opened).convert('RGB')
                view = folder / f'{index:02}-view.webp'
                thumb = folder / f'{index:02}-thumb.webp'
                dimensions = derivative(image, view, 1600, 80, profile)
                derivative(image, thumb, 240, 72, profile)
                photo = {
                    'original': original,
                    'view': '../' + view.relative_to(ROOT).as_posix(),
                    'thumb': '../' + thumb.relative_to(ROOT).as_posix(),
                    'width': dimensions[0], 'height': dimensions[1],
                    'alt': f"{collection['title']} — photograph {index}",
                }
                if index == 1:
                    cover = folder / 'cover.webp'
                    cover_dimensions = derivative(image, cover, 960, 80, profile)
                    album['cover'] = '../' + cover.relative_to(ROOT).as_posix()
                    album['coverWidth'], album['coverHeight'] = cover_dimensions
                album['photos'].append(photo)
        manifest.append(album)
        print(f"{album['title']}: {len(album['photos'])} photographs", flush=True)
    destination = ROOT / 'assets/data/blog-albums.json'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    size = sum(path.stat().st_size for path in OUTPUT.rglob('*.webp'))
    print(f'Optimized photographs: {size / 1_000_000:.1f} MB', flush=True)


if __name__ == '__main__':
    main()
