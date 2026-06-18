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

## 2. Keep Project Governance Files

- [x] Keep `AGENTS.md`.
- [x] Keep `Makefile`.
- [x] Keep `NEW-REPO-BOOTSTRAP-CHECKLIST.md`.
- [x] Keep `.github/ISSUE_TEMPLATE/`.
- [x] Keep `.github/codex/prompts/`.
- [x] Keep `.github/scripts/deepseek_pr_review.py`.
- [x] Keep `.github/workflows/ci.yml`.
- [x] Keep `.github/workflows/codeql.yml`.
- [x] Keep `.github/workflows/deepseek-pr-review.yml`.
- [x] Keep `.github/pull_request_template.md`.
- [x] Keep `docs/agents/`, `docs/architecture/`, `docs/contracts/`,
      `docs/fixtures/`, and `docs/roadmap.md`.
- [x] Keep `fixtures/exposure/`.
- [x] Keep `multica/issue-template.md` because it contains
      exposure-specific safety fields and stop conditions.
- [x] Keep `scripts/`.

Historical bootstrap copies included shared runtime templates in this product
repo. Current policy is to keep only project-specific governance here and use
`Notyet1307/codex-multica` plus live Multica workspace configuration as the
source of truth for shared agents, skills, prompts, squads, and autopilot
templates.

Do not copy `.agents/skills/`, `multica/agent-system-prompts/`,
`multica/agents.yaml`, `multica/squads.yaml`, or `multica/autopilots.yaml` back
into this repo unless a later Multica issue explicitly approves that scope.

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
- [ ] Reuse existing workspace skills from `Notyet1307/codex-multica` and live
      Multica workspace configuration where possible, including:
  - `spec-first-intake`
  - `tdd-vertical-slice`
  - `systematic-debugging`
  - `verification-before-completion`
  - `security-pr-review`
  - `context-pack`
- [ ] Reuse the `OpenAI-*` workspace agents maintained in
      `Notyet1307/codex-multica` and live Multica workspace configuration.
- [ ] Route security-sensitive work to `OpenAI-security-reviewer`.

## 6. Open the First Bootstrap PR

- [ ] Create a branch that includes the Multica issue ID.
- [ ] Run `make verify` locally.
- [ ] Open the PR.
- [ ] Confirm the PR links to the Multica issue.
- [ ] Include a handoff with changed files, validation, scope check, risks, PR
      URL, and a visible `## Context pack` section.
- [ ] Close the Multica issue only after merge and acceptance criteria are met.
