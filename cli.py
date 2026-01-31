#!/usr/bin/env python3
import argparse
from forge.build import build_book

def main():
    parser = argparse.ArgumentParser(description="Build a reader-friendly JSON version of an EPUB.")
    parser.add_argument("epub", help="Path to the EPUB file")
    parser.add_argument("--out", default="./build", help="Output folder")
    parser.add_argument("--segment-tokens", type=int, default=1000, help="Max tokens per segment")
    parser.add_argument("--resources-uri", default="images/", help="Base URI for resources like images")

    args = parser.parse_args()

    build_book(
        epub_path=args.epub,
        out_dir=args.out,
        segment_tokens=args.segment_tokens,
        resources_uri=args.resources_uri
    )

if __name__ == "__main__":
    main()
