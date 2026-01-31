import os
import zipfile
from bs4 import BeautifulSoup
from .blocks import create_block
from .images import copy_image
from pathlib import Path, PurePosixPath

def extract_html(epub_path: str, out_dir: str, resources_uri: str) -> list:
    """
    Extract HTML content from EPUB and generate blocks.
    Image blocks will point to the already extracted images folder
    defined by resources_uri.
    """
    blocks = []
    resources_uri = Path(resources_uri)  # ensure Path object for joins

    with zipfile.ZipFile(epub_path, "r") as zf:
        for name in zf.namelist():
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
                        blocks.append({
                            "block_id": create_block("", "image")["block_id"],
                            "type": "image",
                            "content": str(img_uri),  # JSON URI
                            "metadata": {"original_path": src},
                            "tokens": 0
                        })

    return blocks