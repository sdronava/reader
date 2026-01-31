import os
import shutil
import zipfile
from pathlib import Path
from .ids import gen_id
from zipfile import ZipFile

def copy_image(src_path: str, out_dir: str, resources_uri: str) -> dict:
    """
    Copy an image to the output folder (resources folder) and return a block reference
    """
    os.makedirs(os.path.join(out_dir, resources_uri), exist_ok=True)
    filename = os.path.basename(src_path)
    dest_path = os.path.join(out_dir, resources_uri, filename)
    shutil.copyfile(src_path, dest_path)

    return {
        "block_id": gen_id("img"),
        "type": "image",
        "content": os.path.join(resources_uri, filename),
        "metadata": {"original_path": src_path},
        "tokens": 0
    }

def copy_images_from_epub(epub_path: str, out_dir: str) -> None:
    """
    Extract images from EPUB into a central 'images/' folder inside out_dir.
    Returns a dict: {image_filename: out_path}.
    """
    out_dir = Path(out_dir)  # <-- convert string to Path
    out_images = out_dir / "images"
    out_images.mkdir(parents=True, exist_ok=True)

    image_map = {}

    with ZipFile(epub_path, "r") as zf:
        for f in zf.namelist():
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                img_name = Path(f).name
                out_file = out_images / img_name
                with zf.open(f) as src, open(out_file, "wb") as dst:
                    shutil.copyfileobj(src, dst)
                image_map[img_name] = out_file

    return image_map
