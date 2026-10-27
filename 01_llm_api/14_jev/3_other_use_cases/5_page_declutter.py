"""
5) Page declutter - remove ads, cookie banners and upsells from a web page.

A browser extension can send every element of a page to Jev and hide the
annoying ones before you notice them. Jev never rewrites the page. It only
decides KEEP or REMOVE for each element, and the code does the removing.

All elements go in ONE call (one question per element), so the whole page
is judged in a few hundred milliseconds.

Input:  sample_page.html   Output: sample_page.clean.html
"""

from pathlib import Path
from bs4 import BeautifulSoup

from jev import decide, noul

HERE = Path(__file__).parent
page = BeautifulSoup((HERE / "sample_page.html").read_text(), "html.parser")
elements = page.body.find_all(recursive=False)

questions = {
    f"el{i}": noul(
        f"Should this page element be removed? Element <{el.name}>: '{el.get_text(' ', strip=True)[:300]}'",
        true="Ad, sponsored content, cookie banner, newsletter pop-up, upsell, clickbait links.",
        false="Part of the article (title, text, author) or basic navigation and footer.",
    )
    for i, el in enumerate(elements)
}

result = decide(state={"page_title": page.title.get_text()}, questions=questions)

removed = 0
for i, el in enumerate(elements):
    p_remove = result["answers"][f"el{i}"]["noul"]
    action = "REMOVE" if p_remove >= 0.5 else "keep  "
    print(f"{action} {p_remove:4.0%}  <{el.name}> {el.get_text(' ', strip=True)[:70]}")
    if p_remove >= 0.5:
        el.decompose()
        removed += 1

(HERE / "sample_page.clean.html").write_text(str(page))
print(
    f"\nRemoved {removed} of {len(elements)} elements in {result['latency_ms']} ms "
    f"for ${result['usage']['cost']:.6f}. Open sample_page.clean.html to compare."
)
