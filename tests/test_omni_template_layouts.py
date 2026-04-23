import base64
import json
import unittest
from pathlib import Path


class OmniTemplateLayoutTests(unittest.TestCase):
    def test_portrait_catalogs_tracks_the_non_landscape_catalogs(self):
        template = json.loads(Path("ume-omni-template-v3.1.json").read_text(encoding="utf-8"))
        included_keys = template["includedKeys"]
        values = template["values"]

        self.assertIn("portrait_catalogs", included_keys)

        selected = set(json.loads(base64.b64decode(values["selected_catalogs"]["_data"]).decode("utf-8")))
        landscape = set(json.loads(base64.b64decode(values["landscape_catalogs"]["_data"]).decode("utf-8")))
        portrait = set(json.loads(base64.b64decode(values["portrait_catalogs"]["_data"]).decode("utf-8")))

        self.assertTrue(portrait, "portrait_catalogs should not be empty")
        self.assertTrue(portrait.isdisjoint(landscape))
        self.assertEqual(selected, portrait | landscape)

