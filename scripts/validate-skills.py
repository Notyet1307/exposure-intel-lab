#!/usr/bin/env python3
"""Retired shared runtime template validator."""

import sys


def main() -> int:
    print(
        "validate-skills.py is retired: shared skill templates live in "
        "Notyet1307/codex-multica and live Multica workspace configuration. "
        "Run scripts/validate-project-governance.py for product repo governance."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
