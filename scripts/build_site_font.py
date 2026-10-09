"""Subset the official Source Han Sans CN variable font for this site's Chinese.

Requires fonttools and brotli. Pass the downloaded official font as --source;
the large source font is not stored in this repository. Rebuild after adding
Chinese characters to assets/i18n/zh. Latin text continues to use Poppins.
"""
import argparse
import json
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    args = parser.parse_args()
    text = '中文选择页面语言已切换为暂时未能加载请稍后重试显示篇论文项会议报告条个相册张照片查看第共教程下载原始展开代码行放大图片切换摘要研究详情自动换年日月'
    for path in (ROOT / 'assets/i18n/zh').glob('*.json'):
        text += ''.join(json.loads(path.read_text()).values())
    text += (ROOT / 'assets/js/site-language.js').read_text()
    characters = {ord(char) for char in text if any(start <= ord(char) <= end for start, end in ((0x2000, 0x206f), (0x3000, 0x303f), (0x3400, 0x9fff), (0xff00, 0xffef)))}
    font = TTFont(args.source)
    missing = characters - set(font.getBestCmap())
    if missing:
        raise ValueError('Missing source glyphs: ' + ''.join(map(chr, sorted(missing))))
    options = subset.Options()
    options.flavor = 'woff2'
    options.layout_features = ['*']
    options.name_IDs = ['*']
    subsetter = subset.Subsetter(options)
    subsetter.populate(unicodes=characters)
    subsetter.subset(font)
    # Give the modified subset its own internal family name (SIL OFL).
    for record in font['name'].names:
        if record.nameID in (1, 4, 6, 16):
            value = 'FujiangSiteSans' if record.nameID == 6 else 'Fujiang Site Sans'
            record.string = value.encode(record.getEncoding())
    font.flavor = 'woff2'
    dest = ROOT / 'assets/fonts/source-han-sans-cn-site.woff2'
    dest.parent.mkdir(parents=True, exist_ok=True)
    font.save(dest)
    print(str(len(characters)) + ' characters; ' + str(round(dest.stat().st_size / 1024)) + ' KiB')


if __name__ == '__main__':
    main()
