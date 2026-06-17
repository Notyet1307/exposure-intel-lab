# exposure-intel-lab Roadmap

## Purpose

This roadmap defines how `exposure-intel-lab` moves from governance bootstrap to
a deliverable exposure intelligence runtime.

Codex, Multica, and GitHub are development governance tools. They are not part
of the final delivery runtime. The delivered runtime must be able to run without
Codex, Multica, GitHub, or GitHub Actions.

## Operating Principles

- Fixture-first: prove data contracts, normalization, comparison, reports, and
  audit output with synthetic fixtures before any real source is connected.
- Runtime-later: do not add product runtime code until the roadmap phase
  explicitly allows it.
- Authorization-gated: no real API source may be connected without a reviewed
  authorization and source-definition issue.
- No active interaction: the system processes authorized source data only. It
  must not scan, crawl, probe, exploit, fingerprint, credential-test, or
  interact with unauthorized targets.
- Evidence-first: every runtime behavior must be testable and reproducible from
  inputs, outputs, reports, audit manifests, and validation commands.
- Delivery independence: customer or operator environments must not require
  Codex, Multica, GitHub, GitHub Actions, or repository issue state to run the
  delivered runtime.

## Current Status

Completed:

- Governance bootstrap is complete.
- `make verify` is the repository verification entrypoint for development.
- CI, CodeQL, and DeepSeek review are configured for GitHub PR validation.
- The architecture and safety boundaries are documented.
- Synthetic exposure fixtures and fixture validation are available.
- Exposure data contracts are documented and fixture validation is hardened.

Not yet started:

- Product runtime code.
- Normalization and comparison engine.
- Report generation.
- Delivery packaging.
- PI-agent integration.
- OctoBus integration.
- agent-compose integration.
- Apple container integration.
- Real authorized API ingestion.

## Role Boundaries

| Layer | Role | Non-role |
|---|---|---|
| Multica | Development-time project, issue, routing, handoff, and status coordination. | Not part of delivered runtime, not a data source, not a scheduler, and not acceptance evidence by itself. |
| GitHub | Development-time durable code, PR, CI, review, and evidence layer. | Not required in customer runtime, not the business scheduler, and not the source authorization system. |
| Codex | Development-time implementation, debugging, validation, and PR repair agent. | Not final merge authority, not a runtime dependency, not a credential custodian, and not an autonomous scanner. |
| Product runtime | Deterministic CLI or library that validates inputs, normalizes observations, compares snapshots, generates reports, and writes audit evidence. | Not a scanner, crawler, exploit tool, credential tester, or unauthorized target interaction system. |
| Capability gateway | Future optional wrapper around explicitly authorized APIs or tools. | Not an authorization bypass, not the core data model, and not the evidence truth. |
| Runner or scheduler | Future optional runner for repeatable runtime execution. | Not acceptance evidence, not task truth, and not the product brain. |
| Delivery layer | Installable package, container image, configuration, operations docs, and offline or inner-network runbook. | Not dependent on Codex, Multica, or GitHub Actions. |

## Issue Requirements

Every implementation issue should include:

- Roadmap phase.
- Source roadmap: `docs/roadmap.md`.
- What the issue advances.
- What the issue explicitly does not advance.
- Allowed files or allowed areas.
- Validation commands.
- Stop conditions.
- Whether product runtime code is allowed.

Suggested issue section:

```text
Roadmap
- Phase:
- Source: docs/roadmap.md
- Advances:
- Does not advance:
- Product runtime code allowed: yes/no
```

## Phase R0: Governance Bootstrap

Status: complete.

Goal:

- Establish Codex + Multica + GitHub development governance for the repository.

Done when:

- `AGENTS.md` exists and describes repository rules.
- `make verify` works.
- CI, CodeQL, and DeepSeek review are configured.
- Human final merge is required.
- Visible context-pack handoff rules are available.
- Repository safety boundaries are documented.

Non-goals:

- Product runtime code.
- Real data ingestion.
- PI-agent, OctoBus, agent-compose, or Apple container integration.

## Phase R1: Architecture and Safety Boundaries

Status: complete.

Goal:

- Define the exposure intelligence workflow architecture before implementation.

Done when:

- Component roles and non-roles are documented.
- Multica, GitHub, and Codex are limited to development governance.
- PI-agent, OctoBus, and agent-compose are future candidates only.
- Active scanning, probing, crawling, exploitation, fingerprinting, credential
  testing, unauthorized target interaction, and real exposure data ingestion are
  explicitly out of scope.

Non-goals:

- Runtime implementation.
- Source adapter implementation.
- Real API access.

## Phase R2: Fixture-First Data Surface

Status: complete.

Goal:

- Define synthetic source observation fixtures and validate that they are safe to
  use for future parser, normalizer, and comparison work.

Done when:

- Synthetic fixtures exist under `fixtures/exposure/`.
- Fixture documentation explains source observation shape and safety
  constraints.
- Fixture validation rejects real-looking targets outside approved example
  domains and documentation IP ranges.
- Fixture validation runs through `make verify`.
- Fixtures cover added, removed, changed, and unchanged comparison cases.

Non-goals:

- Runtime source adapters.
- Network calls.
- Real source observations.
- Product runtime package or CLI.

## Phase R3: Data Contracts and Validator Hardening

Status: complete.

Goal:

- Stabilize the source observation, normalized record, comparison report, and
  audit manifest contracts before runtime implementation.

Expected outputs:

- Source observation contract.
- Normalized exposure record contract.
- Comparison report contract.
- Audit manifest contract.
- Stronger fixture validation for status values, confidence values, timestamp
  order, asset and payload consistency, and secret-like values.

Done when:

- Contracts are documented.
- Existing synthetic fixtures pass the stronger validator.
- Invalid fixtures fail with clear errors.
- No third-party dependency is required unless explicitly approved.

Evidence:

- Source observation, normalized exposure record, comparison report, and audit
  manifest contracts are documented in
  `docs/contracts/exposure-data-contracts.md`.
- The exposure fixture validator enforces allowed source status and confidence
  values, chronological snapshot order, observed asset and payload consistency,
  required comparison coverage, synthetic-only host data, and secret-like field
  and value rejection.
- `make verify` runs the exposure fixture validator, and the current synthetic
  fixtures under `fixtures/exposure/` pass it without adding dependencies.

Non-goals:

- Real API schemas.
- Vendor-specific adapter fields.
- Runtime CLI packaging.
- Network access.

## Phase R4: Runtime Entry Gate

Status: planned.

Goal:

- Explicitly decide that the repository is entering product runtime
  implementation.

Done when:

- `AGENTS.md` is updated to allow product runtime code for approved roadmap
  phases.
- The allowed runtime directory layout is documented.
- The runtime remains independent from Codex, Multica, and GitHub Actions.
- Runtime verification commands are defined separately from development PR
  checks.

Required decision:

- Choose the initial runtime shape, likely a deterministic Python CLI or
  library.

Non-goals:

- PI-agent as the base runtime.
- OctoBus as a required runtime dependency.
- agent-compose as a required scheduler.
- Apple container as a required delivery platform.

## Phase R5: Deterministic Runtime MVP

Status: planned.

Goal:

- Build a local deterministic runtime that reads synthetic fixtures and produces
  normalized records, comparison results, reports, and audit evidence.

Expected outputs:

- Runtime package or source module.
- CLI entrypoint.
- Parser for synthetic source observations.
- Normalizer to stable exposure records.
- Comparison engine for added, removed, changed, and unchanged records.
- JSON and/or Markdown report output.
- Audit manifest with input hash, output hash, runtime version, command, and
  validation status.
- Unit and contract tests.

Done when:

- Runtime runs locally without network access.
- Same input produces deterministic output.
- All four comparison cases are tested.
- Runtime tests are included in `make verify`.
- Runtime can also be tested without GitHub Actions.

Non-goals:

- LLM agent integration.
- External API calls.
- chaitin-cli calls.
- PI-agent, OctoBus, or agent-compose integration.
- Real credentials or customer data.

## Phase R6: Report and Evidence Packaging

Status: planned.

Goal:

- Make runtime outputs reviewable and suitable for operator handoff.

Expected outputs:

- Stable report format.
- Machine-readable JSON output.
- Human-readable Markdown report.
- Audit manifest.
- Example outputs generated from synthetic fixtures.
- Documentation explaining how to review outputs.

Done when:

- Reports are deterministic.
- Reports include limitations and skipped fields.
- Reports do not contain secrets or real target data.
- Audit evidence is enough to reproduce the run from local inputs.

Non-goals:

- Dashboard UI.
- PDF or HTML export unless separately approved.
- Real source ingestion.

## Phase R7: Delivery Packaging

Status: planned.

Goal:

- Make the runtime installable and runnable outside the development governance
  environment.

Expected outputs:

- Packaging decision.
- Local install and run instructions.
- Example configuration.
- Offline or inner-network run notes.
- Optional OCI image design if needed.
- Operations guide.

Done when:

- Runtime can run without Codex, Multica, GitHub, or GitHub Actions.
- Inputs and outputs are explicit local paths.
- Logs and reports avoid secrets.
- Container, if added, runs as non-root and uses explicit input and output
  mounts.

Non-goals:

- Requiring GitHub runner in customer environment.
- Requiring Codex in customer environment.
- Requiring Multica in customer environment.
- Making Apple container the only supported runtime.

## Phase R8: Authorized Source Adapter Design

Status: planned.

Goal:

- Design how real authorized data sources may be connected later.

Expected outputs:

- Source definition document.
- Credential handling design.
- Rate limit and retry policy.
- Retention and redaction policy.
- Adapter interface.
- Mock adapter tests.

Done when:

- Missing or expired authorization fails closed before any external request.
- Credentials never enter repo, logs, reports, issue text, or PR descriptions.
- Adapter behavior is tested with mock data.
- Security review is required before live source access.

Non-goals:

- Live API calls.
- Real credentials.
- Mutation APIs.
- Active scanning or target interaction.

## Phase R9: Controlled Authorized API Pilot

Status: planned and gated.

Goal:

- Connect one explicitly authorized read-only source after human approval.

Preconditions:

- Phase R8 is complete.
- Human-approved source definition exists.
- Credential handling is reviewed.
- Security review approves the pilot.
- Live output location is ignored by git.
- Report redaction is validated.

Done when:

- Only allowlisted endpoints are called.
- Only read-only credentials are used.
- Requests respect rate limits.
- Outputs are stored outside tracked fixtures unless synthetic.
- Reports are redacted by default.
- Rollback and credential revocation are documented.

Non-goals:

- Scanning.
- Probing.
- Exploitation.
- Credential testing.
- Mutation APIs.
- Expanding source scope without a new issue.

## Phase R10: Optional Capability Gateway Evaluation

Status: planned and optional.

Goal:

- Evaluate whether OctoBus or a similar gateway adds value for authorized source
  access.

Done when:

- Evaluation uses mock or explicitly authorized local capabilities.
- Gateway access is scoped and audited.
- The product runtime does not depend on the gateway unless separately
  approved.
- Gateway success is not treated as acceptance evidence.

Non-goals:

- Replacing source authorization.
- Storing credentials in gateway config without review.
- Making OctoBus mandatory for MVP.

## Phase R11: Optional Runner/Scheduler Evaluation

Status: planned and optional.

Goal:

- Evaluate scheduled or repeatable execution after the runtime is deterministic
  and auditable.

Done when:

- Runner calls the runtime CLI.
- Each run has run id, exit code, logs, report path, and audit manifest.
- Runner failure does not corrupt inputs or previous outputs.
- GitHub or local evidence remains the reviewable truth.

Non-goals:

- Making agent-compose mandatory for MVP.
- Treating runner success as acceptance evidence.
- Giving scheduler uncontrolled credential access.

## Phase R12: Optional Agent Assistance Evaluation

Status: planned and optional.

Goal:

- Evaluate PI-agent or another local agent runtime as an operator assistant only
  after deterministic runtime behavior exists.

Done when:

- Agent assistance is optional.
- Agent output is clearly separated from deterministic runtime output.
- Agent has no autonomous scanning, credential, or mutation authority.
- Human review remains required for decisions.

Non-goals:

- Using PI-agent as the base runtime.
- Making agent output the source of truth.
- Allowing autonomous target interaction.

## Hard Gates

The following require explicit human approval and a dedicated issue:

- Adding product runtime code before Phase R4.
- Adding third-party runtime dependencies.
- Accessing any real API source.
- Handling credentials, tokens, cookies, or customer data.
- Adding network calls.
- Adding PI-agent, OctoBus, agent-compose, or Apple container integration.
- Adding active scanning, crawling, probing, exploitation, fingerprinting, or
  credential-testing behavior.
- Changing GitHub workflow permissions.
- Changing delivery assumptions.

## Current Recommended Next Issues

1. Harden fixture contracts and validators.
2. Add the runtime entry gate decision.
3. Implement deterministic fixture parser and normalized record contract.
4. Implement fixture comparison MVP.
5. Generate deterministic JSON or Markdown reports and audit manifests.
