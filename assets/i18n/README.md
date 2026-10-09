# Website languages

English remains the source language of the twelve public HTML pages. A URL
without `lang=zh` always opens in English, regardless of browser language or
previous visits. `?lang=zh` opens the same page in Chinese. Other query
parameters and the fragment identifier are retained. Site links carry the
current language, including links between the six tutorial readers.

`assets/js/site-language.js` manages the language control, URL state, and
translations. It replaces text nodes and user-facing attributes while keeping
the original DOM elements, event listeners, forms, code, and disclosure state.
Back and forward navigation also restore the language. No language preference
is saved in local storage.

`zh/common.json` contains shared navigation, profile, footer, and interaction
text. Each page has a JSON dictionary named after its HTML filename; the
homepage uses `zh/about.json`. Keys are the original English text with
whitespace normalized. Values are authored Chinese translations. The page
dictionary overrides the shared one. Dictionaries load only when Chinese is
requested. Existing and newly inserted UI text is translated, including album
dialogs, figure captions, filtering status, and copy/form feedback.

Chinese inline text runs remove unnecessary spaces between Han characters and
Chinese punctuation, including across emphasis and link boundaries. Standalone
sentence punctuation in Chinese paragraphs is localized. Separate layout cells,
English word spacing, decimals, filenames and code are preserved. Whitespace is
recorded alongside translated text so switching back restores the English source.

The personal name is 纪甫江 in Chinese profile text, page titles, descriptions,
and footers, and Fujiang Ji in English. Bibliographic author names retain their
original English spelling.

Formal paper titles, author names, journal names, citation numbers, DOI links,
software names, and code remain in English. Original figures, posters, and the
English CV download remain unchanged. These may also be explicitly protected
with `data-i18n-keep` when adding new content.

When editing English copy, update its dictionary key and Chinese value. Add
new page filenames to the controller's page list. Use `SiteLanguage.href(url)`
for programmatic navigation, `sourceText(element)` / `sourceAttribute(element,
name)` when reading an original label into another element, and listen to
`site:languagechange` when a component needs to refresh a language-dependent
search index. Dynamic numeric status strings are formatted by the controller.

After adding Chinese characters, rebuild the local font with
`scripts/build_site_font.py`. Its source and license are documented under
`assets/fonts/`. The Latin font remains Poppins.
