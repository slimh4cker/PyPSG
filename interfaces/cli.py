import argparse
import sys
from pathlib import Path

from core.parser import TreeParser
from core.planner import Planner
from core.executor import Executor


DESCRIPTION = """
Generate directory and file structures from a tree-formatted text input.

The input format follows the common `tree` command style, for example:

  project/
  ├── src/
  │   └── main.py
  └── README.md

Indentation must use groups of 4 characters (spaces or │).
"""

EPILOG = """
Examples:

  Read from file:
    structure-gen --input structure.txt --dest ./output

  Read from stdin:
    cat structure.txt | structure-gen --dry-run

  Inline usage:
    echo "project/\\n├── src/" | structure-gen

Notes:
  - The root element must be a directory.
  - Files are detected by extension (.py, .md, .toml, etc).
  - Use --dry-run to preview actions without creating files.
"""


def build_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(
        prog="structure-gen",
        description=DESCRIPTION,
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )


def run() -> int:
    parser = build_parser()

    parser.add_argument(
        "--input",
        type=Path,
        help="Input file containing the tree structure (defaults to stdin)"
    )

    parser.add_argument(
        "--dest",
        type=Path,
        default=Path.cwd(),
        help="Destination directory (default: current directory)"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview actions without creating files or directories"
    )

    args = parser.parse_args()

    try:
        text = (
            args.input.read_text(encoding="utf-8")
            if args.input
            else sys.stdin.read()
        )

        tree = TreeParser().parse(text)
        actions = Planner().build(tree, args.dest)

        executor = Executor(dry_run=args.dry_run)
        executor.execute(actions)

        for line in executor.log:
            print(line)

        return 0

    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(run())
