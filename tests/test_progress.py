"""Exercise Maya command boundaries with a mock; no host qualification implied."""
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import Mock, patch


class ProgressTests(unittest.TestCase):
    def setUp(self):
        self.commands = Mock()
        self.commands.progressWindow.return_value = False
        maya = types.ModuleType('maya')
        maya.cmds = self.commands
        path = Path(__file__).resolve().parents[1] / 'max_payne_maya/progress_bar.py'
        spec = importlib.util.spec_from_file_location('tested_progress', str(path))
        self.progress = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, {'maya': maya, 'maya.cmds': self.commands}):
            spec.loader.exec_module(self.progress)

    def test_zero_operations_do_not_divide_by_zero(self):
        self.progress.init(0)
        self.progress.show()
        self.assertTrue(self.progress.update())

    def test_cancellation_aborts_outer_import_phases(self):
        self.progress.init(10)
        self.commands.progressWindow.return_value = True
        completed = []
        with self.assertRaises(self.progress.ImportCancelled):
            self.progress.update()
            completed.append('geometry phase')
        self.assertEqual([], completed)

    def test_completion_keeps_window_until_importer_cleanup(self):
        self.progress.init(1)
        self.progress.update()
        self.commands.progressWindow.assert_called_with(edit=True, progress=100, status='')
        self.progress.hide()
        self.commands.progressWindow.assert_called_with(endProgress=1)

    def test_reinitialize_resets_progress(self):
        self.progress.init(1)
        self.progress.update()
        self.progress.init(4)
        self.progress.update()
        self.commands.progressWindow.assert_called_with(edit=True, progress=25.0, status='')
