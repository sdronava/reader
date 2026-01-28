import json
import os
from .epub import extract_toc, extract_blocks_from_section, resolve_epub_path
from .segments import segment_blocks
from .ids import gen_id

def build_book(epub_path, out_dir, segment_tokens):
    os.makedirs(out_dir, exist_ok=True)

    toc = extract_toc(epub_path)

    manifest = {
        "book_id": gen_id("book"),
        "chapters": []
    }

    for ch in toc["chapters"]:
        ch_dir = os.path.join(out_dir, ch["id"])
        os.makedirs(ch_dir, exist_ok=True)

        chapter_entry = {
            "chapter_id": ch["id"],
            "title": ch["title"],
            "sections": []
        }

        for sec in ch["sections"]:
            internal_path = resolve_epub_path(epub_path, sec["href"])
            blocks = extract_blocks_from_section(epub_path, internal_path)
            segments = segment_blocks(blocks, segment_tokens)

            sec_file = f"{sec['id']}.json"
            with open(os.path.join(ch_dir, sec_file), "w") as f:
                json.dump({
                    "section_id": sec["id"],
                    "segments": segments
                }, f, indent=2)

            chapter_entry["sections"].append({
                "section_id": sec["id"],
                "file": sec_file
            })

        manifest["chapters"].append(chapter_entry)

    with open(os.path.join(out_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)
