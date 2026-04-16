from __future__ import annotations

import argparse

from .commands.conservation import add_conservation_parser


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="enzywizard-conservation",
        description="EnzyWizard-Conservation: Calculate residue sequence conservation from a cleaned protein sequence, a user-provided multiple sequence alignment (MSA), and generate a detailed JSON report."
    )
    add_conservation_parser(parser)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)