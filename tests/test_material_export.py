import importlib.util
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import Mock, patch

from test_images import scx


class MaterialExportTests(unittest.TestCase):
    def setUp(self):
        self.commands = Mock()
        maya = types.ModuleType('maya')
        maya.cmds = self.commands
        package = types.ModuleType('max_payne_maya')
        package.__path__ = []
        package.progress_bar = Mock()
        package.ldb = types.ModuleType('max_payne_maya.ldb')
        proxy = types.ModuleType('max_payne_maya.ldb.ldb_proxy')
        for name in ('MayaTextureProxy', 'MayaLDBProxy', 'MayaMaterialProxy'):
            setattr(proxy, name, types.SimpleNamespace)
        self.module = importlib.util.module_from_spec(importlib.util.spec_from_file_location(
            'tested_material', str(Path(__file__).resolve().parents[1] / 'max_payne_maya/ldb/material.py')))
        modules = {'maya': maya, 'maya.cmds': self.commands,
                   'max_payne_maya': package, 'max_payne_maya.ldb': package.ldb,
                   'max_payne_maya.ldb.ldb_proxy': proxy,
                   'max_payne_maya.progress_bar': package.progress_bar, 'PIL': None}
        with patch.dict(sys.modules, modules):
            self.module.__spec__.loader.exec_module(self.module)

    def test_scx_texture_is_exported_and_cache_does_not_alias_contents_or_folders(self):
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as temporary:
            root = Path(temporary)
            texture = types.SimpleNamespace(file_path=r'C:\textures\mask.scx',
                                            file_type_name='scx', data=scx())
            first = self.module.dumpTextureData(str(root), texture)
            self.assertEqual('mask.tga', Path(first).name)
            self.assertEqual(2, Path(first).read_bytes()[2])
            self.assertEqual(first, self.module.dumpTextureData(str(root), texture))
            texture.data = scx()[:-1] + b'\x00'
            second = self.module.dumpTextureData(str(root), texture)
            self.assertNotEqual(first, second)
            self.assertNotEqual(Path(first).read_bytes(), Path(second).read_bytes())
            other = root / 'other'
            other.mkdir()
            third = self.module.dumpTextureData(str(other), texture)
            self.assertEqual(other, Path(third).parent)

    def test_invalid_scx_creates_no_output(self):
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as temporary:
            texture = types.SimpleNamespace(file_path='broken.scx', file_type_name='scx', data=b'bad')
            with self.assertRaises(ValueError):
                self.module.dumpTextureData(temporary, texture)
            self.assertEqual([], list(Path(temporary).iterdir()))

    def test_explicit_alpha_does_not_double_connect_transparency(self):
        self.commands.shadingNode.side_effect = ['shader', 'diffuse', 'alpha']
        self.commands.sets.return_value = 'group'
        material = types.SimpleNamespace(name='mat',
                                         properties=types.SimpleNamespace(use_alpha_channel=True))
        self.module.createHyperShadeGraph(material, 'diffuse.tga', 'alpha.tga', '', '', '')
        transparency = [call[0] for call in self.commands.connectAttr.call_args_list
                        if call[0][1] == 'shader.transparency']
        self.assertEqual([('alpha.outColor', 'shader.transparency')], transparency)
