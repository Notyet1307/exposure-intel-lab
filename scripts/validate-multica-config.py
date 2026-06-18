#!/usr/bin/env python3
"""Retired shared Multica runtime template validator."""

import sys


def main() -> int:
    print(
        "validate-multica-config.py is retired: shared Multica agents, prompts, "
        "squads, and autopilot templates live in Notyet1307/codex-multica and "
        "live Multica workspace configuration. Run "
        "scripts/validate-project-governance.py for product repo governance."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
