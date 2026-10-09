The Chinese webfont is a site-specific subset of Adobe's Source Han Sans CN
variable font. The subset has been renamed internally to Fujiang Site Sans.
The original copyright and SIL Open Font License are in OFL.txt.

Official source:
https://github.com/adobe-fonts/source-han-sans

Source file:
https://raw.githubusercontent.com/adobe-fonts/source-han-sans/release/Variable/WOFF2/TTF/Subset/SourceHanSansCN-VF.ttf.woff2

Rebuild with `scripts/build_site_font.py --source /path/to/original.woff2` after
adding Chinese characters to the translations. The build requires fonttools
and brotli. The full source font is intentionally kept outside the repository.

The CSS family alias is Source Han Sans; Poppins remains responsible for Latin
text. The webfont is requested only when Chinese glyphs are displayed in that
family. English mode uses system fallback fonts for the small 中文 control.
