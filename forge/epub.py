import os
import zipfile
from bs4 import BeautifulSoup
from .blocks import create_block
from pathlib import Path, PurePosixPath
from .spine import get_spine_html_files
import xml.etree.ElementTree as ET

def extract_metadata(epub_path: str) -> dict:
    """
    Extract basic metadata from EPUB (content.opf)
    Returns dict with title, author, language, identifier.
    """
    metadata = {
        "title": None,
        "author": None,
        "language": None,
        "identifier": None
    }

    with zipfile.ZipFile(epub_path, "r") as zf:
        # find content.opf
        opf_path = None
        for f in zf.namelist():
            if f.endswith(".opf"):
                opf_path = f
                break

        if not opf_path:
            print("Warning: content.opf not found in EPUB")
            return metadata

        # parse XML
        content = zf.read(opf_path).decode("utf-8")
        tree = ET.fromstring(content)

        # EPUB metadata namespace
        ns = {"dc": "http://purl.org/dc/elements/1.1/"}

        title_elem = tree.find(".//dc:title", ns)
        author_elem = tree.find(".//dc:creator", ns)
        lang_elem = tree.find(".//dc:language", ns)
        id_elem = tree.find(".//dc:identifier", ns)

        if title_elem is not None:
            metadata["title"] = title_elem.text
        if author_elem is not None:
            metadata["author"] = author_elem.text
        if lang_elem is not None:
            metadata["language"] = lang_elem.text
        if id_elem is not None:
            metadata["identifier"] = id_elem.text

    return metadata



def extract_html(epub_path: str, out_dir: str, resources_uri: str) -> list:
    """
    Extract HTML content from EPUB and generate blocks.
    Image blocks will point to the already extracted images folder
    defined by resources_uri.
    """
    blocks = []
    resources_uri = Path(resources_uri)  # ensure Path object for joins

    with zipfile.ZipFile(epub_path, "r") as zf:
        ordered_files = get_spine_html_files(epub_path)
        for name in ordered_files:
        #for name in zf.namelist():
            if name.lower().endswith((".xhtml", ".html")):
                content = zf.read(name).decode("utf-8")
                soup = BeautifulSoup(content, "lxml")

                # Text blocks
                for elem in soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6"]):
                    text = elem.get_text(strip=True)
                    if text:
                        blocks.append(create_block(text))

                # Image blocks — just point to existing extracted images
                for img in soup.find_all("img"):
                    src = img.get("src")
                    if src:
                        img_name = Path(PurePosixPath(src).name)  # normalize filename
                        img_uri = resources_uri / img_name
                        print(img_uri)

                        blocks.append(
                            create_block(
                                content=str(img_uri),
                                block_type="image",
                                metadata={"original_path": src},
                                tokens=0,
                            )
                        )

    return blocks