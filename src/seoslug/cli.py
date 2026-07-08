"""Command-line helpers for seoslug."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

from .validation import validate_html_jsonld


def _read_input(path: str) -> str:
    if path == "-":
        import sys

        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="seoslug")
    subparsers = parser.add_subparsers(dest="command", required=True)

    html_parser = subparsers.add_parser("validate-html", help="Validate rendered HTML JSON-LD blocks")
    html_parser.add_argument("paths", nargs="+", help="HTML files or - for stdin")
    html_parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")

    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.command != "validate-html":
        parser.error("unknown command")

    exit_code = 0
    for path in args.paths:
        html = _read_input(path)
        warnings = validate_html_jsonld(html, strict=args.strict)
        if warnings:
            exit_code = 1
            for warning in warnings:
                print(f"{path}: {warning}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
