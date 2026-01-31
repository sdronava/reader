import os
import json
from .images import copy_images_from_epub
from .epub import extract_html
from .segments import segment_blocks
from pathlib import Path

def write_segments(segments: list, out_dir: str):
    for seg in segments:
        seg_dir = os.path.join(out_dir, seg["segment_id"])
        os.makedirs(seg_dir, exist_ok=True)
        filepath = os.path.join(seg_dir, f"{seg['segment_id']}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(seg, f, ensure_ascii=False, indent=2)

def build_book(epub_path: str, out_dir="build", segment_tokens=1000, resources_uri="images/"):
    os.makedirs(out_dir, exist_ok=True)
    # 0. Copy images from EPUB to output directory
    out_dir = Path(out_dir)
    copy_images_from_epub(epub_path, out_dir)

    # 1. Extract blocks from EPUB
    blocks = extract_html(epub_path, out_dir=out_dir, resources_uri=resources_uri)

    # 2. Segment blocks
    segments = segment_blocks(blocks, max_tokens=segment_tokens)

    # 3. Write segments to JSON
    write_segments(segments, out_dir)

    print(f"Build complete. Segments written to {out_dir}")
