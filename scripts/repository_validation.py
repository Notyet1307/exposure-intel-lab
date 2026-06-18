#!/usr/bin/env python3
"""Lightweight structural validation for the exposure-intel-lab governance repository."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Iterable


OUTPUT_EXPECTATION_PATTERN = re.compile(r"\b(return|output|respond|response|format)\b", re.IGNORECASE)
DISABLED_REASON_PATTERN = re.compile(r"\b(disabled|parked|restore|enable|re-enable|reenable)\b", re.IGNORECASE)


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def validate_project_governance(root: Path) -> list[str]:
    errors: list[str] = []

    required_files = (
        "AGENTS.md",
        "Makefile",
        "README.md",
        "NEW-REPO-BOOTSTRAP-CHECKLIST.md",
        "docs/agents/domain.md",
        "docs/agents/code-review.md",
        "docs/agents/security-review.md",
        "docs/agents/issue-tracker.md",
        "docs/agents/pr-guidelines.md",
        "docs/agents/triage-labels.md",
        "docs/architecture/exposure-intelligence-workflow.md",
        "docs/contracts/exposure-data-contracts.md",
        "docs/fixtures/exposure-fixtures.md",
        "docs/roadmap.md",
        "fixtures/exposure/synthetic-source-observations.json",
        "multica/issue-template.md",
        ".github/ISSUE_TEMPLATE/bug.yml",
        ".github/ISSUE_TEMPLATE/feature.yml",
        ".github/ISSUE_TEMPLATE/security-review.yml",
        ".github/codex/prompts/review.md",
        ".github/pull_request_template.md",
        ".github/scripts/deepseek_pr_review.py",
        ".github/workflows/ci.yml",
        ".github/workflows/codeql.yml",
        ".github/workflows/deepseek-pr-review.yml",
        "scripts/check-agent-ready.sh",
        "scripts/validate-exposure-fixtures.py",
    )
    for file_path in required_files:
        if not (root / file_path).is_file():
            errors.append(f"{file_path} is missing")

    required_fragments = {
        "AGENTS.md": (
            "Product: exposure-intel-lab",
            "Repository: exposure-intel-lab",
            "This bootstrap does not add product runtime code.",
            "Notyet1307/codex-multica",
            "Active scanning, crawling, probing, exploitation, fingerprinting, credential testing, or unauthorized internet target interaction is out of scope.",
        ),
        "Makefile": (
            "validate-project-governance.py",
            "validate-exposure-fixtures.py",
        ),
        "multica/issue-template.md": (
            "Active scanning/probing/credential testing touched: yes/no",
            "Real target or real exposure data interaction touched: yes/no",
            "The work requires real API credentials.",
        ),
        "docs/agents/domain.md": (
            "Authorized data source",
            "Active scanning",
            "Notyet1307/codex-multica",
        ),
        "NEW-REPO-BOOTSTRAP-CHECKLIST.md": (
            "Notyet1307/codex-multica",
            "Keep `multica/issue-template.md`",
        ),
        ".github/workflows/ci.yml": ("make verify",),
        ".github/pull_request_template.md": ("Multica",),
        ".github/codex/prompts/review.md": ("Return Markdown",),
        "docs/roadmap.md": (
            "Product runtime code",
            "No active interaction",
        ),
        "docs/contracts/exposure-data-contracts.md": ("synthetic data surface",),
        "docs/fixtures/exposure-fixtures.md": ("synthetic",),
    }
    for file_path, fragments in required_fragments.items():
        path = root / file_path
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for fragment in fragments:
            if fragment not in text:
                errors.append(f"{file_path} missing required governance fragment {fragment}")

    forbidden_fragments = {
        "Makefile": (
            "validate-skills.py",
            "validate-multica-config.py",
        ),
        "AGENTS.md": (
            "python3 scripts/validate-skills.py",
            "python3 scripts/validate-multica-config.py",
        ),
    }
    for file_path, fragments in forbidden_fragments.items():
        path = root / file_path
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for fragment in fragments:
            if fragment in text:
                errors.append(f"{file_path} contains obsolete validation command {fragment}")

    forbidden_paths = (
        ".agents/skills",
        "multica/agent-system-prompts",
        "multica/agents.yaml",
        "multica/squads.yaml",
        "multica/autopilots.yaml",
    )
    for forbidden_path in forbidden_paths:
        if (root / forbidden_path).exists():
            errors.append(f"{forbidden_path} is a shared runtime template copy and should not be present")

    return errors


def validate_prompts(root: Path) -> list[str]:
    errors: list[str] = []
    prompts_dir = root / ".github/codex/prompts"
    if not prompts_dir.is_dir():
        return [".github/codex/prompts is missing"]

    prompt_files = sorted(prompts_dir.glob("*.md"))
    if not prompt_files:
        errors.append(".github/codex/prompts has no prompt files")

    for prompt_path in prompt_files:
        text = prompt_path.read_text(encoding="utf-8")
        path_label = relative(prompt_path, root)
        if not text.strip():
            errors.append(f"{path_label} is empty")
            continue
        if not OUTPUT_EXPECTATION_PATTERN.search(text):
            errors.append(f"{path_label} lacks an output or response expectation")

    return errors


def top_level_yaml_keys(text: str) -> set[str]:
    keys: set[str] = set()
    for line in text.splitlines():
        if line.startswith((" ", "\t")) or not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.match(r"^([A-Za-z_][\w-]*):", line)
        if match:
            keys.add(match.group(1))
    return keys


def workflow_files(root: Path) -> Iterable[Path]:
    workflows_dir = root / ".github/workflows"
    if not workflows_dir.is_dir():
        return []
    patterns = ("*.yml", "*.yaml", "*.yml.disabled", "*.yaml.disabled")
    files: list[Path] = []
    for pattern in patterns:
        files.extend(workflows_dir.glob(pattern))
    return sorted(set(files))


def validate_workflows(root: Path) -> list[str]:
    errors: list[str] = []
    workflows = list(workflow_files(root))
    if not workflows:
        return [".github/workflows has no workflow files"]

    for workflow_path in workflows:
        text = workflow_path.read_text(encoding="utf-8")
        path_label = relative(workflow_path, root)
        keys = top_level_yaml_keys(text)
        for required_key in ("name", "on", "jobs"):
            if required_key not in keys:
                errors.append(f"{path_label} missing top-level {required_key}")

        if workflow_path.name.endswith(".disabled") and not DISABLED_REASON_PATTERN.search(text):
            errors.append(f"{path_label} lacks a documented disabled reason or restore condition")

        if workflow_path.name == "deepseek-pr-review.yml":
            errors.extend(validate_deepseek_workflow_security(path_label, text))

    return errors


def validate_deepseek_workflow_security(path_label: str, text: str) -> list[str]:
    errors: list[str] = []
    required_fragments = (
        "pull_request_target:",
        "contents: read",
        "pull-requests: write",
        "issues: write",
        "uses: actions/checkout@v5",
        "ref: ${{ github.event.pull_request.base.sha }}",
        "path: trusted",
        "persist-credentials: false",
        "working-directory: trusted",
        "$RUNNER_TEMP/pr-truncated.diff",
        "$RUNNER_TEMP/deepseek-review.md",
        ".github/scripts/deepseek_pr_review.py",
        ".github/codex/prompts/review.md",
    )

    for fragment in required_fragments:
        if fragment not in text:
            errors.append(f"{path_label} missing trusted DeepSeek workflow fragment {fragment}")

    forbidden_fragments = (
        "pr-truncated.diff \\\n            .github/codex/prompts/review.md",
        "${{ github.workspace }}/deepseek-review.md",
    )
    for fragment in forbidden_fragments:
        if fragment in text:
            errors.append(f"{path_label} contains unsafe DeepSeek workflow fragment {fragment!r}")

    if "DEEPSEEK_API_KEY" in text and "python3 .github/scripts/deepseek_pr_review.py" in text:
        secret_index = text.index("DEEPSEEK_API_KEY")
        script_index = text.index("python3 .github/scripts/deepseek_pr_review.py")
        trusted_index = text.find("working-directory: trusted", 0, script_index)
        if trusted_index == -1 or trusted_index > secret_index:
            errors.append(f"{path_label} passes DEEPSEEK_API_KEY without trusted working-directory")

    return errors


def validate_readme_paths(root: Path) -> list[str]:
    readme_path = root / "README.md"
    if not readme_path.is_file():
        return []

    readme = readme_path.read_text(encoding="utf-8")
    key_paths = (
        "AGENTS.md",
        ".github/codex/prompts",
        ".github/workflows",
        ".github/pull_request_template.md",
        "docs/agents",
        "docs/contracts",
        "docs/fixtures",
        "fixtures/exposure",
        "multica/issue-template.md",
        "scripts",
    )

    errors: list[str] = []
    for key_path in key_paths:
        if key_path in readme and not (root / key_path).exists():
            errors.append(f"README.md references missing path {key_path}")
    return errors


def run_checks(root: Path, checks: Iterable[tuple[str, callable]]) -> int:
    all_errors: list[str] = []
    for name, check in checks:
        errors = check(root)
        if errors:
            all_errors.extend(f"{name}: {error}" for error in errors)
        else:
            print(f"OK: {name}")

    if all_errors:
        for error in all_errors:
            print(f"ERROR: {error}")
        return 1
    return 0


def main(check_name: str | None = None) -> int:
    root = Path.cwd()
    checks = {
        "project-governance": validate_project_governance,
        "prompts": validate_prompts,
        "workflows": validate_workflows,
        "readme-paths": validate_readme_paths,
    }

    if check_name:
        return run_checks(root, [(check_name, checks[check_name])])
    return run_checks(root, checks.items())


if __name__ == "__main__":
    sys.exit(main())
