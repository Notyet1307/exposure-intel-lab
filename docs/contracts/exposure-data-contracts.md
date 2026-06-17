# Exposure Data Contracts

These contracts define the synthetic data surface for fixture-first exposure
intelligence work. They are conceptual contracts for future runtime design, not
real API schemas, vendor adapter schemas, or authorization to ingest real target
data.

All examples and fixture data must remain synthetic. Source observations must
use reserved example domains, `.invalid` names, or documentation IP ranges only.
Contracts in this document must not be implemented with network calls, active
scanning, crawling, probing, exploitation, fingerprinting, credential testing, or
real target interaction unless a later reviewed issue explicitly authorizes that
work.

## Source Observation Contract

Source observations represent near-raw records from a synthetic authorized
source snapshot. They preserve the source-native record identity and enough
payload detail for later normalization and comparison tests.

Required snapshot fields:

- `snapshot_id`: stable identifier for one source snapshot.
- `source_id`: stable synthetic source identifier.
- `collected_at`: ISO-8601 UTC timestamp ending in `Z`; snapshots in a fixture
  file must appear in strictly increasing chronological order.
- `authorization_scope_ref`: synthetic authorization reference only.
- `observations`: non-empty list of source observations.

Required observation fields:

- `source_record_id`: stable source-native record identifier within a snapshot.
- `observed_asset`: source-reported asset object with `kind` and `value`.
- `exposure_category`: source-reported category for future normalization.
- `source_status`: source-reported status. Allowed values are `observed` and
  `remediated`.
- `source_confidence`: source-reported confidence. Allowed values are `low`,
  `medium`, and `high`.
- `source_payload`: non-empty synthetic near-raw payload.

Allowed observed assets:

- `kind: "domain"` with a value ending in `.example` or `.invalid`.
- `kind: "ip"` with a value in `192.0.2.0/24`, `198.51.100.0/24`, or
  `203.0.113.0/24`.

Payload consistency rules:

- For a domain `observed_asset`, `source_payload.asset` must match
  `observed_asset.value`.
- For an IP `observed_asset`, `source_payload.ip` must match
  `observed_asset.value`.
- Payload strings must not contain real-looking domains outside approved
  suffixes, non-documentation IP addresses, secret-like field names, or obvious
  secret-like values.

## Normalized Exposure Record Contract

Normalized exposure records are the future runtime output of translating source
observations into a stable product data shape. They are not implemented in the
current fixture-only phase, but downstream design should preserve these
conceptual fields.

Expected normalized fields:

- `normalized_record_id`: deterministic identifier derived from the source,
  source record, and normalized asset.
- `source_record_id`: original source observation identifier.
- `source_id`: original synthetic source identifier.
- `snapshot_id`: source snapshot that produced the record.
- `asset`: normalized asset object with `kind` and `value`.
- `category`: normalized exposure category.
- `status`: normalized exposure status derived from `source_status`.
- `confidence`: normalized confidence derived from `source_confidence`.
- `observed_at`: normalized timestamp copied from the snapshot `collected_at`.
- `evidence`: bounded synthetic evidence fields copied from approved
  `source_payload` keys.

Normalization must be deterministic for the same input. It must not add live
enrichment, network lookups, scanning, source adapter calls, secrets, customer
data, or production data.

## Comparison Report Contract

Comparison reports are the future runtime output of comparing two normalized
snapshot results.

Expected report fields:

- `baseline_snapshot_id`: earlier snapshot identifier, or `null` only for
  explicitly added records.
- `current_snapshot_id`: later snapshot identifier, or `null` only for
  explicitly removed records.
- `generated_at`: deterministic report generation timestamp or an explicit test
  fixture value in future runtime tests.
- `summary`: counts for `added`, `removed`, `changed`, and `unchanged` records.
- `records`: per-record comparison entries.

Allowed comparison cases:

- `added`: absent from baseline and present in current.
- `removed`: present in baseline and absent from current.
- `changed`: present in both snapshots with a material normalized-field change.
- `unchanged`: present in both snapshots with no material normalized-field
  change.

The fixture validator checks `comparison_expectations` for these four cases so
future comparison behavior has deterministic acceptance examples.

## Audit Manifest Contract

Audit manifests are the future runtime evidence record for a deterministic run.
They should make an execution reproducible without depending on Codex, Multica,
GitHub, GitHub Actions, or issue state.

Expected manifest fields:

- `manifest_version`: audit manifest contract version.
- `input_fixture_path`: relative path to the synthetic input fixture.
- `input_sha256`: hash of the exact input bytes.
- `output_paths`: relative paths to generated normalized records, comparison
  reports, and human-readable reports.
- `output_sha256`: hash map for generated outputs.
- `command`: local command used to produce outputs.
- `runtime_version`: product runtime version or fixture test runtime version.
- `validation_status`: pass/fail status for contract validation.
- `created_at`: deterministic or explicitly supplied timestamp for test runs.

Audit manifests must not include secrets, credentials, cookies, customer data,
production data, raw external API responses, local auth files, or private target
data.
