from typing import Optional
from bs4 import BeautifulSoup


def extract_annex(soup: BeautifulSoup) -> Optional[str]:
    """Return full Annex text (concatenated paragraphs) or None."""

    # Find the Annex h2 header (case insensitive)
    annex_h2 = soup.find("h2", string=re.compile(r"^\s*Annex\s*$", re.I))

    if not annex_h2:
        return None

    texts: List[str] = []
    node = annex_h2.find_next_sibling()

    while node and not (node.name == "h2"):
        # grab paragraph–level text, skip empty / whitespace nodes
        if node.name in {"p", "ul", "ol"}:
            txt = node.get_text(" ", strip=True)

            if txt:
                texts.append(txt)

        node = node.find_next_sibling()

    joined = " ".join(texts).strip()
    return joined or None
