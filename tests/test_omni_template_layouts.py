import base64
import json
import os
import re
import unittest
from pathlib import Path


class OmniTemplateLayoutTests(unittest.TestCase):
    def test_portrait_catalogs_tracks_the_non_landscape_catalogs(self):
        template_path = self._latest_omni_template_path()
        template = json.loads(template_path.read_text(encoding="utf-8"))
        included_keys = template["includedKeys"]
        values = template["values"]

        self.assertIn("portrait_catalogs", included_keys)

        selected = set(json.loads(base64.b64decode(values["selected_catalogs"]["_data"]).decode("utf-8")))
        landscape = set(json.loads(base64.b64decode(values["landscape_catalogs"]["_data"]).decode("utf-8")))
        portrait = set(json.loads(base64.b64decode(values["portrait_catalogs"]["_data"]).decode("utf-8")))

        self.assertTrue(portrait, "portrait_catalogs should not be empty")
        self.assertTrue(portrait.isdisjoint(landscape))
        self.assertEqual(selected, portrait | landscape)

    def _latest_omni_template_path(self) -> Path:
        pattern = re.compile(r"^ume-omni-template-v(\d+(?:\.\d+)*)\.json$")
        from_env = os.getenv("OMNI_TEMPLATE_FILE")
        if from_env:
            path = Path(from_env)
            self.assertTrue(path.is_file(), f"OMNI_TEMPLATE_FILE does not exist: {from_env}")
            self.assertIsNotNone(
                pattern.match(path.name),
                f"OMNI_TEMPLATE_FILE must match ume-omni-template-v*.json: {from_env}",
            )
            return path

        candidates = []
        for path in Path(".").glob("ume-omni-template-v*.json"):
            match = pattern.match(path.name)
            if not match:
                continue
            version = tuple(int(part) for part in match.group(1).split("."))
            candidates.append((version, path))

        self.assertTrue(candidates, "No omni template files found")
        return max(candidates, key=lambda item: item[0])[1]
