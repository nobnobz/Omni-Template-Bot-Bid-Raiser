import re
import unittest
from pathlib import Path

from scripts.update_release_groups import (
    UpstreamEntry,
    apply_patterns_to_target,
    build_family_patterns,
    build_family_patterns_with_gates,
    extract_family_gates,
    compile_group_assignments,
    extract_groups_from_pattern,
    family_gate,
    merge_source_groups,
    resolve_template_path,
    resolve_tier_conflicts,
    semantic_source_group_changes,
)


def _source_filter(name: str) -> dict:
    return {
        "name": name,
        "pattern": "placeholder",
        "type": "filter",
        "groupId": "source-group",
        "id": name.lower().replace(" ", "-"),
    }


class UpdateReleaseGroupsTests(unittest.TestCase):
    def test_copy_targets_are_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "copy template file"):
            resolve_template_path(Path("Other/fusion-tags-ume-copy.json"), None)

    def test_minimalistic_target_uses_self_template(self):
        self.assertEqual(
            resolve_template_path(Path("Other/fustion-tags-ume-minimalistic.json"), None),
            Path("Other/fustion-tags-ume-minimalistic.json"),
        )

    def test_extract_groups_from_pattern(self):
        pattern = r"/^(?=.*\\b(?:ABBIE|ABBiE|NTb)\\b).*/i"
        self.assertEqual(extract_groups_from_pattern(pattern), ["ABBIE", "ABBiE", "NTb"])

    def test_extract_groups_from_slot_style_anime_pattern(self):
        pattern = (
            r"/^(?=.*(BluRay|Blu-Ray))(?=.*(\[(Moxie|smol|SoM)\]|-(Moxie|smol|SoM)\b|"
            r"\b(DemiHuman|FLE|Flugel|LYS1TH3A|ZR)\b|(?<=remux).*\b(NAN0)\b|-ZR-)).*/i"
        )
        self.assertCountEqual(
            extract_groups_from_pattern(pattern),
            ["Moxie", "smol", "SoM", "DemiHuman", "FLE", "Flugel", "LYS1TH3A", "ZR", "NAN0"],
        )

    def test_merge_entries_supports_copy_tiers(self):
        entries = [
            UpstreamEntry("Radarr Remux T1", r"/^(?=.*\\b(?:A)\\b).*/i"),
            UpstreamEntry("Sonarr Remux T1", r"/^(?=.*\\b(?:B)\\b).*/i"),
            UpstreamEntry("Radarr Remux T2", r"/^(?=.*\\b(?:C)\\b).*/i"),
            UpstreamEntry("Sonarr Remux T2", r"/^(?=.*\\b(?:D)\\b).*/i"),
            UpstreamEntry("Radarr Remux T3", r"/^(?=.*\\b(?:E)\\b).*/i"),
            UpstreamEntry("Radarr UHD Bluray T1", r"/^(?=.*\\b(?:F)\\b).*/i"),
            UpstreamEntry("Radarr HD Bluray T1", r"/^(?=.*\\b(?:G)\\b).*/i"),
            UpstreamEntry("Sonarr HD Bluray T1", r"/^(?=.*\\b(?:H)\\b).*/i"),
            UpstreamEntry("Anime BD T1", r"/^(?=.*\\b(?:I)\\b).*/i"),
            UpstreamEntry("Anime BD T8", r"/^(?=.*\\b(?:J)\\b).*/i"),
            UpstreamEntry("Radarr Web T1", r"/^(?=.*\\b(?:K)\\b).*/i"),
            UpstreamEntry("Sonarr Web T1", r"/^(?=.*\\b(?:L)\\b).*/i"),
            UpstreamEntry("Web T1", r"/^(?=.*\\b(?:M)\\b).*/i"),
            UpstreamEntry("Anime Web T1", r"/^(?=.*\\b(?:N)\\b).*/i"),
            UpstreamEntry("Anime Web T6", r"/^(?=.*\\b(?:O)\\b).*/i"),
            UpstreamEntry("Radarr UHD Bluray T2", r"/^(?=.*\\b(?:P)\\b).*/i"),
            UpstreamEntry("Radarr HD Bluray T2", r"/^(?=.*\\b(?:Q)\\b).*/i"),
            UpstreamEntry("Sonarr HD Bluray T2", r"/^(?=.*\\b(?:R)\\b).*/i"),
            UpstreamEntry("Anime BD T2", r"/^(?=.*\\b(?:S)\\b).*/i"),
            UpstreamEntry("Radarr UHD Bluray T3", r"/^(?=.*\\b(?:T)\\b).*/i"),
            UpstreamEntry("Radarr HD Bluray T3", r"/^(?=.*\\b(?:U)\\b).*/i"),
            UpstreamEntry("Anime BD T3", r"/^(?=.*\\b(?:V)\\b).*/i"),
            UpstreamEntry("Anime BD T4", r"/^(?=.*\\b(?:W)\\b).*/i"),
            UpstreamEntry("Anime BD T5", r"/^(?=.*\\b(?:X)\\b).*/i"),
            UpstreamEntry("Anime BD T6", r"/^(?=.*\\b(?:Y)\\b).*/i"),
            UpstreamEntry("Anime BD T7", r"/^(?=.*\\b(?:Z)\\b).*/i"),
            UpstreamEntry("Radarr Web T2", r"/^(?=.*\\b(?:AA)\\b).*/i"),
            UpstreamEntry("Sonarr Web T2", r"/^(?=.*\\b(?:AB)\\b).*/i"),
            UpstreamEntry("Anime Web T2", r"/^(?=.*\\b(?:AC)\\b).*/i"),
            UpstreamEntry("Radarr Web T3", r"/^(?=.*\\b(?:AD)\\b).*/i"),
            UpstreamEntry("Sonarr Web T3", r"/^(?=.*\\b(?:AE)\\b).*/i"),
            UpstreamEntry("Anime Web T3", r"/^(?=.*\\b(?:AF)\\b).*/i"),
            UpstreamEntry("Anime Web T4", r"/^(?=.*\\b(?:AG)\\b).*/i"),
            UpstreamEntry("Anime Web T5", r"/^(?=.*\\b(?:AH)\\b).*/i"),
        ]

        merged = merge_source_groups(entries)
        self.assertEqual(merged["REMUX"]["1"], ["A", "B"])
        self.assertEqual(merged["BLU-RAY"]["1"], ["F", "G", "H", "I"])
        self.assertEqual(merged["BLU-RAY"]["8"], ["J"])
        self.assertEqual(merged["WEB"]["1"], ["K", "L", "M", "N"])
        self.assertEqual(merged["WEB"]["6"], ["O"])

    def test_resolve_conflicts_preserves_marker_split_groups(self):
        merged = {
            "REMUX": {"1": [], "2": ["TRiToN"], "3": ["TRiToN"]},
            "BLU-RAY": {"1": ["NTb"], "2": ["NTb", "Remux"], "3": [], "4": [], "5": [], "6": [], "7": [], "8": []},
            "WEB": {
                "1": ["Kitsune"],
                "2": ["playWEB", "SIGMA", "SiGMA"],
                "3": ["Kitsune", "SiGMA"],
                "4": ["WEB"],
                "5": ["PlayWeb"],
                "6": [],
            },
        }

        final = resolve_tier_conflicts(merged)

        self.assertEqual(final["REMUX"]["2"], ["TRiToN"])
        self.assertEqual(final["REMUX"]["3"], ["TRiToN"])
        self.assertEqual(final["BLU-RAY"]["1"], ["NTb"])
        self.assertEqual(final["BLU-RAY"]["2"], ["NTb"])
        self.assertEqual(final["WEB"]["2"], ["playWEB", "SIGMA", "SiGMA"])
        self.assertEqual(final["WEB"]["3"], ["Kitsune", "SiGMA"])
        self.assertEqual(final["WEB"]["5"], ["PlayWeb"])

    def test_generated_web_patterns_cover_edge_cases(self):
        merged = {
            "REMUX": {"1": ["FraMeSToR"], "2": ["TRiToN"], "3": ["SumVision"]},
            "BLU-RAY": {
                "1": ["CtrlHD"],
                "2": ["NTb"],
                "3": ["HONE"],
                "4": ["AnimeOne"],
                "5": ["AnimeTwo"],
                "6": ["AnimeThree"],
                "7": ["AnimeFour"],
                "8": ["AnimeFive"],
            },
            "WEB": {
                "1": ["BYNDR", "HONE", "Kitsune"],
                "2": ["BLUTONiUM", "playWEB", "SIGMA"],
                "3": ["SiGMA", "Kitsune"],
                "4": ["Erai-raws"],
                "5": ["PlayWeb"],
                "6": ["T4H"],
            },
        }

        assignments = compile_group_assignments(resolve_tier_conflicts(merged))
        patterns = build_family_patterns(assignments)

        self.assertRegex(
            "Anaconda.2025.2160p.iT.WEB-DL.DDP5.1.Atmos.DV.HDR.H.265-BYNDR.DUAL-andrehsa.mkv",
            re.compile(patterns["WEB 1"]),
        )
        self.assertRegex(
            "The Pitt (2025) S01E02 (2160p MAX WEB-DL H265 DV HDR DDP Atmos 5.1 English - HONE).mkv",
            re.compile(patterns["WEB 1"]),
        )
        self.assertRegex(
            "Show.S01E01.1080p.WEB-DL.x265-BLUTONiUM.mkv",
            re.compile(patterns["WEB 2"]),
        )
        self.assertRegex(
            "Movie.2025.1080p.WEB-DL.x265-SiGMA.mkv",
            re.compile(patterns["WEB 3"]),
        )
        self.assertRegex(
            "[Erai-raws] Saikyou no Ousama - 01 [1080p CR WEBRip HEVC EAC3][MultiSub].mkv",
            re.compile(patterns["WEB 4"]),
        )
        self.assertRegex(
            "Anime.2025.1080p.CR.WEB-DL.x265-playWEB.mkv",
            re.compile(patterns["WEB 5"]),
        )
        self.assertRegex(
            "Show.S01E01.1080p.WEB-DL.x265-SIGMA.mkv",
            re.compile(patterns["WEB 2"]),
        )
        self.assertRegex(
            "Movie.2025.1080p.WEB-DL.x265-T4H.mkv",
            re.compile(patterns["WEB 6"]),
        )
        self.assertRegex(
            "Movie.2025.1080p.WEB-DL.x265-randomgroup.mkv",
            re.compile(patterns["WEB Unranked"]),
        )
        self.assertNotRegex(
            "The.Beginning.After.the.End.S01E01.1080p.CR.WEB-DL.DUAL.DDP2.0.H.264-Kitsune.mkv",
            re.compile(patterns["WEB 1"]),
        )
        self.assertRegex(
            "The.Beginning.After.the.End.S01E01.1080p.CR.WEB-DL.DUAL.DDP2.0.H.264-Kitsune.mkv",
            re.compile(patterns["WEB 3"]),
        )

    def test_apply_patterns_to_target_uses_template_source_filters(self):
        target = {
            "filters": [
                _source_filter("REMUX 1"),
                _source_filter("REMUX 2"),
                _source_filter("REMUX 3"),
                _source_filter("REMUX Unranked"),
                _source_filter("BLU-RAY 1"),
                _source_filter("BLU-RAY 2"),
                _source_filter("BLU-RAY 3"),
                _source_filter("BLU-RAY Unranked"),
                _source_filter("WEB 1"),
                _source_filter("WEB 2"),
                _source_filter("WEB 3"),
                _source_filter("WEB 4"),
                _source_filter("WEB 5"),
                _source_filter("WEB Unranked"),
                {"name": "HDR", "pattern": "hdr", "type": "filter"},
            ]
        }
        template = {
            "filters": [_source_filter(name) for name in (
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
            )]
        }
        generated = {name: f"pattern for {name}" for name in [item["name"] for item in template["filters"]]}

        updated = apply_patterns_to_target(target, template, generated)
        updated_names = [item["name"] for item in updated["filters"]]

        self.assertIn("BLU-RAY 8", updated_names)
        self.assertIn("WEB 6", updated_names)
        self.assertEqual(updated["filters"][-1]["name"], "HDR")
        web6 = next(item for item in updated["filters"] if item["name"] == "WEB 6")
        self.assertEqual(web6["pattern"], "pattern for WEB 6")

    def test_extract_family_gates_from_current_source_patterns(self):
        target = {
            "filters": [
                _source_filter("REMUX 1") | {"pattern": r"(?i)^(?=.*REMUXSOURCE)(?:(?=.*A)).*$"},
                _source_filter("BLU-RAY 1") | {"pattern": r"(?i)^(?=.*BLURAYSOURCE)(?!.*REMUX)(?:(?=.*B)).*$"},
                _source_filter("WEB 1") | {"pattern": r"(?i)^(?=.*WEBSOURCE)(?!.*REMUX)(?:(?=.*C)).*$"},
            ]
        }

        gates = extract_family_gates(target)
        self.assertEqual(gates["REMUX"], r"(?=.*REMUXSOURCE)")
        self.assertEqual(gates["BLU-RAY"], r"(?=.*BLURAYSOURCE)(?!.*REMUX)")
        self.assertEqual(gates["WEB"], r"(?=.*WEBSOURCE)(?!.*REMUX)")

    def test_semantic_change_check_ignores_text_only_gate_differences(self):
        merged = {
            "REMUX": {"1": ["FraMeSToR"], "2": ["TRiToN"], "3": ["SumVision"]},
            "BLU-RAY": {
                "1": ["CtrlHD"],
                "2": ["NTb"],
                "3": ["HONE"],
                "4": ["AnimeOne"],
                "5": ["AnimeTwo"],
                "6": ["AnimeThree"],
                "7": ["AnimeFour"],
                "8": ["AnimeFive"],
            },
            "WEB": {
                "1": ["BYNDR", "Kitsune"],
                "2": ["BLUTONiUM", "playWEB", "SIGMA"],
                "3": ["SiGMA"],
                "4": ["Erai-raws"],
                "5": ["PlayWeb"],
                "6": ["T4H"],
            },
        }
        resolved = resolve_tier_conflicts(merged)
        assignments = compile_group_assignments(resolved)
        generated = build_family_patterns(assignments)
        target_patterns = build_family_patterns_with_gates(
            assignments,
            {
                "REMUX": family_gate("REMUX") + r"(?!.*UNLIKELYMARKER)",
                "BLU-RAY": family_gate("BLU-RAY") + r"(?!.*UNLIKELYMARKER)",
                "WEB": family_gate("WEB") + r"(?!.*UNLIKELYMARKER)",
            },
        )

        target = {
            "filters": [
                _source_filter(name) | {"pattern": target_patterns[name]}
                for name in target_patterns
            ]
        }

        self.assertEqual(semantic_source_group_changes(target, target_patterns, resolved), [])
        self.assertEqual(semantic_source_group_changes(target, generated, resolved), [])


if __name__ == "__main__":
    unittest.main()
