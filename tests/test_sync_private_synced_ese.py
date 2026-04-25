import copy
import unittest

from scripts.sync_private_synced_ese import sync_target_data


class SyncPrivateSyncedESETests(unittest.TestCase):
    def test_only_whitelisted_rules_and_version_are_updated(self):
        target = {
            "metadata": {
                "name": "excludedStreamExpressions (Standard)",
                "author": "Bot-Bid-Raiser",
                "description": "local test",
                "version": "1.2.5",
            },
            "values": [
                "/*G's Low Bitrate*/local-g",
                "/*ongoingSeasonPack*/local-ongoing",
                "/*Low Seeders*/local-seeders",
                "/*Extra SeaDex*/local-seadex",
                "/*Bad 4k Anime*/local-bad-anime",
                "/*Upscaled 4k*/local-upscaled",
                "/*Bad 4k Bluray*/local-bad-bluray",
                "/*Bad 1080P Bluray*/local-bad-1080",
                "/*⚠️ Bad NZBs*/keep-me",
                "/*⚠️ Extra Cached (HQ)*/keep-me-too",
            ],
        }
        original = copy.deepcopy(target)

        upstream = [
            {"expression": "/*Part of Tamtaro SEL Setup*/[]", "enabled": True},
            {"expression": "/*Standard ESE v1.2.6 [git.tamtaro.de]*/[]", "enabled": True},
            {"expression": "/*G's Low Bitrate*/upstream-g", "enabled": True},
            {"expression": "/*No Sootio Library*/upstream-sootio", "enabled": True},
            {"expression": "/*ongoingSeasonPack*/upstream-ongoing", "enabled": True},
            {"expression": "/*Low Seeders*/upstream-seeders", "enabled": True},
            {"expression": "/*Extra SeaDex*/upstream-seadex", "enabled": True},
            {"expression": "/*Bad 4k Anime*/upstream-bad-anime", "enabled": True},
            {"expression": "/*Upscaled 4k*/upstream-upscaled", "enabled": True},
            {"expression": "/*Bad 4k Bluray*/upstream-bad-bluray", "enabled": True},
            {"expression": "/*Bad 1080P Bluray*/upstream-bad-1080", "enabled": True},
            {"expression": "/*⚠️ Bad NZBs*/upstream-warning", "enabled": True},
        ]

        changed, missing = sync_target_data(target, upstream)

        self.assertTrue(changed)
        self.assertEqual(missing, ["No Sootio Library"])
        self.assertEqual(target["metadata"]["version"], "1.2.6")
        self.assertEqual(
            target["values"][:8],
            [
                "/*G's Low Bitrate*/upstream-g",
                "/*ongoingSeasonPack*/upstream-ongoing",
                "/*Low Seeders*/upstream-seeders",
                "/*Extra SeaDex*/upstream-seadex",
                "/*Bad 4k Anime*/upstream-bad-anime",
                "/*Upscaled 4k*/upstream-upscaled",
                "/*Bad 4k Bluray*/upstream-bad-bluray",
                "/*Bad 1080P Bluray*/upstream-bad-1080",
            ],
        )
        self.assertEqual(target["values"][8], original["values"][8])
        self.assertEqual(target["values"][9], original["values"][9])

    def test_missing_target_rule_raises_helpful_error(self):
        target = {"metadata": {"version": "1.2.5"}, "values": ["/*G's Low Bitrate*/local-g"]}
        upstream = [
            {"expression": "/*G's Low Bitrate*/upstream-g", "enabled": True},
            {"expression": "/*Standard ESE v1.2.6 [git.tamtaro.de]*/[]", "enabled": True},
        ]

        with self.assertRaisesRegex(RuntimeError, "missing upstream rule 'No Sootio Library'"):
            sync_target_data(target, upstream)


if __name__ == "__main__":
    unittest.main()
