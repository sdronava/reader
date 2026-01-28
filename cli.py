import argparse
from forge.build import build_book

def main():
    parser = argparse.ArgumentParser("forge")
    sub = parser.add_subparsers(dest="command")

    build = sub.add_parser("build")
    build.add_argument("epub")
    build.add_argument("--out", default="./build")
    build.add_argument("--segment-tokens", type=int, default=1000)

    args = parser.parse_args()

    if args.command == "build":
        build_book(
            epub_path=args.epub,
            out_dir=args.out,
            segment_tokens=args.segment_tokens
        )

if __name__ == "__main__":
    main()
