#!/usr/bin/env bash
set -euo pipefail

missing=0

require_file() {
  if [ ! -f "$1" ]; then
    echo "MISSING: $1"
    missing=1
  else
    echo "OK: $1"
  fi
}

require_contains() {
  if ! grep -Fq "$2" "$1"; then
    echo "MISSING: $1 does not contain $2"
    missing=1
  else
    echo "OK: $1 contains $2"
  fi
}

require_not_contains() {
  if grep -Fq "$2" "$1"; then
    echo "UNEXPECTED: $1 contains $2"
    missing=1
  else
    echo "OK: $1 does not contain $2"
  fi
}

require_file AGENTS.md
require_file Makefile
require_file NEW-REPO-BOOTSTRAP-CHECKLIST.md
require_file docs/agents/domain.md
require_file docs/agents/code-review.md
require_file docs/agents/security-review.md
require_file docs/agents/issue-tracker.md
require_file .github/pull_request_template.md
require_file .github/codex/prompts/review.md
require_file .github/scripts/deepseek_pr_review.py
require_file .github/workflows/ci.yml
require_file .github/workflows/deepseek-pr-review.yml
require_file .github/workflows/codeql.yml

require_contains AGENTS.md "Product: exposure-intel-lab"
require_contains AGENTS.md "Repository: exposure-intel-lab"
require_contains AGENTS.md "This bootstrap does not add product runtime code."
require_contains AGENTS.md "Active scanning, crawling, probing, exploitation, fingerprinting, credential testing, or unauthorized internet target interaction is out of scope."
require_contains AGENTS.md "Future API ingestion must use authorized data sources only."
require_contains AGENTS.md "PI-agent, OctoBus, agent-compose, and containerization are future design topics."
require_contains AGENTS.md "make verify"
require_contains NEW-REPO-BOOTSTRAP-CHECKLIST.md "Future API ingestion must use authorized data sources only."
require_contains docs/agents/domain.md "Authorized data source"
require_contains docs/agents/domain.md "Active scanning"
require_contains .github/workflows/ci.yml "make verify"
require_contains .github/workflows/codeql.yml "language: ['python']"
require_not_contains .github/workflows/codeql.yml "language: ['javascript-typescript']"
require_contains .github/workflows/deepseek-pr-review.yml "pull_request_target:"
require_contains .github/workflows/deepseek-pr-review.yml "pull-requests: write"
require_contains .github/workflows/deepseek-pr-review.yml "ref: \${{ github.event.pull_request.base.sha }}"
require_contains .github/workflows/deepseek-pr-review.yml "path: trusted"
require_contains .github/workflows/deepseek-pr-review.yml "persist-credentials: false"
require_contains .github/workflows/deepseek-pr-review.yml "working-directory: trusted"
require_contains .github/workflows/deepseek-pr-review.yml "\$RUNNER_TEMP/pr-truncated.diff"
require_contains .github/workflows/deepseek-pr-review.yml "\$RUNNER_TEMP/deepseek-review.md"
require_contains .github/workflows/deepseek-pr-review.yml "steps.deepseek_review.outputs.exit_code != '0'"
require_not_contains .github/workflows/deepseek-pr-review.yml "continue-on-error: true"
require_not_contains .github/workflows/deepseek-pr-review.yml "hashFiles('deepseek-review.md')"
require_contains .github/workflows/deepseek-pr-review.yml "exit 0"
require_contains .github/workflows/deepseek-pr-review.yml "always() && steps.deepseek_review.outputs.exit_code != '0'"

python3 .github/scripts/deepseek_pr_review.py --self-test

if [ -d .agents/skills ]; then
  find .agents/skills -mindepth 2 -maxdepth 2 -name SKILL.md -print | sort
else
  echo "MISSING: .agents/skills"
  missing=1
fi

if [ "$missing" -ne 0 ]; then
  echo "Agent readiness check failed."
  exit 1
fi

echo "Agent readiness check passed."
