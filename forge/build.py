import os
import json
from pathlib import Path
from .images import copy_images_from_epub
from .epub import extract_html, extract_metadata
from .segments import segment_blocks

def write_segment(segment: dict, base_dir: Path):
    """Write a single segment JSON to its own folder."""
    seg_dir = base_dir / segment["segment_id"]
    seg_dir.mkdir(parents=True, exist_ok=True)

    with open(seg_dir / "segment.json", "w", encoding="utf-8") as f:
        json.dump(segment, f, ensure_ascii=False, indent=2)

def write_segments(segments: list[dict], out_dir: Path):
    """Write all segments to JSON."""
    for seg in segments:
        write_segment(seg, out_dir)

def write_metadata(book_metadata: dict, out_dir: Path):
    """Write a central metadata.json for the EPUB"""
    with open(out_dir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(book_metadata, f, ensure_ascii=False, indent=2)

def build_book(epub_path: str, out_dir="build", segment_tokens=1000, resources_uri="images/"):
    """
    Build JSON segments from an EPUB, copy images, and generate metadata.
    """
    # Ensure paths
    out_dir = Path(out_dir)
    resources_uri = Path(resources_uri)
    os.makedirs(out_dir, exist_ok=True)

    # 0. Extract images
    copy_images_from_epub(epub_path, out_dir)

    # 1. Extract EPUB metadata
    book_metadata = extract_metadata(epub_path)
    write_metadata(book_metadata, out_dir)

    # 2. Extract blocks from EPUB
    blocks = extract_html(epub_path, out_dir=out_dir, resources_uri=resources_uri)

    # 3. Segment blocks
    segments = segment_blocks(blocks, max_tokens=segment_tokens)

    # 4. Attach book metadata to each segment
    for seg in segments:
        seg["book_metadata"] = book_metadata

    # 5. Write segments to JSON
    write_segments(segments, out_dir)

    print(f"Build complete. Segments written to {out_dir}")

    return {
        "out_dir": out_dir,
        "num_blocks": len(blocks),
        "num_segments": len(segments),
        "book_metadata": book_metadata,
    }
