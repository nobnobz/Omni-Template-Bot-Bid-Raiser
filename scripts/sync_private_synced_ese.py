#!/usr/bin/env python3
"""Sync a small whitelist of ESE rules from Tam-Taro's upstream template."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Iterable

UPSTREAM_URL = "https://raw.githubusercontent.com/Tam-Taro/SEL-Filtering-and-Sorting/main/AIOStreams-SyncedURLs/Tamtaro-synced-ESEs-standard.json"
DEFAULT_TARGET_PATH = Path("Other/private-synced-ese.json")

TARGET_RULE_LABELS = (
    "G's Low Bitrate",
    "No Sootio Library",
    "ongoingSeasonPack",
    "Low Seeders",
    "Extra SeaDex",
    "Bad 4k Anime",
    "Upscaled 4k",
    "Bad 4k Bluray",
    "Bad 1080P Bluray",
)

VERSION_LABEL_PREFIX = "Standard ESE"
COMMENT_RE = re.compile(r"^/\*([^*]+)\*/")
VERSION_RE = re.compile(r"v(\d+(?:\.\d+)*)")


def main() -> int:
    args = parse_args()

    try:
        upstream_entries = fetch_upstream_entries(args.upstream_url)
        target_data = load_json(args.target_file)
        changed, missing_local_rules = sync_target_data(target_data, upstream_entries)
    except Exception as exc:  # pragma: no cover - surfaced in CI and CLI
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.dry_run:
        print(json.dumps(target_data, indent=2, ensure_ascii=False))
        return 0

    if missing_local_rules:
        print(
            "Skipped missing local rules: " + ", ".join(missing_local_rules),
            file=sys.stderr,
        )

    if changed:
        write_json(args.target_file, target_data)
        print(f"Updated {args.target_file}")
    else:
        print(f"No changes for {args.target_file}")

    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-file", type=Path, default=DEFAULT_TARGET_PATH)
    parser.add_argument("--upstream-url", default=UPSTREAM_URL)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def fetch_upstream_entries(url: str) -> list[dict]:
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            payload = response.read().decode("utf-8")
    except urllib.error.URLError as exc:  # pragma: no cover - network failure
        raise RuntimeError(f"failed to fetch upstream ESE file from {url}") from exc

    parsed = json.loads(payload)
    if not isinstance(parsed, list):
        raise RuntimeError("upstream ESE file must be a JSON array")
    return parsed


def load_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError(f"{path} must contain a JSON object")
    return data


def sync_target_data(target_data: dict, upstream_entries: Iterable[dict]) -> tuple[bool, list[str]]:
    values = target_data.get("values")
    metadata = target_data.get("metadata")

    if not isinstance(values, list):
        raise RuntimeError("target data must contain a JSON array at values")
    if not isinstance(metadata, dict):
        raise RuntimeError("target data must contain a JSON object at metadata")

    upstream_by_label = {
        label: entry.get("expression")
        for entry in upstream_entries
        if isinstance(entry, dict) and (label := extract_label(entry.get("expression"))) is not None
    }

    changed = False
    missing_local_rules: list[str] = []
    for label in TARGET_RULE_LABELS:
        if label not in upstream_by_label:
            raise RuntimeError(f"missing upstream rule {label!r}")

        index = find_value_index(values, label)
        if index is None:
            missing_local_rules.append(label)
            continue

        upstream_expression = upstream_by_label[label]
        if not isinstance(upstream_expression, str):
            raise RuntimeError(f"upstream rule {label!r} does not contain an expression string")

        if values[index] != upstream_expression:
            values[index] = upstream_expression
            changed = True

    version = extract_upstream_version(upstream_entries)
    if version and metadata.get("version") != version:
        metadata["version"] = version
        changed = True

    return changed, missing_local_rules


def extract_upstream_version(upstream_entries: Iterable[dict]) -> str | None:
    for entry in upstream_entries:
        if not isinstance(entry, dict):
            continue

        label = extract_label(entry.get("expression"))
        if not label or not label.startswith(VERSION_LABEL_PREFIX):
            continue

        match = VERSION_RE.search(label)
        if match:
            return match.group(1)

    return None


def extract_label(expression: object) -> str | None:
    if not isinstance(expression, str):
        return None

    match = COMMENT_RE.match(expression.strip())
    if not match:
        return None
    return match.group(1).strip()


def find_value_index(values: list, label: str) -> int | None:
    for index, value in enumerate(values):
        if extract_label(value) == label:
            return index
    return None


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
