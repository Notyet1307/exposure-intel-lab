# AGENTS.md

## Purpose

This file is the durable operating manual for Codex and other coding agents working in this repository. Follow it unless a human explicitly overrides it in a task, issue, or PR comment.

## Project facts

- Product: exposure-intel-lab
- Repository: exposure-intel-lab
- Primary users: engineers evaluating an authorized exposure intelligence workflow.
- Runtime today: governance files, Markdown, YAML, Bash, Python helper scripts, and GitHub Actions.
- Package manager: none.
- Product runtime: not present in this bootstrap issue.
- Issue tracker: Multica. GitHub PRs must reference Multica issue IDs, for example `MUL-123`.
- Production data classification: none in this repository during governance bootstrap; future data handling must be explicitly authorized before implementation.
- Shared live Multica agents, skills, prompts, squads, and autopilot templates are maintained in `Notyet1307/codex-multica` and live Multica workspace configuration, not in this product repository.

## Current scope

This bootstrap establishes the Codex + Multica + GitHub operating model for exposure-intel-lab.

Repo-owned bootstrap work is limited to project-specific governance, safety, validation, fixture, contract, and review scaffolding:

- `AGENTS.md`
- `Makefile`
- `NEW-REPO-BOOTSTRAP-CHECKLIST.md`
- `.github/`
- `docs/agents/`
- `docs/architecture/`
- `docs/contracts/`
- `docs/fixtures/`
- `docs/roadmap.md`
- `fixtures/exposure/`
- `multica/issue-template.md`
- `scripts/`

This bootstrap does not add product runtime code.

Do not copy shared runtime templates back into this repository without a later explicit Multica issue. Shared skills, agent prompts, desired live agent state, squad design, and autopilot templates belong in `Notyet1307/codex-multica` and live Multica workspace configuration.

## Security and authorization boundaries

Active scanning, crawling, probing, exploitation, fingerprinting, credential testing, or unauthorized internet target interaction is out of scope.

Future API ingestion must use authorized data sources only. Do not ingest real internet exposure data, customer data, credentials, cookies, tokens, secrets, or private target data unless a later issue provides explicit authorization and review requirements.

PI-agent, OctoBus, agent-compose, and containerization are future design topics. Do not install, integrate, or configure them in this bootstrap issue.

Stop and ask a human before proceeding if a task would require:

- real API credentials or secrets
- accessing real internet targets
- active scanning, probing, exploitation, or credential testing
- installing PI-agent, OctoBus, agent-compose, or Apple container
- adding product runtime code
- changing shared workspace skills or agents
- modifying Multica workspace runtime directly

## Repository layout

Current governance layout:

```text
<repo-root>/
├── AGENTS.md
├── Makefile
├── NEW-REPO-BOOTSTRAP-CHECKLIST.md
├── .github/
├── docs/agents/
├── docs/architecture/
├── docs/contracts/
├── docs/fixtures/
├── docs/roadmap.md
├── fixtures/exposure/
├── multica/issue-template.md
└── scripts/
```

Do not create product runtime directories until a later Multica issue explicitly designs and approves them.

## Commands

```bash
# Install dependencies
# No dependency installation is required for governance bootstrap.

# Standard local and CI verification entrypoint
make verify

# Readiness check
bash scripts/check-agent-ready.sh

# Shell syntax check
bash -n scripts/*.sh

# Structural validation
python3 scripts/validate-project-governance.py
python3 scripts/validate-prompts.py
python3 scripts/validate-workflows.py
python3 scripts/validate-readme-paths.py
python3 scripts/validate-exposure-fixtures.py
```

## Language policy

Use English for durable project artifacts:

- issue titles and descriptions
- branch names
- commit messages
- pull request titles and bodies
- agent system prompts
- code comments
- documentation committed to the repository
- GitHub Actions and script output intended for CI logs

Use Chinese when explaining status, decisions, and next steps directly to the human operator in chat.

## Work intake rules

For every task, identify:

1. Goal: what user-visible or operator-visible behavior changes.
2. Context: issue ID, PR, affected files, logs, screenshots, prior decisions.
3. Constraints: compatibility, security, performance, architecture, non-goals.
4. Done when: tests, CI, review, documentation, deployment notes.

If these are missing and the task is small, make explicit assumptions and proceed conservatively. If the task is high risk, ask for clarification before changing code.

## Visible context packs

For non-trivial multi-agent, delegated, resumed, or long-running work, the worker must leave a visible Multica issue comment containing a `## Context pack` section before claiming ready for review.

Hidden execution logs, side-panel state, and implicit chat memory are not durable handoff context. If a future agent is expected to continue the work, the context pack must be written as a normal visible issue comment or included in Handoff Back.

Handoff Back is the detailed evidence report: work performed, changed files, validation, scope check, risks, and readiness. Context pack is the compact resume state: the durable facts a future agent needs to continue without rereading hidden logs or the full thread.

When both are present, do not duplicate the full evidence report inside Context pack. The Context pack may reference Handoff Back and the PR for full validation, changed-file, scope, and risk evidence, while still recording the current goal, status, constraints, next action, and any open questions.

Context pack requirements are proportional to handoff risk. Trivial acknowledgements, single-step answers, and work with no durable follow-up value do not need a context pack.

Private or security-sensitive context must still follow the `context-pack` privacy rules: do not post private security context to workspace-visible channels; redact shared handoff context or stop and ask a human.

## Change rules

- Prefer small, reviewable changes.
- Do not perform unrelated refactors.
- Do not reformat entire files unless the repository formatter requires it.
- Add or update tests or validation for behavior changes where a correct test seam exists.
- Keep generated files out of commits unless they are already tracked or required by the project.
- Never overwrite human work. Before editing, check current diffs if possible.
- Do not modify `.env`, private credentials, production secrets, local auth files, or workspace runtime state.
- Keep `make verify` as the standard local and CI verification entrypoint.

## Agent operating model

- Multica is the project, issue, routing, handoff, and status coordination layer.
- GitHub is the durable code, PR, CI, review, and evidence layer.
- Codex is the implementation, debugging, validation, and PR repair agent.
- Runner success is not acceptance evidence; GitHub checks and documented validation are the evidence layer.
- Humans own product direction, security exceptions, production deployment, and final merge.

## Security baseline

- Never log secrets, tokens, passwords, session cookies, PII, financial data, medical data, or customer confidential content.
- Authentication checks must occur before sensitive actions.
- Authorization must be resource-specific and tenant-aware.
- Validate and normalize untrusted input at trust boundaries.
- Use parameterized database queries or ORM-safe APIs if a later issue introduces data storage.
- Avoid shelling out with untrusted input. If unavoidable, escape arguments and add tests.
- Avoid SSRF by using allowlists for outbound URLs and blocking private/internal IP ranges.
- Avoid path traversal by resolving paths and checking containment.
- Do not introduce new dependencies unless justified in the PR.
- For cryptography, use standard libraries. Do not design custom crypto.
- Treat AI-generated code as untrusted until reviewed and tested.

## Data handling rules

- Do not copy production data into tests.
- Use synthetic fixtures.
- Redact secrets and PII in logs, screenshots, PR descriptions, comments, and issue text.
- Do not store credentials in `custom_env`, committed config, `AGENTS.md`, Skill files, prompts, or issue comments.
- Use short-lived, least-privilege credentials for any future authorized agent runtime.

## Testing strategy

Use the test level that proves behavior with the least brittleness.

Preferred order:

1. Unit tests for pure logic.
2. Integration tests through public interfaces.
3. Contract tests for API compatibility.
4. E2E tests for critical user journeys.
5. Manual verification only when automation is impractical; document exact steps.

Avoid tests that assert implementation details, private method calls, arbitrary mocks, or fragile DOM structure unless that is the public contract.

## TDD mode

When the task is a feature or bug fix and the behavior can be tested:

1. Write one failing test for one vertical slice.
2. Run the test and confirm it fails for the expected reason.
3. Write the minimal implementation.
4. Run the test and related checks.
5. Refactor only after green.
6. Repeat for the next slice.

Do not write all tests first and all implementation after. Use thin vertical slices.

## Debugging mode

For bugs:

1. Build a deterministic reproduction loop.
2. Confirm the reproduced symptom matches the user-reported issue.
3. List 3-5 ranked falsifiable hypotheses.
4. Instrument narrowly; tag temporary logs with `[DEBUG-<id>]`.
5. Fix after the cause is identified.
6. Add a regression test where possible.
7. Remove all debug instrumentation.
8. Record the root cause in the PR.

## Review guidelines

Also read `docs/agents/code-review.md` and `docs/agents/security-review.md` when reviewing.

Focus on blocking issues:

- Incorrect behavior
- Security regression
- Data loss or data exposure
- Broken migration or rollback
- Missing tests for risky change
- Public API compatibility break
- Performance regression on hot path
- Deployment or configuration risk

Do not flood reviews with style comments if formatter/linter covers them.

## Pull request requirements

Every PR must include:

- Multica issue ID in branch, title, or body.
- Summary of changes.
- Validation commands and results.
- Risk assessment.
- Rollback notes if applicable.
- Security notes if auth, data, logging, dependencies, network calls, file upload, or tenancy are touched.
- Confirmation that no active scanning, probing, exploitation, credential testing, or real target interaction was added.

## Definition of done

A task is done only when:

- Acceptance criteria are satisfied.
- Relevant checks pass, especially `make verify`.
- Security-sensitive changes have been reviewed.
- PR links to the Multica issue ID.
- Any user-facing behavior change is documented if needed.
- The agent has left a concise handoff with changed files, validation, scope check, risks, PR URL, and a visible `## Context pack` section when required by handoff risk.

## When to stop and escalate

Stop and ask a human when:

- The task requires production access.
- The task requires customer data.
- The issue conflicts with documented architecture decisions.
- There are multiple reasonable product behaviors.
- A migration may cause data loss.
- Security policy requires exception approval.
- The task requires spending money or provisioning cloud resources.
- The repository lacks enough tests to verify a high-risk change.
- The task crosses the security and authorization boundaries in this file.
