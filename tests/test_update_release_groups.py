import json
import unittest

from scripts.update_release_groups import (
    UpstreamEntry,
    build_updated_patterns,
    extract_groups_from_pattern,
    merge_source_groups,
    resolve_tier_conflicts,
    update_patterns_in_raw_json,
)


def _target_pattern(name: str, groups: str) -> dict:
    return {
        "name": name,
        "pattern": rf"(?=.*\b(?:{groups})\b)|{name}",
        "type": "filter",
    }


class UpdateReleaseGroupsTests(unittest.TestCase):
    def test_extract_groups_from_pattern(self):
        pattern = r"/^(?=.*\\b(?:ABBIE|ABBiE|NTb)\\b).*/i"
        self.assertEqual(extract_groups_from_pattern(pattern), ["ABBIE", "ABBiE", "NTb"])

    def test_merge_entries_across_radarr_sonarr_split(self):
        entries = [
            UpstreamEntry("Radarr Remux T1", r"/^(?=.*\\b(?:A|B)\\b).*/i"),
            UpstreamEntry("Sonarr Remux T1", r"/^(?=.*\\b(?:B|C)\\b).*/i"),
            UpstreamEntry("Radarr Remux T2", r"/^(?=.*\\b(?:D)\\b).*/i"),
            UpstreamEntry("Sonarr Remux T2", r"/^(?=.*\\b(?:E)\\b).*/i"),
            UpstreamEntry("Radarr Remux T3", r"/^(?=.*\\b(?:F)\\b).*/i"),
            UpstreamEntry("Sonarr Remux T3", r"/^(?=.*\\b(?:G)\\b).*/i"),
            UpstreamEntry("Radarr UHD Bluray T1", r"/^(?=.*\\b(?:H)\\b).*/i"),
            UpstreamEntry("Radarr HD Bluray T1", r"/^(?=.*\\b(?:I)\\b).*/i"),
            UpstreamEntry("Sonarr HD Bluray T1", r"/^(?=.*\\b(?:J)\\b).*/i"),
            UpstreamEntry("Radarr UHD Bluray T2", r"/^(?=.*\\b(?:K)\\b).*/i"),
            UpstreamEntry("Radarr HD Bluray T2", r"/^(?=.*\\b(?:L)\\b).*/i"),
            UpstreamEntry("Sonarr HD Bluray T2", r"/^(?=.*\\b(?:M)\\b).*/i"),
            UpstreamEntry("Radarr UHD Bluray T3", r"/^(?=.*\\b(?:N)\\b).*/i"),
            UpstreamEntry("Radarr HD Bluray T3", r"/^(?=.*\\b(?:O)\\b).*/i"),
            UpstreamEntry("Sonarr HD Bluray T3", r"/^(?=.*\\b(?:P)\\b).*/i"),
            UpstreamEntry("Radarr Web T1", r"/^(?=.*\\b(?:Q)\\b).*/i"),
            UpstreamEntry("Sonarr Web T1", r"/^(?=.*\\b(?:R)\\b).*/i"),
            UpstreamEntry("Web T1", r"/^(?=.*\\b(?:S)\\b).*/i"),
            UpstreamEntry("Radarr Web T2", r"/^(?=.*\\b(?:T)\\b).*/i"),
            UpstreamEntry("Sonarr Web T2", r"/^(?=.*\\b(?:U)\\b).*/i"),
            UpstreamEntry("Radarr Web T3", r"/^(?=.*\\b(?:W)\\b).*/i"),
            UpstreamEntry("Sonarr Web T3", r"/^(?=.*\\b(?:X)\\b).*/i"),
        ]

        merged = merge_source_groups(entries)
        # merge_source_groups intentionally only maps/sums source entries;
        # deduplication is tested separately in resolve_tier_conflicts.
        self.assertEqual(merged["REMUX"]["T1"], ["A", "B", "B", "C"])
        self.assertEqual(merged["BLU-RAY"]["T1"], ["H", "I", "J"])
        self.assertEqual(merged["WEB"]["T2"], ["T", "U"])

    def test_tier_conflicts_and_casing_dedupe(self):
        merged = {
            "REMUX": {
                "T1": ["FraMeSToR", "ZQ"],
                "T2": ["framestor", "Other"],
                "T3": ["ZQ", "other"],
            },
            "BLU-RAY": {"T1": [], "T2": [], "T3": []},
            "WEB": {"T1": [], "T2": [], "T3": []},
        }

        final, unranked, dedupe_logs, promotion_logs, counts = resolve_tier_conflicts(merged)

        self.assertEqual(final["REMUX"]["T1"], ["FraMeSToR", "ZQ"])
        self.assertEqual(final["REMUX"]["T2"], ["Other"])
        self.assertEqual(final["REMUX"]["T3"], [])
        self.assertEqual(unranked["REMUX"], ["FraMeSToR", "ZQ", "Other"])
        self.assertTrue(any("lower-tier duplicate" in msg for msg in dedupe_logs["REMUX"]))
        self.assertEqual(promotion_logs["REMUX"], [])
        self.assertEqual(counts["REMUX T1"], 2)

    def test_unranked_rebuild_uses_final_union(self):
        merged = {
            "REMUX": {"T1": ["A"], "T2": ["B"], "T3": ["C"]},
            "BLU-RAY": {"T1": ["D"], "T2": ["E"], "T3": ["F"]},
            "WEB": {"T1": ["G"], "T2": ["H"], "T3": ["I"]},
        }
        _, unranked, _, _, _ = resolve_tier_conflicts(merged)
        self.assertEqual(unranked["BLU-RAY"], ["D", "E", "F"])
        self.assertEqual(unranked["WEB"], ["G", "H", "I"])

    def test_build_and_apply_pattern_updates_only_release_group_segment(self):
        target = {
            "filters": [
                _target_pattern("REMUX 1", "OLD"),
                _target_pattern("REMUX 2", "OLD"),
                _target_pattern("REMUX 3", "OLD"),
                _target_pattern("REMUX Unranked", "OLD"),
                _target_pattern("BLU-RAY 1", "OLD"),
                _target_pattern("BLU-RAY 2", "OLD"),
                _target_pattern("BLU-RAY 3", "OLD"),
                _target_pattern("BLU-RAY Unranked", "OLD"),
                _target_pattern("WEB 1", "OLD"),
                _target_pattern("WEB 2", "OLD"),
                _target_pattern("WEB 3", "OLD"),
                _target_pattern("WEB Unranked", "OLD"),
                {"name": "UNCHANGED", "pattern": "foo", "type": "filter"},
            ]
        }

        final = {
            "REMUX": {"T1": ["A"], "T2": ["B"], "T3": ["C"]},
            "BLU-RAY": {"T1": ["D"], "T2": ["E"], "T3": ["F"]},
            "WEB": {"T1": ["G"], "T2": ["H"], "T3": ["I"]},
        }
        unranked = {"REMUX": ["A", "B", "C"], "BLU-RAY": ["D", "E", "F"], "WEB": ["G", "H", "I"]}

        updates = build_updated_patterns(target, final, unranked)
        raw = json.dumps(target, indent=2)
        out = update_patterns_in_raw_json(raw, updates)

        self.assertIn(r"\\b(?:A)\\b", out)
        self.assertIn(r"\\b(?:A|B|C)\\b", out)
        self.assertIn('"name": "UNCHANGED",', out)
        self.assertIn('"pattern": "foo"', out)


if __name__ == "__main__":
    unittest.main()
