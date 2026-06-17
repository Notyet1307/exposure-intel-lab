# Exposure Fixtures

The files under `fixtures/exposure/` are synthetic source observation fixtures
for the future authorized exposure intelligence workflow. They define the input
shape that later normalization and comparison code can use before any real API,
PI-agent, OctoBus, or agent-compose integration exists.

The broader conceptual contracts for source observations, normalized exposure
records, comparison reports, and audit manifests are documented in
`docs/contracts/exposure-data-contracts.md`.

These fixtures are not scan results and do not represent real internet targets.
They use only reserved example domains and documentation IP address ranges:

- `.example`
- `.invalid`
- `192.0.2.0/24`
- `198.51.100.0/24`
- `203.0.113.0/24`

## Source Observation Shape

Each fixture file is a JSON object with these top-level fields:

- `fixture_set_id`: Stable identifier for the fixture set.
- `fixture_kind`: Must be `source_observation_snapshots`.
- `description`: Human-readable purpose of the fixture set.
- `safety`: Synthetic-data guardrails for reviewers and validators.
- `comparison_expectations`: Declares records that should later exercise added,
  removed, changed, and unchanged comparison behavior.
- `snapshots`: Ordered source snapshots from the same synthetic authorized
  source.

Each snapshot contains:

- `snapshot_id`: Stable snapshot identifier.
- `source_id`: Synthetic source identifier.
- `collected_at`: UTC timestamp for the synthetic collection event. Snapshots in
  a fixture file must be ordered chronologically by this value.
- `authorization_scope_ref`: Synthetic authorization reference, not a real
  approval or credential.
- `observations`: Source-native observations limited to approved synthetic
  fields.

Each observation contains:

- `source_record_id`: Stable source-native record identifier.
- `observed_asset`: The source-reported asset label, either an example domain or
  documentation IP address.
- `exposure_category`: Source-reported category for later normalization tests.
- `source_status`: Source-reported status. Allowed values are `observed` and
  `remediated`.
- `source_confidence`: Source-reported confidence level. Allowed values are
  `low`, `medium`, and `high`.
- `source_payload`: Synthetic near-raw source payload, limited to approved
  fields such as example asset labels, documentation IPs, ports, protocols,
  service names, and evidence notes.

For domain observations, `source_payload.asset` must match
`observed_asset.value`. For IP observations, `source_payload.ip` must match
`observed_asset.value`.

## Safety Constraints

Fixture data must not contain secrets, credentials, cookies, customer data,
production data, real targets, external API responses, or private target data.
The fixture validator rejects common secret-like field names, real-looking host
data outside the allowed example domains and documentation IP ranges, and
missing comparison coverage. It also rejects obvious secret-like string values,
including common token formats and direct secret, token, password, credential,
cookie, API key, or private key assignments inside fixture values.

Future work may add parsers, normalizers, and comparison tests against these
fixtures. It must still avoid active scanning, crawling, probing, exploitation,
fingerprinting, credential testing, real target interaction, network calls, and
runtime integrations unless a later reviewed issue explicitly authorizes them.
