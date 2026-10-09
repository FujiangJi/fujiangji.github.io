"""Generate editable SVG keyword figures for the homepage.

Sizes express research emphasis, rather than measured word frequencies.
Update KEYWORDS below when the research program changes. Requires Pillow.
"""

import argparse
import math
from html import escape
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT, GAP = 1400, 850, 10
KEYWORDS = [
    ("Hyperspectral Remote Sensing", 76, "blue"),
    ("Plant Functional Traits", 76, "ink"),
    ("Biological Soil Crusts", 72, "earth"),
    ("Ecosystem Function", 60, "ink"),
    ("Forest Fragmentation", 56, "blue"),
    ("Dryland Ecosystems", 54, "earth"),
    ("Imaging Spectroscopy", 54, "blue"),
    ("Functional Diversity", 46, "ink"),
    ("Data Fusion", 46, "blue"),
    ("Climate Feedbacks", 44, "earth"),
    ("Deep Learning", 40, "blue"),
    ("Community Composition", 36, "earth"),
    ("Trait Transferability", 34, "ink"),
    ("Radiative Transfer", 34, "blue"),
    ("Multiscale Mapping", 34, "blue"),
    ("Forest Edge Effects", 34, "ink"),
    ("Global Change", 34, "earth"),
    ("Seasonal Dynamics", 32, "ink"),
    ("EMIT", 40, "earth"),
    ("Transfer Learning", 30, "blue"),
    ("Leaf Spectroscopy", 30, "muted"),
    ("Climate Experiments", 30, "earth"),
    ("Spectral Diversity", 30, "ink"),
    ("Field Observations", 30, "muted"),
    ("PRISMA", 30, "muted"),
    ("EnMAP", 30, "muted"),
    ("NEON AOP", 28, "muted"),
    ("PlanetScope", 28, "muted"),
    ("UAS", 28, "muted"),
]
PALETTES = {
    "light": {"blue": "#365f9c", "ink": "#263f62", "earth": "#986449", "muted": "#64738a"},
    "dark": {"blue": "#aac8ff", "ink": "#e4edf9", "earth": "#e7b893", "muted": "#aebdd1"},
}


def intersects(a, b):
    return not (a[2] + GAP <= b[0] or b[2] + GAP <= a[0]
                or a[3] + GAP <= b[1] or b[3] + GAP <= a[1])


def make_layout(font_path):
    placed = []
    for label, wanted_size, category in KEYWORDS:
        for size in range(wanted_size, 25, -2):
            font = ImageFont.truetype(str(font_path), size)
            bbox = font.getbbox(label)
            width, height = bbox[2] - bbox[0] + 4, bbox[3] - bbox[1] + 4
            found = None
            for step in range(32000):
                radius = 4.8 * math.sqrt(step)
                angle = step * 2.399963229728653
                x = round(WIDTH / 2 + radius * math.cos(angle) - width / 2)
                y = round(HEIGHT / 2 + radius * math.sin(angle) * 0.7 - height / 2)
                rect = (x, y, x + width, y + height)
                if x < 26 or y < 20 or x + width > WIDTH - 26 or y + height > HEIGHT - 20:
                    continue
                # Give the cloud a soft oval outline, without a decorative mask.
                if any(((px - WIDTH / 2) / (WIDTH / 2)) ** 2
                       + ((py - HEIGHT / 2) / (HEIGHT / 2)) ** 2 > 1
                       for px, py in [(x, y), (x + width, y), (x, y + height), (x + width, y + height)]):
                    continue
                if any(intersects(rect, item["rect"]) for item in placed):
                    continue
                found = {"label": label, "size": size, "category": category,
                         "rect": rect, "x": x - bbox[0] + 2, "y": y - bbox[1] + 2,
                         "baseline": y - bbox[1] + 2 + font.getmetrics()[0]}
                break
            if found:
                placed.append(found)
                break
        else:
            raise RuntimeError(f"Cannot place keyword: {label}")
    return placed


def write_svg(layout, palette, destination):
    description = "Research themes and methods: " + "; ".join(item["label"] for item in layout) + "."
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">',
        '<title id="title">Fujiang Ji — research overview</title>',
        f'<desc id="desc">{escape(description)}</desc>',
        '<g font-family="Arial, Helvetica, sans-serif" font-weight="700">',
    ]
    for item in layout:
        lines.append(f'<text x="{item["x"]}" y="{item["baseline"]}" font-size="{item["size"]}" fill="{palette[item["category"]]}">{escape(item["label"])}</text>')
    lines.extend(['</g>', '</svg>'])
    destination.write_text('\n'.join(lines) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--font', type=Path, default=Path('/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
    parser.add_argument('--preview', type=Path, help='Optional PNG proof, outside the website assets.')
    args = parser.parse_args()
    layout = make_layout(args.font)
    assets = Path(__file__).resolve().parents[1] / 'assets/images/about_page'
    for theme, palette in PALETTES.items():
        write_svg(layout, palette, assets / f'Research_overview_{theme}.svg')
    if args.preview:
        image = Image.new('RGB', (WIDTH, HEIGHT), '#fffefb')
        draw = ImageDraw.Draw(image)
        for item in layout:
            draw.text((item['x'], item['y']), item['label'],
                      font=ImageFont.truetype(str(args.font), item['size']),
                      fill=PALETTES['light'][item['category']])
        image.save(args.preview)
    print(f'Generated light and dark SVGs with {len(layout)} keywords.')
    print('Primary keyword sizes:', [(item['label'], item['size']) for item in layout[:7]])


if __name__ == '__main__':
    main()
