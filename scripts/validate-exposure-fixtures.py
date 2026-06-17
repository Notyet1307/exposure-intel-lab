#!/usr/bin/env python3
"""Validate synthetic exposure source observation fixtures."""

from __future__ import annotations

import ipaddress
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "fixtures" / "exposure"
EXPECTED_KIND = "source_observation_snapshots"
EXPECTED_CASES = {"added", "removed", "changed", "unchanged"}
ALLOWED_DOMAIN_SUFFIXES = (".example", ".invalid")
ALLOWED_IP_NETWORKS = tuple(
    ipaddress.ip_network(network)
    for network in ("192.0.2.0/24", "198.51.100.0/24", "203.0.113.0/24")
)
SECRET_FIELD_PATTERN = re.compile(
    r"(secret|token|password|credential|cookie|api[_-]?key|private[_-]?key)",
    re.IGNORECASE,
)
DOMAIN_LIKE_PATTERN = re.compile(
    r"\b(?!(?:snapshot|src|rec|synthetic|source|observation|authorized)\b)"
    r"(?=[a-z0-9.-]*\.)[a-z0-9][a-z0-9.-]*\.[a-z]{2,}\b",
    re.IGNORECASE,
)
ISO_UTC_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def main() -> int:
    errors: list[str] = []

    if not FIXTURE_DIR.is_dir():
        errors.append("fixtures/exposure is missing")
    else:
        fixture_paths = sorted(FIXTURE_DIR.glob("*.json"))
        if not fixture_paths:
            errors.append("fixtures/exposure contains no JSON fixture files")

        for fixture_path in fixture_paths:
            errors.extend(validate_fixture_file(fixture_path))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("OK: exposure fixtures")
    return 0


def validate_fixture_file(path: Path) -> list[str]:
    label = path.relative_to(ROOT).as_posix()
    errors: list[str] = []

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return [f"{label} is not valid JSON: {error}"]

    if not isinstance(data, dict):
        return [f"{label} must be a JSON object"]

    errors.extend(validate_no_secret_fields(data, label))
    errors.extend(validate_strings_are_synthetic(data, label))

    for field in ("fixture_set_id", "fixture_kind", "description", "safety", "comparison_expectations", "snapshots"):
        if field not in data:
            errors.append(f"{label} missing top-level {field}")

    if data.get("fixture_kind") != EXPECTED_KIND:
        errors.append(f"{label} fixture_kind must be {EXPECTED_KIND}")

    safety = data.get("safety")
    if not isinstance(safety, dict):
        errors.append(f"{label} safety must be an object")
    elif safety.get("synthetic_only") is not True:
        errors.append(f"{label} safety.synthetic_only must be true")

    snapshots = data.get("snapshots")
    if not isinstance(snapshots, list) or len(snapshots) < 2:
        errors.append(f"{label} snapshots must contain at least two snapshots")
        snapshots = []

    snapshot_ids: set[str] = set()
    observed_records: dict[str, set[str]] = {}
    for index, snapshot in enumerate(snapshots):
        if not isinstance(snapshot, dict):
            errors.append(f"{label} snapshots[{index}] must be an object")
            continue
        snapshot_errors, snapshot_id, record_ids = validate_snapshot(snapshot, label, index)
        errors.extend(snapshot_errors)
        if snapshot_id:
            if snapshot_id in snapshot_ids:
                errors.append(f"{label} duplicate snapshot_id {snapshot_id}")
            snapshot_ids.add(snapshot_id)
            observed_records[snapshot_id] = record_ids

    expectations = data.get("comparison_expectations")
    if not isinstance(expectations, list):
        errors.append(f"{label} comparison_expectations must be a list")
    else:
        errors.extend(validate_comparison_expectations(expectations, label, snapshot_ids, observed_records))

    return errors


def validate_snapshot(snapshot: dict[str, Any], label: str, index: int) -> tuple[list[str], str | None, set[str]]:
    errors: list[str] = []
    prefix = f"{label} snapshots[{index}]"
    record_ids: set[str] = set()

    required_fields = ("snapshot_id", "source_id", "collected_at", "authorization_scope_ref", "observations")
    for field in required_fields:
        if field not in snapshot:
            errors.append(f"{prefix} missing {field}")

    snapshot_id = require_string(snapshot.get("snapshot_id"), f"{prefix}.snapshot_id", errors)
    require_string(snapshot.get("source_id"), f"{prefix}.source_id", errors)
    collected_at = require_string(snapshot.get("collected_at"), f"{prefix}.collected_at", errors)
    require_string(snapshot.get("authorization_scope_ref"), f"{prefix}.authorization_scope_ref", errors)
    if collected_at and not is_utc_timestamp(collected_at):
        errors.append(f"{prefix}.collected_at must be an ISO-8601 UTC timestamp")

    observations = snapshot.get("observations")
    if not isinstance(observations, list) or not observations:
        errors.append(f"{prefix}.observations must be a non-empty list")
        return errors, snapshot_id, record_ids

    for observation_index, observation in enumerate(observations):
        if not isinstance(observation, dict):
            errors.append(f"{prefix}.observations[{observation_index}] must be an object")
            continue

        observation_errors, record_id = validate_observation(observation, f"{prefix}.observations[{observation_index}]")
        errors.extend(observation_errors)
        if record_id:
            if record_id in record_ids:
                errors.append(f"{prefix} duplicate source_record_id {record_id}")
            record_ids.add(record_id)

    return errors, snapshot_id, record_ids


def validate_observation(observation: dict[str, Any], prefix: str) -> tuple[list[str], str | None]:
    errors: list[str] = []
    required_fields = (
        "source_record_id",
        "observed_asset",
        "exposure_category",
        "source_status",
        "source_confidence",
        "source_payload",
    )
    for field in required_fields:
        if field not in observation:
            errors.append(f"{prefix} missing {field}")

    record_id = require_string(observation.get("source_record_id"), f"{prefix}.source_record_id", errors)
    require_string(observation.get("exposure_category"), f"{prefix}.exposure_category", errors)
    require_string(observation.get("source_status"), f"{prefix}.source_status", errors)
    require_string(observation.get("source_confidence"), f"{prefix}.source_confidence", errors)

    observed_asset = observation.get("observed_asset")
    if not isinstance(observed_asset, dict):
        errors.append(f"{prefix}.observed_asset must be an object")
    else:
        kind = require_string(observed_asset.get("kind"), f"{prefix}.observed_asset.kind", errors)
        value = require_string(observed_asset.get("value"), f"{prefix}.observed_asset.value", errors)
        if kind and value:
            errors.extend(validate_asset_value(kind, value, f"{prefix}.observed_asset.value"))

    source_payload = observation.get("source_payload")
    if not isinstance(source_payload, dict):
        errors.append(f"{prefix}.source_payload must be an object")
    elif not source_payload:
        errors.append(f"{prefix}.source_payload must not be empty")

    return errors, record_id


def validate_comparison_expectations(
    expectations: list[Any],
    label: str,
    snapshot_ids: set[str],
    observed_records: dict[str, set[str]],
) -> list[str]:
    errors: list[str] = []
    cases: set[str] = set()

    for index, expectation in enumerate(expectations):
        prefix = f"{label} comparison_expectations[{index}]"
        if not isinstance(expectation, dict):
            errors.append(f"{prefix} must be an object")
            continue

        case = require_string(expectation.get("case"), f"{prefix}.case", errors)
        record_id = require_string(expectation.get("source_record_id"), f"{prefix}.source_record_id", errors)
        if case:
            cases.add(case)
            if case not in EXPECTED_CASES:
                errors.append(f"{prefix}.case must be one of {sorted(EXPECTED_CASES)}")

        baseline_id = expectation.get("baseline_snapshot_id")
        current_id = expectation.get("current_snapshot_id")
        if baseline_id is not None and not isinstance(baseline_id, str):
            errors.append(f"{prefix}.baseline_snapshot_id must be a string or null")
        if current_id is not None and not isinstance(current_id, str):
            errors.append(f"{prefix}.current_snapshot_id must be a string or null")
        for field_name, snapshot_id in (("baseline_snapshot_id", baseline_id), ("current_snapshot_id", current_id)):
            if isinstance(snapshot_id, str) and snapshot_id not in snapshot_ids:
                errors.append(f"{prefix}.{field_name} references unknown snapshot {snapshot_id}")

        if case in EXPECTED_CASES and record_id:
            errors.extend(validate_expected_record_presence(prefix, case, record_id, baseline_id, current_id, observed_records))

    missing_cases = EXPECTED_CASES - cases
    if missing_cases:
        errors.append(f"{label} comparison_expectations missing cases {sorted(missing_cases)}")

    return errors


def validate_expected_record_presence(
    prefix: str,
    case: str,
    record_id: str,
    baseline_id: Any,
    current_id: Any,
    observed_records: dict[str, set[str]],
) -> list[str]:
    errors: list[str] = []
    baseline_has = isinstance(baseline_id, str) and record_id in observed_records.get(baseline_id, set())
    current_has = isinstance(current_id, str) and record_id in observed_records.get(current_id, set())

    if case == "added":
        if baseline_id is not None or not current_has:
            errors.append(f"{prefix} added case must have null baseline and present current record")
    elif case == "removed":
        if not baseline_has or current_id is not None:
            errors.append(f"{prefix} removed case must have present baseline record and null current")
    elif case in {"changed", "unchanged"}:
        if not baseline_has or not current_has:
            errors.append(f"{prefix} {case} case must have present baseline and current records")

    return errors


def validate_asset_value(kind: str, value: str, label: str) -> list[str]:
    if kind == "domain":
        if not value.endswith(ALLOWED_DOMAIN_SUFFIXES):
            return [f"{label} domain must end with one of {ALLOWED_DOMAIN_SUFFIXES}"]
    elif kind == "ip":
        if not is_allowed_ip(value):
            return [f"{label} IP must be in an allowed documentation range"]
    else:
        return [f"{label} asset kind must be domain or ip"]

    return []


def validate_no_secret_fields(value: Any, label: str) -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_label = f"{label}.{key}"
            if SECRET_FIELD_PATTERN.search(key):
                errors.append(f"{child_label} uses a secret-like field name")
            errors.extend(validate_no_secret_fields(child, child_label))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(validate_no_secret_fields(child, f"{label}[{index}]"))
    return errors


def validate_strings_are_synthetic(value: Any, label: str) -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            errors.extend(validate_strings_are_synthetic(child, f"{label}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(validate_strings_are_synthetic(child, f"{label}[{index}]"))
    elif isinstance(value, str):
        for ip_candidate in ipaddress_values(value):
            if not is_allowed_ip(ip_candidate):
                errors.append(f"{label} contains non-documentation IP {ip_candidate}")
        for domain_candidate in DOMAIN_LIKE_PATTERN.findall(value):
            if not domain_candidate.endswith(ALLOWED_DOMAIN_SUFFIXES):
                errors.append(f"{label} contains non-example domain {domain_candidate}")
    return errors


def ipaddress_values(value: str) -> list[str]:
    candidates: list[str] = []
    for match in re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", value):
        try:
            ipaddress.ip_address(match)
        except ValueError:
            continue
        candidates.append(match)
    return candidates


def is_allowed_ip(value: str) -> bool:
    try:
        address = ipaddress.ip_address(value)
    except ValueError:
        return False
    return any(address in network for network in ALLOWED_IP_NETWORKS)


def is_utc_timestamp(value: str) -> bool:
    if not ISO_UTC_PATTERN.match(value):
        return False
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return False
    return True


def require_string(value: Any, label: str, errors: list[str]) -> str | None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label} must be a non-empty string")
        return None
    return value


if __name__ == "__main__":
    raise SystemExit(main())
