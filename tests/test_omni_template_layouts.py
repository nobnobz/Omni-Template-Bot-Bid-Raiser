import base64
import json
import unittest
from pathlib import Path


class OmniTemplateLayoutTests(unittest.TestCase):
    def test_studios_keeps_its_stable_id_when_layout_changes(self):
        v30 = json.loads(Path("Older Versions/v3.0/ume-omni-template-v3.0.json").read_text(encoding="utf-8"))
        v31 = json.loads(Path("ume-omni-template-v3.1.json").read_text(encoding="utf-8"))

        old_groups = json.loads(base64.b64decode(v30["values"]["main_catalog_groups"]["_data"]).decode("utf-8"))
        new_groups = json.loads(base64.b64decode(v31["values"]["main_catalog_groups"]["_data"]).decode("utf-8"))

        old_studios_id = next(key for key, value in old_groups.items() if value["name"] == "Studios")
        new_studios_id = next(key for key, value in new_groups.items() if value["name"] == "Studios")

        self.assertEqual(old_studios_id, new_studios_id)
        self.assertEqual(new_groups[new_studios_id]["posterType"], "Landscape")
        self.assertEqual(v31["values"]["main_group_order"][6], new_studios_id)

    def test_group_id_references_are_consistent(self):
        v31 = json.loads(Path("ume-omni-template-v3.1.json").read_text(encoding="utf-8"))

        main_groups = json.loads(base64.b64decode(v31["values"]["main_catalog_groups"]["_data"]).decode("utf-8"))
        subgroup_order = json.loads(base64.b64decode(v31["values"]["subgroup_order"]["_data"]).decode("utf-8"))

        self.assertEqual(set(main_groups.keys()), set(subgroup_order.keys()))
        self.assertFalse(any(key.startswith("fusion-") for key in main_groups.keys()))
        self.assertFalse(any(key.startswith("fusion-") for key in subgroup_order.keys()))
