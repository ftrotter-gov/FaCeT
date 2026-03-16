#!/usr/bin/env python3
"""split_org_credential_hospital_sql.py

Splits `sql/insert_org_credential_hospital.sql` into multiple smaller SQL files
based on the `category` field in each INSERT block.

Why:
  The hospital org-credential insert file has grown large and is easier to
  maintain when split into one file per category.

What it does:
  - Parses the file as a series of INSERT blocks (optionally preceded by `--`
    comment lines).
  - Each block is expected to contain rows for exactly one category.
  - Writes output files:
      sql/insert_org_credential_hospital_<category>.sql

Safety / idempotence:
  - By default, refuses to overwrite output files unless you pass --overwrite.
  - Can optionally replace the original input file with a short pointer comment
    via --slim-input.

Usage:
  python src/split_org_credential_hospital_sql.py --slim-input --overwrite
"""

from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from pathlib import Path


INSERT_BLOCK_RE = re.compile(
    r"(?:^|\n)"  # start or newline
    r"(?P<prefix>(?:--[^\n]*\n)*)"  # any leading -- comment lines
    r"\s*"
    r"(?P<insert>"  # the insert statement through its terminating semicolon
    r"INSERT\s+INTO\s+org_credential\s*\([\s\S]*?\)\s*VALUES\s*[\s\S]*?;"
    r")",
    re.IGNORECASE,
)

# Tuple start lines look like: (
#     1000,
#     'certification',
ROW_CATEGORY_RE = re.compile(r"\(\s*\d+\s*,\s*'([^']+)'\s*,", re.MULTILINE)


def parse_insert_blocks(sql_text: str) -> list[str]:
    """Return a list of INSERT blocks, each including any immediately preceding
    comment lines.
    """
    text = (sql_text or "").strip() + "\n"
    blocks: list[str] = []
    for m in INSERT_BLOCK_RE.finditer(text):
        prefix = m.group("prefix") or ""
        insert = m.group("insert")
        blocks.append((prefix + insert).strip() + "\n")
    return blocks


def categories_in_block(block: str) -> list[str]:
    return sorted(set(ROW_CATEGORY_RE.findall(block)))


def write_file(*, path: Path, content: str, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(
            f"Refusing to overwrite existing file: {path} (pass --overwrite)"
        )
    path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Split hospital org_credential insert SQL into per-category files."
    )
    parser.add_argument(
        "--input",
        default="sql/insert_org_credential_hospital.sql",
        help="Input SQL file to split (default: %(default)s)",
    )
    parser.add_argument(
        "--out-dir",
        default="sql",
        help="Output directory for split SQL files (default: %(default)s)",
    )
    parser.add_argument(
        "--prefix",
        default="insert_org_credential_hospital_",
        help="Filename prefix for output files (default: %(default)s)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite output files if they already exist",
    )
    parser.add_argument(
        "--slim-input",
        action="store_true",
        help="Replace the input file contents with a short pointer comment (prevents duplicate inserts)",
    )

    args = parser.parse_args()

    in_path = Path(args.input)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    sql_text = in_path.read_text(encoding="utf-8")
    blocks = parse_insert_blocks(sql_text)
    if not blocks:
        raise SystemExit(f"No INSERT blocks found in {in_path} (pattern mismatch?)")

    blocks_by_category: dict[str, list[str]] = defaultdict(list)
    multi_category_blocks: list[tuple[list[str], str]] = []

    for b in blocks:
        cats = categories_in_block(b)
        if len(cats) != 1:
            multi_category_blocks.append((cats, b))
            continue
        blocks_by_category[cats[0]].append(b)

    if multi_category_blocks:
        details = "\n".join(
            f"- categories={cats} ..." for cats, _ in multi_category_blocks
        )
        raise SystemExit(
            "One or more INSERT blocks contained 0 or multiple categories. "
            "Please split those blocks manually or improve the parser.\n" + details
        )

    # basic stats (rows, by category)
    row_categories = ROW_CATEGORY_RE.findall(sql_text)
    row_counts = Counter(row_categories)

    written_files: list[Path] = []
    for category in sorted(blocks_by_category.keys()):
        out_path = out_dir / f"{args.prefix}{category}.sql"
        header = (
            f"-- Hospital org credentials: {category}\n"
            "-- Split from insert_org_credential_hospital.sql\n\n"
        )
        content = header + "\n\n".join(blocks_by_category[category]).strip() + "\n"
        write_file(path=out_path, content=content, overwrite=args.overwrite)
        written_files.append(out_path)

    if args.slim_input:
        pointer = (
            "-- NOTE: This file was split into category-specific files to keep sizes manageable.\n"
            "-- Use these files instead (they are all merged by merge_sql.py automatically):\n"
            + "".join(
                f"--   - {args.prefix}{category}.sql\n"
                for category in sorted(blocks_by_category.keys())
            )
        )
        write_file(path=in_path, content=pointer, overwrite=True)

    # Print summary for humans/CI logs
    print(f"Read: {in_path}")
    print(f"Found INSERT blocks: {len(blocks)}")
    print("Rows by category (from row scan):")
    for cat, cnt in sorted(row_counts.items()):
        print(f"  {cat}: {cnt}")
    print("Wrote:")
    for p in written_files:
        print(f"  {p}")
    if args.slim_input:
        print(f"Slimmed input file in place: {in_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
