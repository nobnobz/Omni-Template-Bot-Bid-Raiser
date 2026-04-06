#!/usr/bin/env python3
"""Update release-group regex lists in Other/fusion-tags-ume.json from upstream source."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

UPSTREAM_URL = "https://raw.githubusercontent.com/Vidhin05/Releases-Regex/main/English/regexes.json"
DEFAULT_TARGET_PATH = Path("Other/fusion-tags-ume.json")

TIERS = ("T1", "T2", "T3")
TIER_PRIORITY = {tier: index for index, tier in enumerate(TIERS)}
CATEGORY_ORDER = ("REMUX", "BLU-RAY", "WEB")

# Explicit source-to-target mapping requested by repository owner.
SOURCE_MAPPING = {
    "REMUX": {
        "T1": [("Radarr Remux T1", True), ("Sonarr Remux T1", True)],
        "T2": [("Radarr Remux T2", True), ("Sonarr Remux T2", True)],
        "T3": [("Radarr Remux T3", True), ("Sonarr Remux T3", False)],
    },
    "BLU-RAY": {
        "T1": [("Radarr UHD Bluray T1", True), ("Radarr HD Bluray T1", True), ("Sonarr HD Bluray T1", True)],
        "T2": [("Radarr UHD Bluray T2", True), ("Radarr HD Bluray T2", True), ("Sonarr HD Bluray T2", True)],
        "T3": [("Radarr UHD Bluray T3", True), ("Radarr HD Bluray T3", True), ("Sonarr HD Bluray T3", False)],
    },
    "WEB": {
        "T1": [("Radarr Web T1", True), ("Sonarr Web T1", True), ("Web T1", True)],
        "T2": [("Radarr Web T2", True), ("Sonarr Web T2", True), ("Web T2", False)],
        "T3": [("Radarr Web T3", True), ("Sonarr Web T3", True), ("Web T3", False)],
    },
}

TARGET_FILTER_NAMES = {
    "REMUX": {"T1": "REMUX 1", "T2": "REMUX 2", "T3": "REMUX 3", "UNRANKED": "REMUX Unranked"},
    "BLU-RAY": {
        "T1": "BLU-RAY 1",
        "T2": "BLU-RAY 2",
        "T3": "BLU-RAY 3",
        "UNRANKED": "BLU-RAY Unranked",
    },
    "WEB": {"T1": "WEB 1", "T2": "WEB 2", "T3": "WEB 3", "UNRANKED": "WEB Unranked"},
}

# Captures token lists wrapped with word boundaries, e.g. \b(?:A|B|C)\b or \b(A|B)\b.
BOUNDARY_LIST_PATTERN = re.compile(
    r"\\b\(\?:([A-Za-z0-9][A-Za-z0-9._-]*(?:\|[A-Za-z0-9][A-Za-z0-9._-]*)*)\)\\b"
    r"|\\b\(([A-Za-z0-9][A-Za-z0-9._-]*(?:\|[A-Za-z0-9][A-Za-z0-9._-]*)*)\)\\b"
)


@dataclass(frozen=True)
class UpstreamEntry:
    name: str
    pattern: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-url", default=UPSTREAM_URL, help="URL for upstream regexes.json")
    parser.add_argument(
        "--target-file",
        default=str(DEFAULT_TARGET_PATH),
        help="Path to Other/fusion-tags-ume.json",
    )
    return parser.parse_args()


def fetch_upstream_entries(source_url: str) -> List[UpstreamEntry]:
    try:
        with urllib.request.urlopen(source_url, timeout=30) as response:
            payload = response.read().decode("utf-8")
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Failed downloading upstream data from {source_url}: {exc}") from exc

    try:
        data = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Upstream file is not valid JSON: {exc}") from exc

    if not isinstance(data, list):
        raise RuntimeError("Unexpected upstream format: root must be a JSON array.")

    entries: List[UpstreamEntry] = []
    for index, item in enumerate(data):
        if not isinstance(item, dict):
            raise RuntimeError(f"Unexpected upstream format: item #{index} is not an object.")

        name = item.get("name")
        pattern = item.get("pattern")
        if not isinstance(name, str) or not isinstance(pattern, str):
            raise RuntimeError(f"Unexpected upstream format: item #{index} missing string name/pattern.")

        entries.append(UpstreamEntry(name=name, pattern=pattern))

    return entries


def extract_groups_from_pattern(pattern: str) -> List[str]:
    """Extract release groups from \b-bounded token lists inside regex patterns."""
    normalized = pattern.replace("\x08", r"\b")
    normalized = normalized.replace(r"\\b", r"\b")
    groups: List[str] = []

    for match in BOUNDARY_LIST_PATTERN.finditer(normalized):
        chunk = match.group(1) or match.group(2)
        if not chunk:
            continue
        groups.extend(chunk.split("|"))

    return groups


def merge_source_groups(entries: Iterable[UpstreamEntry]) -> Dict[str, Dict[str, List[str]]]:
    by_name: Dict[str, List[UpstreamEntry]] = {}
    for entry in entries:
        by_name.setdefault(entry.name, []).append(entry)

    merged: Dict[str, Dict[str, List[str]]] = {category: {tier: [] for tier in TIERS} for category in CATEGORY_ORDER}

    for category in CATEGORY_ORDER:
        for tier in TIERS:
            mapped_entries = SOURCE_MAPPING[category][tier]
            for mapped_name, required in mapped_entries:
                source_entries = by_name.get(mapped_name)
                if not source_entries:
                    if required:
                        raise RuntimeError(
                            f"Upstream format changed: source entry '{mapped_name}' not found for {category} {tier}."
                        )
                    print(
                        f"[source] Optional source '{mapped_name}' not found for {category} {tier}; skipping."
                    )
                    continue

                for source_entry in source_entries:
                    source_groups = extract_groups_from_pattern(source_entry.pattern)
                    if not source_groups:
                        raise RuntimeError(
                            "Upstream format changed: unable to parse release groups from "
                            f"entry '{source_entry.name}'."
                        )
                    print(f"[source] {source_entry.name}: {len(source_groups)} groups -> {source_groups}")
                    merged[category][tier].extend(source_groups)

    return merged


def resolve_tier_conflicts(
    merged: Dict[str, Dict[str, List[str]]]
) -> Tuple[
    Dict[str, Dict[str, List[str]]],
    Dict[str, List[str]],
    Dict[str, List[str]],
    Dict[str, List[str]],
    Dict[str, int],
]:
    final: Dict[str, Dict[str, List[str]]] = {category: {tier: [] for tier in TIERS} for category in CATEGORY_ORDER}
    unranked_exclusions: Dict[str, List[str]] = {category: [] for category in CATEGORY_ORDER}
    duplicate_logs: Dict[str, List[str]] = {category: [] for category in CATEGORY_ORDER}
    promotion_logs: Dict[str, List[str]] = {category: [] for category in CATEGORY_ORDER}

    for category in CATEGORY_ORDER:
        seen_exact_per_tier: Dict[str, set[str]] = {tier: set() for tier in TIERS}
        best_by_lower: Dict[str, Tuple[str, str]] = {}

        for tier in TIERS:
            for group in merged[category][tier]:
                if group in seen_exact_per_tier[tier]:
                    duplicate_logs[category].append(
                        f"Exact duplicate removed in {category} {tier}: {group}"
                    )
                    continue
                seen_exact_per_tier[tier].add(group)

                # Normalize to lowercase for cross-tier conflict checks so case-only variants
                # (e.g. ABBIE vs ABBiE) resolve to the highest-priority tier spelling.
                lower_key = group.lower()
                existing = best_by_lower.get(lower_key)
                if existing is None:
                    best_by_lower[lower_key] = (tier, group)
                    final[category][tier].append(group)
                    continue

                existing_tier, existing_spelling = existing
                if TIER_PRIORITY[tier] < TIER_PRIORITY[existing_tier]:
                    final[category][existing_tier].remove(existing_spelling)
                    final[category][tier].append(group)
                    best_by_lower[lower_key] = (tier, group)
                    promotion_logs[category].append(
                        f"Promoted {group} to {category} {tier} over {existing_spelling} from {existing_tier}"
                    )
                elif TIER_PRIORITY[tier] > TIER_PRIORITY[existing_tier]:
                    duplicate_logs[category].append(
                        f"Dropped lower-tier duplicate in {category} {tier}: {group} (kept {existing_spelling} in {existing_tier})"
                    )
                else:
                    # Same-tier mixed-case variants are preserved to keep case-sensitive behavior by default.
                    final[category][tier].append(group)

        seen_unranked: set[str] = set()
        for tier in TIERS:
            for group in final[category][tier]:
                if group not in seen_unranked:
                    unranked_exclusions[category].append(group)
                    seen_unranked.add(group)

    final_counts = {
        f"{category} {tier}": len(final[category][tier]) for category in CATEGORY_ORDER for tier in TIERS
    }

    return final, unranked_exclusions, duplicate_logs, promotion_logs, final_counts


def replace_group_list_in_pattern(pattern: str, groups: List[str]) -> str:
    serialized = "|".join(groups)
    match = BOUNDARY_LIST_PATTERN.search(pattern)
    if not match:
        raise RuntimeError("Target pattern format changed: missing release-group token list.")

    chunk = match.group(1) or match.group(2)
    if chunk is None:
        raise RuntimeError("Target pattern format changed: malformed release-group token list.")

    start, end = match.span(1 if match.group(1) is not None else 2)
    return f"{pattern[:start]}{serialized}{pattern[end:]}"


def build_updated_patterns(target_json: Dict[str, object], final: Dict[str, Dict[str, List[str]]], unranked: Dict[str, List[str]]) -> Dict[str, str]:
    filters = target_json.get("filters")
    if not isinstance(filters, list):
        raise RuntimeError("Target file format changed: top-level 'filters' array missing.")

    pattern_by_name: Dict[str, str] = {}
    for item in filters:
        if not isinstance(item, dict):
            continue
        name = item.get("name")
        pattern = item.get("pattern")
        if isinstance(name, str) and isinstance(pattern, str):
            pattern_by_name[name] = pattern

    updated: Dict[str, str] = {}
    for category in CATEGORY_ORDER:
        for tier in TIERS:
            filter_name = TARGET_FILTER_NAMES[category][tier]
            current_pattern = pattern_by_name.get(filter_name)
            if current_pattern is None:
                raise RuntimeError(f"Target pattern '{filter_name}' not found in fusion-tags-ume.json.")
            updated[filter_name] = replace_group_list_in_pattern(current_pattern, final[category][tier])

        unranked_name = TARGET_FILTER_NAMES[category]["UNRANKED"]
        current_unranked_pattern = pattern_by_name.get(unranked_name)
        if current_unranked_pattern is None:
            raise RuntimeError(f"Target pattern '{unranked_name}' not found in fusion-tags-ume.json.")
        updated[unranked_name] = replace_group_list_in_pattern(current_unranked_pattern, unranked[category])

    return updated


def update_patterns_in_raw_json(raw_text: str, updated_patterns: Dict[str, str]) -> str:
    updated_text = raw_text
    for name, new_pattern in updated_patterns.items():
        escaped_name = re.escape(name)
        matcher = re.compile(
            rf'("name"\s*:\s*"{escaped_name}"\s*,[\s\S]*?"pattern"\s*:\s*")((?:\\.|[^"\\])*)(")'
        )

        replacement_count = 0

        def replacer(match: re.Match[str]) -> str:
            nonlocal replacement_count
            replacement_count += 1
            escaped_pattern = json.dumps(new_pattern, ensure_ascii=False)[1:-1]
            return f"{match.group(1)}{escaped_pattern}{match.group(3)}"

        updated_text = matcher.sub(replacer, updated_text)
        if replacement_count != 1:
            raise RuntimeError(
                f"Failed updating filter '{name}': expected exactly one pattern field match, got {replacement_count}."
            )

    return updated_text


def main() -> int:
    args = parse_args()
    target_path = Path(args.target_file)

    entries = fetch_upstream_entries(args.source_url)
    merged = merge_source_groups(entries)

    for category in CATEGORY_ORDER:
        for tier in TIERS:
            print(f"[merged] {category} {tier}: {len(merged[category][tier])} groups")

    final, unranked, duplicate_logs, promotion_logs, final_counts = resolve_tier_conflicts(merged)

    for category in CATEGORY_ORDER:
        for line in promotion_logs[category]:
            print(f"[promotion] {line}")
        for line in duplicate_logs[category]:
            print(f"[dedupe] {line}")
        print(f"[unranked] {category}: {len(unranked[category])} exclusions")

    for key, count in final_counts.items():
        print(f"[final] {key}: {count} groups")

    raw_text = target_path.read_text(encoding="utf-8")
    target_json = json.loads(raw_text)

    updated_patterns = build_updated_patterns(target_json, final, unranked)
    updated_text = update_patterns_in_raw_json(raw_text, updated_patterns)

    if updated_text != raw_text:
        target_path.write_text(updated_text, encoding="utf-8")
        print(f"Updated {target_path}")
    else:
        print(f"No changes needed for {target_path}")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
