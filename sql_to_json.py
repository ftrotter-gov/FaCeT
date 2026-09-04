#!/usr/bin/env python3
"""Convert the FaCeT ``sql/`` INSERT files into JSON and back-fill ``credential_class``.

The SQL files in ``sql/`` use ``--`` comments to delimit logical sections of
credentials (for example ``-- Physician Board Certifications``).  Those section
comments are the ``credential_class`` of every row that follows them.

For every ``insert_*.sql`` file this script writes ``json/<name>.json`` shaped as::

    [
      {
        "credential_class": "Homeopathic Medical Doctors",
        "credential_list": [
          {"id": 19, "credential_abbr": "MD(H)", ..., "credential_class": "Homeopathic Medical Doctors"}
        ]
      }
    ]

It also rewrites the SQL files in place so that ``credential_class`` becomes a
real column, which makes the data convenient to work with row by row.

Usage::

    python sql_to_json.py                # write json/ and update sql/
    python sql_to_json.py --no-sql-update  # only (re)generate json/
"""

from __future__ import annotations

import argparse
import json
import os
from typing import Any

from sqlglot.tokens import Tokenizer, TokenType

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SQL_DIR = os.path.join(PROJECT_ROOT, "sql")
DEFAULT_JSON_DIR = os.path.join(PROJECT_ROOT, "json")

# The column that this migration introduces.
CREDENTIAL_CLASS_COLUMN = "credential_class"

# Only files that actually carry data are migrated; ``create_*.sql`` is DDL.
INSERT_FILE_PREFIX = "insert_"

# Boilerplate that appears in the file header comments and carries no meaning as a
# credential class, e.g. "-- INSERT statements for Physician credentials".
_BOILERPLATE_PREFIXES = (
    "INSERT statements for ",
    "Split from ",
)


def iter_insert_files(sql_dir: str) -> list[str]:
    """Return the absolute paths of every data-bearing SQL file, sorted by name."""
    names = [
        name
        for name in os.listdir(sql_dir)
        if name.startswith(INSERT_FILE_PREFIX) and name.endswith(".sql")
    ]
    return [os.path.join(sql_dir, name) for name in sorted(names)]


def _string_char_ranges(tokens: list) -> list[tuple[int, int]]:
    """Character spans covered by string literals, used to ignore ``--`` inside data."""
    return [
        (token.start, token.end)
        for token in tokens
        if token.token_type == TokenType.STRING
    ]


def _line_start_offsets(text: str) -> list[int]:
    """Character offset at which each 1-based line begins (index 0 is unused)."""
    offsets = [0, 0]
    for line in text.split("\n")[:-1]:
        offsets.append(offsets[-1] + len(line) + 1)
    return offsets


def build_credential_class_map(text: str, tokens: list) -> dict[int, str]:
    """Map a line number to the ``credential_class`` label that starts on that line.

    A label is built from a *contiguous block* of standalone ``--`` comment lines so
    that multi-line file headers collapse into a single class.  Comments that trail a
    row of data (``..., NULL), -- 1000``) are ignored because the line does not begin
    with ``--``.  Comment markers that live inside a string literal are ignored too.
    """
    lines = text.split("\n")
    line_starts = _line_start_offsets(text)
    string_ranges = _string_char_ranges(tokens)

    def inside_string(offset: int) -> bool:
        return any(start <= offset <= end for start, end in string_ranges)

    comment_lines: dict[int, str] = {}
    for index, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped.startswith("--"):
            continue
        offset = line_starts[index] + (len(line) - len(line.lstrip()))
        if inside_string(offset):
            continue
        body = stripped.lstrip("-").strip()
        if body.startswith(_BOILERPLATE_PREFIXES):
            # Keep the descriptive tail so the header still forms one block, but
            # drop the "INSERT statements for " style boilerplate lead-in.
            for prefix in _BOILERPLATE_PREFIXES:
                if body.startswith(prefix):
                    body = body[len(prefix) :].strip()
                    break
        if body:
            comment_lines[index] = body

    # Collapse contiguous comment lines into one label, recorded on the first line.
    class_map: dict[int, str] = {}
    for line_number in sorted(comment_lines):
        if line_number - 1 in comment_lines:
            continue  # part of a block that was already consumed
        parts = []
        cursor = line_number
        while cursor in comment_lines:
            parts.append(comment_lines[cursor])
            cursor += 1
        class_map[line_number] = " ".join(parts)
    return class_map


def class_for_line(class_map: dict[int, str], line_number: int) -> str | None:
    """The most recent ``credential_class`` label declared before ``line_number``."""
    candidates = [start for start in class_map if start < line_number]
    if not candidates:
        return None
    return class_map[max(candidates)]


def _token_value(value_tokens: list) -> Any:
    """Convert the tokens of a single VALUES field into a native Python value."""
    if not value_tokens:
        return None

    if len(value_tokens) == 2 and value_tokens[0].token_type == TokenType.DASH:
        return -_token_value(value_tokens[1:])

    if len(value_tokens) == 1:
        token = value_tokens[0]
        token_type = token.token_type
        if token_type == TokenType.NUMBER:
            text = token.text
            return float(text) if ("." in text or "e" in text.lower()) else int(text)
        if token_type == TokenType.STRING:
            return token.text
        if token_type == TokenType.TRUE:
            return True
        if token_type == TokenType.FALSE:
            return False
        if token_type == TokenType.NULL:
            return None
        return token.text

    return " ".join(token.text for token in value_tokens)


def parse_rows(text: str) -> list[dict[str, Any]]:
    """Parse every VALUES row in ``text`` into a dict keyed by the INSERT columns.

    Each returned dict also carries ``credential_class`` plus the private ``_line``
    key describing where the row started, which the SQL rewriter uses to locate it.
    """
    tokens = Tokenizer().tokenize(text)
    class_map = build_credential_class_map(text, tokens)

    rows: list[dict[str, Any]] = []
    columns: list[str] = []
    index = 0
    total = len(tokens)

    while index < total:
        token = tokens[index]

        if token.token_type == TokenType.INSERT:
            # Collect the column names declared between the first balanced parens.
            columns = []
            cursor = index
            while cursor < total and tokens[cursor].token_type != TokenType.L_PAREN:
                cursor += 1
            depth = 0
            while cursor < total:
                current = tokens[cursor]
                if current.token_type == TokenType.L_PAREN:
                    depth += 1
                elif current.token_type == TokenType.R_PAREN:
                    depth -= 1
                    if depth == 0:
                        break
                elif current.token_type != TokenType.COMMA:
                    columns.append(current.text)
                cursor += 1
            index = cursor + 1
            continue

        if token.token_type == TokenType.VALUES:
            index += 1
            # Consume every parenthesised tuple that follows this VALUES keyword.
            while index < total and tokens[index].token_type == TokenType.L_PAREN:
                row_line = tokens[index].line
                index += 1
                values: list[Any] = []
                buffer: list = []
                depth = 1
                while index < total:
                    current = tokens[index]
                    if current.token_type == TokenType.L_PAREN:
                        depth += 1
                        buffer.append(current)
                    elif current.token_type == TokenType.R_PAREN:
                        depth -= 1
                        if depth == 0:
                            values.append(_token_value(buffer))
                            index += 1
                            break
                        buffer.append(current)
                    elif current.token_type == TokenType.COMMA and depth == 1:
                        values.append(_token_value(buffer))
                        buffer = []
                    else:
                        buffer.append(current)
                    index += 1

                row = dict(zip(columns, values))
                row[CREDENTIAL_CLASS_COLUMN] = class_for_line(class_map, row_line)
                row["_line"] = row_line
                rows.append(row)

                # Skip the comma separating consecutive tuples.
                if index < total and tokens[index].token_type == TokenType.COMMA:
                    index += 1
            continue

        index += 1

    return rows


def group_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Group consecutive rows that share a ``credential_class`` into the JSON shape."""
    groups: list[dict[str, Any]] = []
    for row in rows:
        payload = {key: value for key, value in row.items() if key != "_line"}
        label = payload[CREDENTIAL_CLASS_COLUMN]
        if groups and groups[-1][CREDENTIAL_CLASS_COLUMN] == label:
            groups[-1]["credential_list"].append(payload)
        else:
            groups.append(
                {CREDENTIAL_CLASS_COLUMN: label, "credential_list": [payload]}
            )
    return groups


def convert_file(sql_path: str) -> list[dict[str, Any]]:
    """Read one SQL file and return its grouped JSON structure."""
    with open(sql_path, encoding="utf-8") as handle:
        text = handle.read()
    return group_rows(parse_rows(text))


def sql_literal(value: Any) -> str:
    """Render a Python value as a SQL literal."""
    if value is None:
        return "NULL"
    if value is True:
        return "TRUE"
    if value is False:
        return "FALSE"
    if isinstance(value, (int, float)):
        return str(value)
    return "'" + str(value).replace("'", "''") + "'"


def _format_addition(text: str, close_offset: int, addition: str) -> tuple[int, str]:
    """Return where and what to insert so ``addition`` matches the local layout.

    The text is appended directly after the final existing entry rather than before
    the closing paren, which keeps the separating comma attached to that entry.
    Single-line tuples receive ``, value`` inline; the multi-line layout used by the
    ``org_credential`` files receives a new line indented to match its siblings.
    """
    # Step back over the whitespace that precedes the closing paren.
    offset = close_offset
    while offset > 0 and text[offset - 1] in " \t\r\n":
        offset -= 1

    if "\n" not in text[offset:close_offset]:
        return offset, ", " + addition

    # The closing paren sits on its own line; mirror the last entry's indentation.
    last_line_start = text.rfind("\n", 0, offset) + 1
    last_line = text[last_line_start:offset]
    indent = last_line[: len(last_line) - len(last_line.lstrip())]
    return offset, ",\n" + indent + addition


def add_credential_class_to_sql(text: str) -> str:
    """Return ``text`` rewritten so ``credential_class`` is a real column.

    The column name is appended to each INSERT column list and the matching value is
    appended to each VALUES tuple.  Edits are applied from the end of the file
    backwards so that earlier character offsets stay valid.
    """
    tokens = Tokenizer().tokenize(text)
    class_map = build_credential_class_map(text, tokens)

    # (offset, text_to_insert) pairs.
    edits: list[tuple[int, str]] = []
    index = 0
    total = len(tokens)
    columns: list[str] = []

    while index < total:
        token = tokens[index]

        if token.token_type == TokenType.INSERT:
            columns = []
            cursor = index
            while cursor < total and tokens[cursor].token_type != TokenType.L_PAREN:
                cursor += 1
            depth = 0
            close_token = None
            while cursor < total:
                current = tokens[cursor]
                if current.token_type == TokenType.L_PAREN:
                    depth += 1
                elif current.token_type == TokenType.R_PAREN:
                    depth -= 1
                    if depth == 0:
                        close_token = current
                        break
                elif current.token_type != TokenType.COMMA:
                    columns.append(current.text)
                cursor += 1

            if close_token is not None and CREDENTIAL_CLASS_COLUMN not in columns:
                edits.append(
                    _format_addition(
                        text, close_token.start, CREDENTIAL_CLASS_COLUMN
                    )
                )
            index = cursor + 1
            continue

        if token.token_type == TokenType.VALUES:
            index += 1
            while index < total and tokens[index].token_type == TokenType.L_PAREN:
                row_line = tokens[index].line
                index += 1
                depth = 1
                close_token = None
                while index < total:
                    current = tokens[index]
                    if current.token_type == TokenType.L_PAREN:
                        depth += 1
                    elif current.token_type == TokenType.R_PAREN:
                        depth -= 1
                        if depth == 0:
                            close_token = current
                            index += 1
                            break
                    index += 1

                if close_token is not None and CREDENTIAL_CLASS_COLUMN not in columns:
                    label = class_for_line(class_map, row_line)
                    edits.append(
                        _format_addition(text, close_token.start, sql_literal(label))
                    )

                if index < total and tokens[index].token_type == TokenType.COMMA:
                    index += 1
            continue

        index += 1

    for offset, addition in sorted(edits, reverse=True):
        text = text[:offset] + addition + text[offset:]
    return text


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sql-dir", default=DEFAULT_SQL_DIR)
    parser.add_argument("--json-dir", default=DEFAULT_JSON_DIR)
    parser.add_argument(
        "--no-sql-update",
        action="store_true",
        help="only regenerate the JSON files, leave sql/ untouched",
    )
    args = parser.parse_args()

    os.makedirs(args.json_dir, exist_ok=True)

    total_rows = 0
    for sql_path in iter_insert_files(args.sql_dir):
        name = os.path.basename(sql_path)

        if not args.no_sql_update:
            with open(sql_path, encoding="utf-8") as handle:
                original = handle.read()
            updated = add_credential_class_to_sql(original)
            if updated != original:
                with open(sql_path, "w", encoding="utf-8") as handle:
                    handle.write(updated)

        groups = convert_file(sql_path)
        rows = sum(len(group["credential_list"]) for group in groups)
        total_rows += rows

        json_path = os.path.join(args.json_dir, name[: -len(".sql")] + ".json")
        with open(json_path, "w", encoding="utf-8") as handle:
            json.dump(groups, handle, indent=2, ensure_ascii=False)
            handle.write("\n")

        print(f"{name}: {len(groups)} classes, {rows} rows -> {os.path.basename(json_path)}")

    print(f"\nTotal: {total_rows} rows")


if __name__ == "__main__":
    main()
