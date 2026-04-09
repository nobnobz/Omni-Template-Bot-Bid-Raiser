#!/usr/bin/env python3
"""Update fusion release-group filters from upstream regexes.json."""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence

UPSTREAM_URL = "https://raw.githubusercontent.com/Vidhin05/Releases-Regex/main/English/regexes.json"
DEFAULT_TARGET_PATH = Path("Other/fusion-tags-ume.json")

TARGET_TEMPLATE_MAP = {
    "fusion-tags-ume.json": Path("Other/fusion-tags-ume-copy.json"),
    "fusion-tags-ume-colored.json": Path("Other/fusion-tags-ume-colored-copy.json"),
}

FAMILY_TIERS = {
    "REMUX": ("1", "2", "3"),
    "BLU-RAY": ("1", "2", "3", "4", "5", "6", "7", "8"),
    "WEB": ("1", "2", "3", "4", "5", "6"),
}

SOURCE_MAPPING = {
    "REMUX": {
        "1": ("Radarr Remux T1", "Sonarr Remux T1"),
        "2": ("Radarr Remux T2", "Sonarr Remux T2"),
        "3": ("Radarr Remux T3",),
    },
    "BLU-RAY": {
        "1": ("Radarr UHD Bluray T1", "Radarr HD Bluray T1", "Sonarr HD Bluray T1", "Anime BD T1"),
        "2": ("Radarr UHD Bluray T2", "Radarr HD Bluray T2", "Sonarr HD Bluray T2", "Anime BD T2"),
        "3": ("Radarr UHD Bluray T3", "Radarr HD Bluray T3", "Anime BD T3"),
        "4": ("Anime BD T4",),
        "5": ("Anime BD T5",),
        "6": ("Anime BD T6",),
        "7": ("Anime BD T7",),
        "8": ("Anime BD T8",),
    },
    "WEB": {
        "1": ("Radarr Web T1", "Sonarr Web T1", "Web T1", "Anime Web T1"),
        "2": ("Radarr Web T2", "Sonarr Web T2", "Anime Web T2"),
        "3": ("Radarr Web T3", "Sonarr Web T3", "Anime Web T3"),
        "4": ("Anime Web T4",),
        "5": ("Anime Web T5",),
        "6": ("Anime Web T6",),
    },
}

SOURCE_FILTER_NAMES = [
    "REMUX 1",
    "REMUX 2",
    "REMUX 3",
    "REMUX Unranked",
    "BLU-RAY 1",
    "BLU-RAY 2",
    "BLU-RAY 3",
    "BLU-RAY 4",
    "BLU-RAY 5",
    "BLU-RAY 6",
    "BLU-RAY 7",
    "BLU-RAY 8",
    "BLU-RAY Unranked",
    "WEB 1",
    "WEB 2",
    "WEB 3",
    "WEB 4",
    "WEB 5",
    "WEB 6",
    "WEB Unranked",
]

BOUNDARY_LIST_PATTERN = re.compile(
    r"\\b\(\?:([A-Za-z0-9][A-Za-z0-9._-]*(?:\|[A-Za-z0-9][A-Za-z0-9._-]*)*)\)\\b"
    r"|\\b\(([A-Za-z0-9][A-Za-z0-9._-]*(?:\|[A-Za-z0-9][A-Za-z0-9._-]*)*)\)\\b"
)
ANIME_GROUP_CHUNK_PATTERNS = (
    re.compile(r"\\\[\(((?:[^()]+))\)\\\]"),
    re.compile(r"\\\[((?:[A-Za-z0-9][A-Za-z0-9+._-]*(?:\|[A-Za-z0-9][A-Za-z0-9+._-]*)*))\\\]"),
    re.compile(r"-\(((?:[^()]+))\)\\b"),
    re.compile(r"\\b\(((?:[^()]+))\)\\b"),
    re.compile(r"-([A-Za-z0-9][A-Za-z0-9+._-]*)-"),
    re.compile(r"-([A-Za-z0-9][A-Za-z0-9+._-]*)\\b"),
)

VIDEO_EXTENSIONS = (
    "mkv",
    "mp4",
    "avi",
    "m2ts",
    "ts",
    "wmv",
    "mov",
    "m4v",
    "mpg",
    "mpeg",
    "iso",
    "srt",
    "ass",
    "ssa",
    "sub",
    "idx",
    "sup",
    "rar",
    "zip",
    "7z",
    "nfo",
)
VIDEO_EXTENSIONS_REGEX = "|".join(VIDEO_EXTENSIONS)
FORMATTER_BOUNDARY = (
    rf"(?:\.(?:{VIDEO_EXTENSIONS_REGEX})\b|(?:\s*[,;|]\s*|\s+[•·]\s+|\s{{2,}}))"
)
GROUP_END_BOUNDARY = rf"(?=$|[\]\)](?=$|{FORMATTER_BOUNDARY})|{FORMATTER_BOUNDARY})"

REMUX_DETECTOR = (
    r"(?:(?:[_. ]|\d{4}p-|\bHybrid-)(?:(?:BD|UHD)[-_. ]?)?Remux\b|"
    r"(?:(?:BD|UHD)[-_. ]?)?Remux[_. ]\d{4}p)"
)
BLURAY_DETECTOR = (
    r"(?:(?:BluRay|Blu-Ray|HD-?DVD|BDMux|BD(?!$)|UHD|4K|bd(?:720|1080|2160)|"
    r"(?<=[-_. (\[])bd(?=[-_. )\]])|DVD|DVDRip|NTSC|PAL|xvidvd))"
)
WEB_DETECTOR = (
    r"(?:(?:WEB[-_. ]DL(?:mux)?|WEBDL|AmazonHD|AmazonSD|iTunesHD|MaxdomeHD|NetflixU?HD|"
    r"WebHD|HBOMaxHD|DisneyHD|[. ]WEB[. ](?:[xh][ .]?26[45]|AVC|HEVC|DDP?[ .]?5[. ]1)|"
    r"(?:720|1080|2160)p[-. ]WEB[-. ]|[-. ]WEB[-. ](?:720|1080|2160)p|"
    r"(?:AMZN|NF|DP)[. -]WEB[. -](?!Rip)|WebRip|Web-Rip|WEBMux|\[WEB\]|[\[\(]WEB[ .]))"
)
TV_MARKER = (
    r"(?:\bS\d{1,2}[ ._-]*E\d{1,3}\b|\b\d{1,2}x\d{1,3}\b|\bSeason[ ._-]?\d{1,2}\b|"
    r"\b(?:Complete|Full)[ ._-]?Season\b|\bSeason[ ._-]?Pack\b)"
)
CR_MARKER = r"(?:^|[^A-Za-z0-9])CR(?:[^A-Za-z0-9]|$)"

STRICT_GROUPS = {
    "3l",
    "ac",
    "arc",
    "bbq",
    "bmf",
    "dae",
    "doc",
    "don",
    "ebp",
    "end",
    "fle",
    "pmr",
    "sam",
    "som",
    "t4h",
    "tdd",
    "tnp",
    "zq",
    "zr",
}

CASE_SENSITIVE_LOWER = {"sigma"}

NON_GROUP_TOKENS = {
    "web",
    "remux",
}

SPECIAL_CASES = {
    "REMUX": (
        {"kind": "tv_split", "groups": ("12GaugeShotgun", "decibeL", "EPSiLON", "HiFi", "KRaLiMaRKo", "TRiToN"), "series_tier": "2", "movie_tier": "3"},
    ),
    "BLU-RAY": (
        {"kind": "tv_split", "groups": ("NTb",), "series_tier": "1", "movie_tier": "2"},
    ),
    "WEB": (
        {"kind": "tv_split", "groups": ("BLUTONiUM", "BYNDR", "GNOME", "TEPES"), "series_tier": "2", "movie_tier": "1"},
        {"kind": "tv_split", "groups": ("NPMS", "ROCCaT", "SiGMA"), "series_tier": "2", "movie_tier": "3"},
        {"kind": "cr_split", "groups": ("Kitsune",), "marked_tier": "3", "unmarked_tier": "1"},
        {"kind": "cr_split", "groups": ("playWEB", "PlayWeb"), "marked_tier": "5", "unmarked_tier": "2"},
    ),
}

SPECIAL_MULTI_TIER_KEYS = {
    group.lower()
    for rules in SPECIAL_CASES.values()
    for rule in rules
    for group in rule["groups"]
}


@dataclass(frozen=True)
class UpstreamEntry:
    name: str
    pattern: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-url", default=UPSTREAM_URL, help="URL for upstream regexes.json")
    parser.add_argument("--target-file", default=str(DEFAULT_TARGET_PATH), help="Path to target fusion tags JSON")
    parser.add_argument("--template-file", default=None, help="Optional template file to mirror source-tag layout")
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
    normalized = pattern.replace("\x08", r"\b").replace(r"\\b", r"\b")
    groups: List[str] = []
    for match in BOUNDARY_LIST_PATTERN.finditer(normalized):
        chunk = match.group(1) or match.group(2)
        if chunk:
            groups.extend(chunk.split("|"))

    lookahead_chunks = extract_positive_lookahead_chunks(pattern)
    candidate_chunk = lookahead_chunks[1] if len(lookahead_chunks) >= 2 else pattern
    groups.extend(extract_groups_from_slot_chunk(candidate_chunk))

    seen: set[str] = set()
    ordered: List[str] = []
    for group in groups:
        if group not in seen:
            seen.add(group)
            ordered.append(group)
    return ordered


def extract_positive_lookahead_chunks(pattern: str) -> List[str]:
    marker = "(?=.*("
    chunks: List[str] = []
    start_index = 0

    while True:
        marker_index = pattern.find(marker, start_index)
        if marker_index == -1:
            break

        index = marker_index + len(marker)
        depth = 1
        chunk_start = index

        while index < len(pattern):
            char = pattern[index]
            if char == "\\":
                index += 2
                continue
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    chunks.append(pattern[chunk_start:index])
                    start_index = index + 1
                    break
            index += 1
        else:
            break

    return chunks


def extract_groups_from_slot_chunk(chunk: str) -> List[str]:
    cleaned = re.sub(r"\(\?[!=<][^)]*\)", "", chunk)
    cleaned = cleaned.replace(".*", "")

    groups: List[str] = []
    for pattern in ANIME_GROUP_CHUNK_PATTERNS:
        for match in pattern.finditer(cleaned):
            for token in match.group(1).split("|"):
                token = re.sub(r"\(\?[!=<][^)]*\)", "", token)
                token = token.replace(r"\b", "").replace("^", "").replace("$", "")
                token = token.strip()
                if token.startswith("-"):
                    token = token[1:]
                if token.endswith("-"):
                    token = token[:-1]
                if token and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9+._-]*", token):
                    groups.append(token)

    # De-dupe while preserving first-seen spelling/order.
    seen: set[str] = set()
    ordered: List[str] = []
    for group in groups:
        if group not in seen:
            seen.add(group)
            ordered.append(group)
    return ordered


def merge_source_groups(entries: Iterable[UpstreamEntry]) -> Dict[str, Dict[str, List[str]]]:
    by_name: Dict[str, List[UpstreamEntry]] = {}
    for entry in entries:
        by_name.setdefault(entry.name, []).append(entry)

    merged = {
        family: {tier: [] for tier in tiers}
        for family, tiers in FAMILY_TIERS.items()
    }

    for family, tier_map in SOURCE_MAPPING.items():
        for tier, source_names in tier_map.items():
            for source_name in source_names:
                source_entries = by_name.get(source_name)
                if not source_entries:
                    raise RuntimeError(
                        f"Upstream format changed: source entry '{source_name}' not found for {family} {tier}."
                    )
                for source_entry in source_entries:
                    groups = extract_groups_from_pattern(source_entry.pattern)
                    if not groups:
                        raise RuntimeError(
                            f"Upstream format changed: unable to parse release groups from '{source_entry.name}'."
                        )
                    merged[family][tier].extend(groups)
    return merged


def _is_case_sensitive_key(group: str) -> bool:
    return group.lower() in CASE_SENSITIVE_LOWER


def is_non_group_token(group: str) -> bool:
    return group.lower() in NON_GROUP_TOKENS


def resolve_tier_conflicts(merged: Dict[str, Dict[str, List[str]]]) -> Dict[str, Dict[str, List[str]]]:
    final = {
        family: {tier: [] for tier in tiers}
        for family, tiers in FAMILY_TIERS.items()
    }

    for family, tiers in FAMILY_TIERS.items():
        seen_exact_per_tier = {tier: set() for tier in tiers}
        best_by_key: Dict[str, tuple[str, str]] = {}

        for tier in tiers:
            for group in merged[family][tier]:
                if group in seen_exact_per_tier[tier]:
                    continue
                seen_exact_per_tier[tier].add(group)

                if is_non_group_token(group):
                    continue

                lower_key = group.lower()
                if lower_key in SPECIAL_MULTI_TIER_KEYS or _is_case_sensitive_key(group):
                    final[family][tier].append(group)
                    continue

                existing = best_by_key.get(lower_key)
                if existing is None:
                    best_by_key[lower_key] = (tier, group)
                    final[family][tier].append(group)
                    continue

                existing_tier, _ = existing
                if tiers.index(tier) < tiers.index(existing_tier):
                    final[family][existing_tier].remove(existing[1])
                    final[family][tier].append(group)
                    best_by_key[lower_key] = (tier, group)
                elif tiers.index(tier) == tiers.index(existing_tier):
                    continue
                else:
                    continue

    return final


def compile_group_assignments(final_groups: Dict[str, Dict[str, List[str]]]) -> Dict[str, Dict[str, Dict[str, List[str]]]]:
    assignments = {
        family: {tier: {"base": [], "tv": [], "tv_inverse": [], "cr": [], "cr_inverse": []} for tier in tiers}
        for family, tiers in FAMILY_TIERS.items()
    }

    special_lookup = {
        family: {
            group: rule
            for rule in rules
            for group in rule["groups"]
        }
        for family, rules in SPECIAL_CASES.items()
    }

    for family, tiers in FAMILY_TIERS.items():
        for tier in tiers:
            for group in final_groups[family][tier]:
                rule = special_lookup.get(family, {}).get(group)
                if rule is None:
                    assignments[family][tier]["base"].append(group)
                    continue

                if rule["kind"] == "tv_split":
                    if tier == rule["series_tier"]:
                        assignments[family][tier]["tv"].append(group)
                    if tier == rule["movie_tier"]:
                        assignments[family][tier]["tv_inverse"].append(group)
                elif rule["kind"] == "cr_split":
                    if tier == rule["marked_tier"]:
                        assignments[family][tier]["cr"].append(group)
                    if tier == rule["unmarked_tier"]:
                        assignments[family][tier]["cr_inverse"].append(group)
                else:
                    raise RuntimeError(f"Unsupported special rule kind: {rule['kind']}")

    return assignments


def family_gate(family: str) -> str:
    if family == "REMUX":
        return rf"(?=.*{REMUX_DETECTOR})"
    if family == "BLU-RAY":
        return rf"(?=.*{BLURAY_DETECTOR})(?!.*{REMUX_DETECTOR})(?!.*{WEB_DETECTOR})"
    if family == "WEB":
        return rf"(?=.*{WEB_DETECTOR})"
    raise RuntimeError(f"Unknown family: {family}")


def _wrap_group(group: str) -> str:
    escaped = re.escape(group)
    if _is_case_sensitive_key(group):
        return f"(?-i:{escaped})"
    return escaped


def group_alt(groups: Sequence[str]) -> str:
    return "|".join(_wrap_group(group) for group in groups)


def is_strict_group(group: str) -> bool:
    return len(group) <= 3 or group.lower() in STRICT_GROUPS


def build_group_slot(groups: Sequence[str]) -> str:
    if not groups:
        return ""

    safe_groups = [group for group in groups if not is_strict_group(group)]
    strict_groups = [group for group in groups if is_strict_group(group)]
    variants: List[str] = []

    if safe_groups:
        alt = group_alt(safe_groups)
        variants.append(
            rf"(?:^\[(?:{alt})\](?=\s|$|[\[\(._-])|^\((?:{alt})\)(?=\s|$|[\[\(._-])|"
            rf"(?:\[(?:{alt})\]|\((?:{alt})\)|(?:(?<=-)|(?<=_)|(?<=\.)|(?<=\s-\s))(?:{alt})"
            rf"(?:(?:[._-](?:[A-Za-z0-9][A-Za-z0-9+&-]{{1,19}})){{0,3}})){GROUP_END_BOUNDARY})"
        )

    if strict_groups:
        alt = group_alt(strict_groups)
        variants.append(
            rf"(?:^\[(?:{alt})\](?=\s|$|[\[\(._-])|^\((?:{alt})\)(?=\s|$|[\[\(._-])|"
            rf"(?:\[(?:{alt})\]|\((?:{alt})\)|(?:(?<=-)|(?<=_)|(?<=\.))(?:{alt})){GROUP_END_BOUNDARY})"
        )

    return rf"(?:{'|'.join(variants)})"


def build_tier_cases(assignment: Mapping[str, List[str]]) -> List[str]:
    cases: List[str] = []

    for key in ("base",):
        groups = assignment[key]
        if groups:
            cases.append(rf"(?=.*{build_group_slot(groups)})")

    if assignment["tv"]:
        cases.append(rf"(?=.*{TV_MARKER})(?=.*{build_group_slot(assignment['tv'])})")
    if assignment["tv_inverse"]:
        cases.append(rf"(?!.*{TV_MARKER})(?=.*{build_group_slot(assignment['tv_inverse'])})")
    if assignment["cr"]:
        cases.append(rf"(?=.*{CR_MARKER})(?=.*{build_group_slot(assignment['cr'])})")
    if assignment["cr_inverse"]:
        cases.append(rf"(?!.*{CR_MARKER})(?=.*{build_group_slot(assignment['cr_inverse'])})")

    return cases


def build_family_patterns(assignments: Dict[str, Dict[str, Dict[str, List[str]]]]) -> Dict[str, str]:
    return build_family_patterns_with_gates(assignments, {})


def build_family_patterns_with_gates(
    assignments: Dict[str, Dict[str, Dict[str, List[str]]]],
    gate_overrides: Mapping[str, str],
) -> Dict[str, str]:
    patterns: Dict[str, str] = {}

    for family, tiers in FAMILY_TIERS.items():
        tier_cases = {
            tier: build_tier_cases(assignments[family][tier])
            for tier in tiers
        }
        gate = gate_overrides.get(family, family_gate(family))

        for index, tier in enumerate(tiers):
            higher_cases = [case for better in tiers[:index] for case in tier_cases[better]]
            current_cases = tier_cases[tier]
            if not current_cases:
                raise RuntimeError(f"No generated cases for {family} {tier}.")

            parts = [r"(?i)^", gate]
            if higher_cases:
                parts.append(rf"(?!{'|'.join(higher_cases)})")
            parts.append(rf"(?:{'|'.join(current_cases)}).*$")
            patterns[f"{family} {tier}"] = "".join(parts)

        all_ranked_cases = [case for tier in tiers for case in tier_cases[tier]]
        patterns[f"{family} Unranked"] = rf"(?i)^{gate}(?!{'|'.join(all_ranked_cases)}).*$"

    return patterns


def top_level_group_ranges(pattern: str) -> List[tuple[int, int]]:
    ranges: List[tuple[int, int]] = []
    depth = 0
    start = -1
    index = 0

    while index < len(pattern):
        char = pattern[index]
        if char == "\\":
            index += 2
            continue
        if char == "(":
            if depth == 0:
                start = index
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0 and start != -1:
                ranges.append((start, index + 1))
        index += 1

    return ranges


def extract_family_gates(target_json: Dict[str, object]) -> Dict[str, str]:
    target_filters = target_json.get("filters")
    if not isinstance(target_filters, list):
        raise RuntimeError("Target file format changed: top-level 'filters' array missing.")

    patterns_by_name = {
        item.get("name"): item.get("pattern")
        for item in target_filters
        if isinstance(item, dict) and isinstance(item.get("name"), str) and isinstance(item.get("pattern"), str)
    }

    gates: Dict[str, str] = {}
    for family, tiers in FAMILY_TIERS.items():
        first_tier_name = f"{family} {tiers[0]}"
        pattern = patterns_by_name.get(first_tier_name)
        if not isinstance(pattern, str):
            raise RuntimeError(f"Target file missing source filter '{first_tier_name}'.")
        if not pattern.startswith("(?i)^"):
            raise RuntimeError(f"Unexpected source-pattern prefix for '{first_tier_name}'.")

        groups = top_level_group_ranges(pattern)
        if not groups:
            raise RuntimeError(f"Unable to parse source pattern structure for '{first_tier_name}'.")

        final_case_start = groups[-1][0]
        gates[family] = pattern[len("(?i)^"):final_case_start]

    return gates


def sample_release_name(family: str, group: str, mode: str) -> str:
    if family == "REMUX":
        base = f"Movie.2025.2160p.UHD.Remux.x265-{group}.mkv"
        tv = f"Show.S01E01.2160p.UHD.Remux.x265-{group}.mkv"
        samples = {"movie": base, "tv": tv}
    elif family == "BLU-RAY":
        base = f"Movie.2025.1080p.BluRay.x264-{group}.mkv"
        tv = f"Show.S01E01.1080p.BluRay.x264-{group}.mkv"
        samples = {"movie": base, "tv": tv}
    elif family == "WEB":
        base = f"Movie.2025.1080p.WEB-DL.x265-{group}.mkv"
        tv = f"Show.S01E01.1080p.WEB-DL.x265-{group}.mkv"
        samples = {
            "movie": base,
            "tv": tv,
            "cr_movie": f"Movie.2025.1080p.CR.WEB-DL.x265-{group}.mkv",
            "cr_tv": f"Show.S01E01.1080p.CR.WEB-DL.x265-{group}.mkv",
        }
    else:
        raise RuntimeError(f"Unknown family: {family}")

    return samples[mode]


def semantic_source_group_changes(
    target_json: Dict[str, object],
    generated_patterns: Mapping[str, str],
    final_groups: Dict[str, Dict[str, List[str]]],
) -> List[str]:
    target_filters = target_json.get("filters")
    if not isinstance(target_filters, list):
        raise RuntimeError("Target file format changed: top-level 'filters' array missing.")

    current_patterns = {
        item["name"]: re.compile(item["pattern"])
        for item in target_filters
        if isinstance(item, dict)
        and isinstance(item.get("name"), str)
        and item["name"] in generated_patterns
        and isinstance(item.get("pattern"), str)
    }
    generated_compiled = {name: re.compile(pattern) for name, pattern in generated_patterns.items()}

    mismatches: List[str] = []
    for family, tiers in FAMILY_TIERS.items():
        names = [f"{family} {tier}" for tier in tiers] + [f"{family} Unranked"]
        candidate_groups = sorted({group for tier_groups in final_groups[family].values() for group in tier_groups})
        modes = ["movie", "tv"] + (["cr_movie", "cr_tv"] if family == "WEB" else [])

        for group in candidate_groups:
            for mode in modes:
                sample = sample_release_name(family, group, mode)
                current_hits = [name for name in names if current_patterns[name].search(sample)]
                generated_hits = [name for name in names if generated_compiled[name].search(sample)]
                if current_hits != generated_hits:
                    mismatches.append(
                        f"{family}:{group}:{mode}:{','.join(current_hits) or '-'}->{','.join(generated_hits) or '-'}"
                    )

    return mismatches


def resolve_template_path(target_path: Path, explicit_template: str | None) -> Path:
    if target_path.name.endswith("-copy.json"):
        raise RuntimeError(
            f"{target_path.name} is a copy template file. Run the updater against the non-copy target instead."
        )

    if explicit_template:
        return Path(explicit_template)

    template = TARGET_TEMPLATE_MAP.get(target_path.name)
    if template is None:
        raise RuntimeError(
            f"No template mapping configured for {target_path.name}. Use --template-file to specify one."
        )
    return template


def apply_patterns_to_target(
    target_json: Dict[str, object],
    template_json: Dict[str, object],
    generated_patterns: Mapping[str, str],
) -> Dict[str, object]:
    target_filters = target_json.get("filters")
    template_filters = template_json.get("filters")
    if not isinstance(target_filters, list) or not isinstance(template_filters, list):
        raise RuntimeError("Target/template file format changed: top-level 'filters' array missing.")

    generated_names = set(generated_patterns)
    new_filters: List[Dict[str, object]] = []

    for item in template_filters:
        if not isinstance(item, dict):
            continue
        name = item.get("name")
        if not isinstance(name, str) or name not in generated_names:
            continue
        new_item = copy.deepcopy(item)
        new_item["pattern"] = generated_patterns[name]
        new_filters.append(new_item)

    source_names_present = {item["name"] for item in new_filters if isinstance(item.get("name"), str)}
    missing = generated_names - source_names_present
    if missing:
        raise RuntimeError(f"Template file is missing source filters: {sorted(missing)}")

    for item in target_filters:
        if not isinstance(item, dict):
            continue
        name = item.get("name")
        if isinstance(name, str) and name in generated_names:
            continue
        new_filters.append(item)

    updated = copy.deepcopy(target_json)
    updated["filters"] = new_filters
    return updated


def main() -> int:
    args = parse_args()
    target_path = Path(args.target_file)
    template_path = resolve_template_path(target_path, args.template_file)

    entries = fetch_upstream_entries(args.source_url)
    merged = merge_source_groups(entries)
    resolved = resolve_tier_conflicts(merged)
    assignments = compile_group_assignments(resolved)

    target_json = json.loads(target_path.read_text(encoding="utf-8"))
    template_json = json.loads(template_path.read_text(encoding="utf-8"))
    gate_overrides = extract_family_gates(target_json)
    generated_patterns = build_family_patterns_with_gates(assignments, gate_overrides)

    semantic_mismatches = semantic_source_group_changes(target_json, generated_patterns, resolved)
    if not semantic_mismatches:
        print(f"No release-group changes needed for {target_path}")
        return 0

    updated_json = apply_patterns_to_target(target_json, template_json, generated_patterns)

    updated_text = json.dumps(updated_json, indent=2, ensure_ascii=False) + "\n"
    current_text = target_path.read_text(encoding="utf-8")
    if updated_text != current_text:
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
        sys.exit(1)
