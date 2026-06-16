# Domain Language for Agents

Use this file to keep product and engineering language consistent.

## Glossary

| Term | Meaning | Avoid saying | Notes |
|---|---|---|---|
| exposure-intel-lab | The repository for evaluating an authorized exposure intelligence workflow | scanner, exploit kit | The current repo contains governance scaffolding only. |
| Governance bootstrap | The initial Codex + Multica + GitHub operating model setup | product launch | Bootstrap work must not add runtime behavior. |
| Authorized data source | A source explicitly approved for ingestion by a human owner | internet target | Future ingestion must name the approved source and boundaries. |
| Active scanning | Probing, crawling, fingerprinting, exploitation, credential testing, or real target interaction | passive lookup | Out of scope until a later issue explicitly authorizes it. |
| Multica issue | The source of truth for requested work | GitHub issue as source of truth | GitHub may mirror or link work, but Multica owns intake. |
| Agent | A configured Codex worker in Multica | bot | Agents have bounded roles and must not auto-merge. |
| Squad | A Multica routing group led by `OpenAI-scoper` | team | The squad routes issues to the narrowest competent owner. |
| Handoff Back | Worker summary to the requester before review | status note only | Include changed files, validation, scope check, risks, PR URL, and context pack when requested. |
| Readiness check | `make verify` | full product test suite | Verifies required governance files and automation are usable. |
| PI-agent | Possible future project-local agent runtime | current runtime | Not installed or integrated by this bootstrap. |
| OctoBus | Possible future capability gateway | current gateway | Not installed or integrated by this bootstrap. |
| agent-compose | Possible future runner or scheduler | acceptance evidence | Runner success is not acceptance evidence. |

## Bounded contexts

| Context | Owns | Does not own | Main directories |
|---|---|---|---|
| Agent operating rules | Durable instructions, review policy, safety boundaries | Product runtime code | `AGENTS.md`, `docs/agents/` |
| Multica configuration | Agents, squads, autopilots, issue templates | GitHub Actions execution | `multica/` |
| GitHub automation | CI, PR templates, DeepSeek review, CodeQL | Multica routing policy | `.github/` |
| Repo-scoped skills | Reusable agent workflows bundled with this repo | Workspace skill source of truth | `.agents/skills/` |
| Readiness scripts | Local validation helpers | Full CI simulation | `scripts/` |
| Future product runtime | Authorized ingestion, analysis, storage, UI, integrations | Current bootstrap scope | Not present yet |

## Decision log pointers

ADRs should live in `docs/adr/` if later issues introduce durable architecture decisions. Use short ADRs for decisions future agents may otherwise re-litigate.
