.PHONY: verify

verify:
	bash scripts/check-agent-ready.sh
	bash -n scripts/*.sh
	PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate-skills.py
	PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate-multica-config.py
	PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate-prompts.py
	PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate-workflows.py
	PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate-exposure-fixtures.py
