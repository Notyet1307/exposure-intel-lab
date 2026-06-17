# exposure-intel-lab

`exposure-intel-lab` is a governance-first repository for evaluating an
authorized exposure intelligence workflow. The repository currently defines the
Codex, Multica, and GitHub operating model that future implementation work will
use.

## Current phase

This repository is in governance and bootstrap validation. The current contents
are limited to agent instructions, project coordination files, validation
scripts, and GitHub review workflows.

No active scanning, crawling, probing, exploitation, fingerprinting, credential
testing, real target interaction, or real exposure data ingestion is implemented
in this phase.

Future ingestion or analysis work must use authorized data sources only and must
be introduced through reviewed Multica issues and GitHub pull requests.

## Agent workflow

- [AGENTS.md](AGENTS.md) is the durable operating manual for coding agents in
  this repository.
- [NEW-REPO-BOOTSTRAP-CHECKLIST.md](NEW-REPO-BOOTSTRAP-CHECKLIST.md) tracks the
  bootstrap checklist for this repository's Multica, Codex, and GitHub workflow.
- [docs/architecture/exposure-intelligence-workflow.md](docs/architecture/exposure-intelligence-workflow.md)
  defines the target authorized exposure intelligence workflow architecture and
  safety boundaries.

## Verification

Use the standard repository verification entrypoint:

```bash
make verify
```
