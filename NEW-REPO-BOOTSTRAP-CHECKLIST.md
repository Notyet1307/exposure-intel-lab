# New Repo Bootstrap Checklist

Use this checklist to maintain the Codex + Multica + GitHub operating model in
exposure-intel-lab. This bootstrap is governance setup only.

Do not create product runtime code, active scanning logic, probing logic,
exploitation tooling, credential testing, or real internet target interaction as
part of this bootstrap.

## 1. Confirm Scope

- [x] Product is `exposure-intel-lab`.
- [x] Repository is `exposure-intel-lab`.
- [x] Multica is the issue, routing, handoff, and status coordination layer.
- [x] GitHub is the durable code, PR, CI, review, and evidence layer.
- [x] Codex is the implementation, debugging, validation, and PR repair agent.
- [x] Product runtime code is out of scope for this bootstrap.
- [x] Active scanning, probing, exploitation, credential testing, and
      unauthorized target interaction are out of scope.
- [x] Future API ingestion must use authorized data sources only.
- [x] PI-agent, OctoBus, agent-compose, and containerization are future issues.

## 2. Copy Governance Files

- [x] Copy `AGENTS.md`.
- [x] Copy `Makefile`.
- [x] Copy `NEW-REPO-BOOTSTRAP-CHECKLIST.md`.
- [x] Copy `.agents/skills/`.
- [x] Copy `.github/ISSUE_TEMPLATE/`.
- [x] Copy `.github/codex/prompts/`.
- [x] Copy `.github/scripts/deepseek_pr_review.py`.
- [x] Copy `.github/workflows/ci.yml`.
- [x] Copy `.github/workflows/codeql.yml`.
- [x] Copy `.github/workflows/deepseek-pr-review.yml`.
- [x] Copy `.github/pull_request_template.md`.
- [x] Copy `docs/agents/`.
- [x] Copy `multica/`.
- [x] Copy `scripts/`.

## 3. Adapt Repository-Specific Files

- [x] Update `AGENTS.md` for exposure-intel-lab.
- [x] Keep `make verify` as the standard local and CI verification entrypoint.
- [x] Update `.github/workflows/ci.yml` so the readiness job runs
      `make verify`.
- [x] Keep DeepSeek PR review configured without storing secrets in the repo.
- [x] Keep CodeQL configured for Python helper scripts.
- [x] Keep human final merge; do not enable automatic merge.
- [x] Do not change Multica workspace runtime directly from the bootstrap PR.

## 4. Configure GitHub

- [ ] Add `DEEPSEEK_API_KEY` as a GitHub Actions secret before relying on the
      DeepSeek PR review workflow.
- [ ] Open the bootstrap PR with the Multica issue ID in the branch, title, or
      PR body.
- [ ] Include summary, validation, risk, rollback, and security notes in the PR
      body.
- [ ] Wait for the `readiness`, DeepSeek `review`, and CodeQL checks.
- [ ] Have a human review and merge the PR.

## 5. Configure Multica

- [ ] Confirm the Multica project is connected to the GitHub repository.
- [ ] Reuse existing workspace skills where possible, including:
  - `spec-first-intake`
  - `tdd-vertical-slice`
  - `systematic-debugging`
  - `verification-before-completion`
  - `security-pr-review`
  - `context-pack`
- [ ] Reuse the `OpenAI-*` workspace agents described in `multica/agents.yaml`.
- [ ] Route security-sensitive work to `OpenAI-security-reviewer`.

## 6. Open the First Bootstrap PR

- [ ] Create a branch that includes the Multica issue ID.
- [ ] Run `make verify` locally.
- [ ] Open the PR.
- [ ] Confirm the PR links to the Multica issue.
- [ ] Include a handoff with changed files, validation, scope check, risks, PR
      URL, and a visible `## Context pack` section.
- [ ] Close the Multica issue only after merge and acceptance criteria are met.
