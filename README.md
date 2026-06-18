# exposure-intel-lab

`exposure-intel-lab` is a governance-first repository for evaluating an
authorized exposure intelligence workflow. The repository currently defines the
Codex, Multica, and GitHub operating model that future implementation work will
use, plus synthetic exposure fixtures for fixture-first validation.

## Current phase

This repository is in governance and bootstrap validation. The current contents
are limited to agent instructions, project coordination files, validation
scripts, and GitHub review workflows.

No active scanning, crawling, probing, exploitation, fingerprinting, credential
testing, real target interaction, or real exposure data ingestion is implemented
in this phase.

Future ingestion or analysis work must use authorized data sources only and must
be introduced through reviewed Multica issues and GitHub pull requests.

## Synthetic exposure fixtures

Synthetic source observation fixtures live in
[`fixtures/exposure/`](fixtures/exposure/). They use only example domains and
documentation IP ranges so future normalization and comparison work can be built
without real targets, external APIs, credentials, customer data, or runtime
integrations.

See [`docs/fixtures/exposure-fixtures.md`](docs/fixtures/exposure-fixtures.md)
for the fixture shape and safety constraints.

## Agent workflow

- [AGENTS.md](AGENTS.md) is the durable operating manual for coding agents in
  this repository.
- [NEW-REPO-BOOTSTRAP-CHECKLIST.md](NEW-REPO-BOOTSTRAP-CHECKLIST.md) tracks the
  bootstrap checklist for this repository's Multica, Codex, and GitHub workflow.
- Shared live Multica agents, skills, prompts, squads, and autopilot templates
  are maintained in `Notyet1307/codex-multica` and live Multica workspace
  configuration, not in this product repository.
- [docs/architecture/exposure-intelligence-workflow.md](docs/architecture/exposure-intelligence-workflow.md)
  defines the target authorized exposure intelligence workflow architecture and
  safety boundaries.
- [docs/roadmap.md](docs/roadmap.md) defines the project phases, hard gates,
  delivery boundaries, and roadmap metadata expected in future issues.

## Verification

Use the standard repository verification entrypoint:

```bash
make verify
```

To run only the exposure fixture validator:

```bash
python3 scripts/validate-exposure-fixtures.py
```
