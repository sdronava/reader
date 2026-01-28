import zipfile
from zipfile import ZipFile
from bs4 import BeautifulSoup
from .ids import gen_id
from .segments import count_tokens

# ---- Load a single XHTML file from EPUB ----
def load_xhtml_from_epub(epub_path: str, xhtml_path: str) -> str:
    with zipfile.ZipFile(epub_path, "r") as z:
        with z.open(xhtml_path) as f:
            return f.read().decode("utf-8")

def resolve_epub_path(epub_path, href):
    """
    Resolve the href to the actual file in the EPUB zip.
    Strips any fragment (after #) before searching.
    """
    clean_href = href.split("#")[0]  # remove fragment
    with ZipFile(epub_path, "r") as z:
        files = z.namelist()
        # find the first file that ends with clean_href
        matches = [f for f in files if f.endswith(clean_href)]
        if not matches:
            raise FileNotFoundError(f"{clean_href} not found in EPUB")
        return matches[0]

# ---- Extract blocks from a section (realistic implementation) ----
def extract_blocks_from_section(epub_path: str, href: str) -> list:
    """
    href example: 'chap02.xhtml#sec1'
    """
    if "#" in href:
        xhtml_file, anchor = href.split("#", 1)
    else:
        xhtml_file, anchor = href, None

    xhtml_file = resolve_epub_path(epub_path, xhtml_file)
    html = load_xhtml_from_epub(epub_path, xhtml_file)
    soup = BeautifulSoup(html, features="xml")

    # Section root
    section_root = soup.find(id=anchor) if anchor else soup.body

    blocks = []

    for elem in section_root.find_all_next(recursive=False):
        if elem.name in ["h1", "h2", "h3"] and elem != section_root:
            break

        # Paragraph
        if elem.name == "p":
            text = elem.get_text(strip=True)
            if text:
                blocks.append({
                    "block_id": gen_id("blk"),
                    "type": "paragraph",
                    "content": text,
                    "tokens": count_tokens(text)
                })

        # Code block
        elif elem.name == "pre":
            code = elem.get_text()
            blocks.append({
                "block_id": gen_id("blk"),
                "type": "code",
                "content": code,
                "tokens": count_tokens(code),
                "capabilities": {"code": True}
            })

        # Image / figure
        elif elem.name == "img":
            src = elem.get("src")
            alt = elem.get("alt", "")
            blocks.append({
                "block_id": gen_id("blk"),
                "type": "image",
                "content": "",
                "tokens": 0,
                "media_refs": [{"type": "image", "uri": src, "caption": alt}]
            })

    return blocks

# ---- Extract TOC stub ----

def list_epub_files(epub_path):
    with ZipFile(epub_path, "r") as z:
        return z.namelist()

from zipfile import ZipFile
from bs4 import BeautifulSoup

def extract_toc(epub_path: str):
    """
    Return a TOC dict from the EPUB.
    Handles both EPUB2 (toc.ncx) and EPUB3 (nav.xhtml).
    """
    with ZipFile(epub_path, "r") as z:
        files = z.namelist()

        # Try EPUB3 first
        nav_file = next((f for f in files if "nav" in f.lower() and f.endswith(".xhtml")), None)
        if nav_file:
            html = z.read(nav_file).decode("utf-8")
            soup = BeautifulSoup(html, "lxml")
            chapters = []
            for li in soup.select("ol > li"):
                a = li.find("a")
                if a:
                    chapters.append({
                        "id": a.get("href").split("#")[0].replace(".xhtml",""),
                        "title": a.get_text(strip=True),
                        "sections": [
                            {
                                "id": a.get("href").split("#")[1] if "#" in a.get("href") else "sec-1",
                                "title": a.get_text(strip=True),
                                "href": a.get("href")
                            }
                        ]
                    })
            return {"chapters": chapters}

        # Try EPUB2
        ncx_file = next((f for f in files if f.endswith(".ncx")), None)
        if ncx_file:
            xml = z.read(ncx_file).decode("utf-8")
            soup = BeautifulSoup(xml, "xml")
            chapters = []
            for navPoint in soup.find_all("navPoint"):
                a = navPoint.find("content")
                if a and a.has_attr("src"):
                    chapters.append({
                        "id": a["src"].split("#")[0].replace(".xhtml",""),
                        "title": navPoint.find("navLabel").get_text(strip=True),
                        "sections": [
                            {
                                "id": a["src"].split("#")[1] if "#" in a["src"] else "sec-1",
                                "title": navPoint.find("navLabel").get_text(strip=True),
                                "href": a["src"]
                            }
                        ]
                    })
            return {"chapters": chapters}

        # If neither found, fail
        raise ValueError("No nav.xhtml or toc.ncx found for TOC")
