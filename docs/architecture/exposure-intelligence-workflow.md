# Exposure Intelligence Workflow Architecture

## Purpose

This document defines the target operating architecture for an authorized
exposure intelligence workflow in `exposure-intel-lab`. It is a planning
document only. It does not add runtime integrations, credentials, live ingestion,
active scanning, probing, exploitation, fingerprinting, crawling, credential
testing, or real target interaction.

The initial implementation path should remain fixture-first: future code should
prove normalization, comparison, reporting, and evidence capture with synthetic
fixtures before any authorized source is connected.

## Operating truths

- Multica is the coordination truth for project intake, issue routing, handoff,
  status, and ownership.
- GitHub is the evidence truth for durable code, pull requests, review, CI, and
  validation artifacts.
- Codex agents may implement, debug, validate, and repair pull requests within
  the scope of a reviewed Multica issue.
- Runner success is not acceptance evidence. A future PI-agent or agent-compose
  run may produce useful execution logs, but GitHub checks and documented
  validation remain the evidence layer.
- Humans own product direction, security exceptions, production deployment, and
  final merge decisions.

## Component roles

| Component | Role | Non-role |
|---|---|---|
| Multica | Project, issue, routing, handoff, and status coordination. It records requested work, owners, constraints, and handoff context. | Not the durable code store, CI system, merge gate, data source, scanner, or runtime for exposure ingestion. |
| GitHub | Durable code, pull request, CI, review, and evidence layer. It stores repository history and validation evidence. | Not the issue source of truth and not a replacement for Multica routing or handoff state. |
| Codex | Implementation, debugging, validation, and PR repair agent operating under Multica issue scope and repository instructions. | Not a product owner, final merge authority, credential custodian, or autonomous scanner. |
| PI-agent | Candidate local agent runtime for future controlled execution experiments. | Not the task truth source, merge gate, credential broker, or acceptance evidence. It is not installed or integrated in this phase. |
| OctoBus | Candidate capability gateway for explicitly authorized APIs and bounded future capability access. | Not a bypass around source authorization, credential handling rules, or GitHub review evidence. It is not installed or integrated in this phase. |
| agent-compose | Candidate runner or scheduler for future repeatable jobs. | Not acceptance evidence, not an issue tracker, and not a source of truth for status. It is not installed or integrated in this phase. |

## Trust boundaries

The initial workflow has three conceptual trust boundaries:

1. **Authorization boundary:** a human-approved data source definition must exist
   before any future ingestion work can access external data. The source must
   name allowed APIs, scopes, data classes, rate limits, and prohibited targets.
2. **Normalization boundary:** raw authorized source responses must be converted
   into repository-defined normalized records before comparison. Normalization
   should reject unexpected shapes and redact or exclude disallowed fields.
3. **Evidence boundary:** comparison results must become reviewable artifacts in
   GitHub through tests, generated reports, or PR-attached evidence. Multica
   handoff comments may summarize evidence, but they should reference GitHub or
   repository artifacts rather than replacing them.

Credentials, secrets, cookies, tokens, customer data, private target data, and
production data must not cross into committed fixtures, logs, issue comments, PR
descriptions, or generated documentation.

## Initial data flow

The first runtime design should follow this fixture-first flow:

```text
Synthetic authorized-source fixture
  -> source adapter contract
  -> normalized exposure records
  -> comparison engine
  -> comparison report
  -> GitHub validation and review evidence
  -> Multica handoff summary and status coordination
```

A later authorized integration may replace the fixture input with a real approved
API source only after a separate issue defines the source, approval, credentials
handling, data classes, rate limits, and review requirements.

## Conceptual input contracts

### Authorized source definition

An authorized source definition should describe:

- source name and owner
- explicit authorization record or approval reference
- allowed API endpoints or capability names
- allowed tenant, account, organization, or asset scope
- data classes expected from the source
- fields that must be redacted, ignored, or never requested
- rate limits and retry boundaries
- retention and deletion expectations
- validation evidence required before use

### Source observation

A source observation is the raw or near-raw response from an authorized source.
Future implementation should treat observations as untrusted input and normalize
them before comparison. Observations should include:

- source identifier
- collection timestamp
- authorization scope reference
- source-native record identifier
- source-native record payload, limited to approved fields
- source-native confidence or status when available

Real observations are out of scope for this phase. Initial examples must be
synthetic fixtures.

### Normalized exposure record

A normalized exposure record should be stable across source types and contain:

- normalized record identifier
- source identifier and source-native reference
- observed asset or service label, scoped to authorized data
- exposure category
- normalized status
- first and last observed timestamps when available
- source confidence or evidence summary
- redaction status for any omitted fields

The normalized record must not imply that the system performed active scanning
or target interaction. It should only represent data returned by an authorized
source.

## Conceptual output contracts

### Comparison report

A comparison report should summarize differences across two or more authorized
snapshots or fixture sets. It should include:

- report identifier
- input snapshot references
- generated timestamp
- added, removed, changed, and unchanged record counts
- record-level deltas with normalized identifiers
- confidence or evidence notes
- validation status
- limitations and skipped fields

### Evidence artifact

An evidence artifact should be reviewable through GitHub. Depending on the later
implementation, it may be a test result, generated Markdown report, JSON fixture
comparison output, or CI artifact. It should include enough context for a
reviewer to confirm the comparison without relying on runner logs alone.

## Safety boundaries

The following remain out of scope until a later issue explicitly authorizes and
reviews them:

- active scanning
- crawling
- probing
- exploitation
- fingerprinting
- credential testing
- unauthorized target interaction
- real internet exposure data ingestion
- customer data ingestion
- credentials, secrets, tokens, cookies, or private target data
- PI-agent installation or integration
- OctoBus installation or integration
- agent-compose installation or integration
- product runtime directories or workflow changes

Future work must fail closed when source authorization is missing, ambiguous, or
expired. Missing authorization should stop ingestion before any external request
is made.

## Future fixture-first implementation path

1. Add synthetic fixtures that model approved source observations without real
   target data.
2. Define parser and normalizer contracts against those fixtures.
3. Add comparison tests that produce deterministic added, removed, changed, and
   unchanged records.
4. Generate a small comparison report from fixtures.
5. Validate the report through `make verify` or a later reviewed CI check.
6. Only after human approval, design an authorized API source adapter in a new
   issue with explicit credential handling and security review requirements.

Each step should preserve Multica as coordination truth and GitHub as evidence
truth.
