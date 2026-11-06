import importlib.util
import sys
import types
import unittest
from collections import defaultdict
from pathlib import Path

module_path = Path(__file__).resolve().parents[1] / "sketchup_imparator" / "SKPutil" / "__init__.py"

spec = importlib.util.spec_from_file_location("sketchup_imparator.SKPutil", module_path)
sketchup_imparator_skputil = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = sketchup_imparator_skputil
spec.loader.exec_module(sketchup_imparator_skputil)

clear_import_state = sketchup_imparator_skputil.clear_import_state
proxy_dict = sketchup_imparator_skputil.proxy_dict


class DummyImportState:
    pass


class ImportStateCleanupTests(unittest.TestCase):
    def test_clear_import_state_resets_runtime_caches(self):
        state = DummyImportState()
        state.component_meshes = {"old": object()}
        state.skp_components = {"old": object()}
        state.component_depth = {"old": 1}
        state.mesh_cache = {"old": object()}
        state.materials = {"old": object()}
        state.name_mapping = {"old": "value"}
        state.component_skip = {"skip": object()}
        state.component_stats = defaultdict(list, {"a": [1]})
        state.instance_counts = defaultdict(int, {"b": 2})
        state.group_written = {"group": object()}
        state.layers_skip = ["old"]

        clear_import_state(state)

        self.assertEqual(state.component_meshes, {})
        self.assertEqual(state.skp_components, {})
        self.assertEqual(state.component_depth, {})
        self.assertEqual(state.mesh_cache, {})
        self.assertEqual(state.materials, {})
        self.assertEqual(state.name_mapping, {})
        self.assertIsInstance(state.component_skip, proxy_dict)
        self.assertEqual(state.component_skip, {})
        self.assertIsInstance(state.component_stats, defaultdict)
        self.assertEqual(state.component_stats, defaultdict(list))
        self.assertIsInstance(state.instance_counts, defaultdict)
        self.assertEqual(state.instance_counts, defaultdict(int))
        self.assertEqual(state.group_written, {})
        self.assertEqual(state.layers_skip, [])


if __name__ == "__main__":
    unittest.main()
