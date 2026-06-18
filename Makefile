.PHONY: verify

verify:
	bash scripts/check-agent-ready.sh
	bash -n scripts/*.sh
	PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate-project-governance.py
	PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate-prompts.py
	PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate-workflows.py
	PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate-readme-paths.py
	PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate-exposure-fixtures.py
