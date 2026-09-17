"""Installer checks using isolated destinations. No real Codex settings are touched."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class InstallTests(unittest.TestCase):
    def setUp(self):
        # Keep fixtures for inspection; this test never deletes user files.
        self.fixture = Path(tempfile.mkdtemp(prefix='cat-pets-test-'))
        self.bundle = self.fixture / 'bundle with spaces'
        shutil.copytree(ROOT, self.bundle, ignore=shutil.ignore_patterns('.git', '__pycache__'))
        self.dest = self.fixture / 'codex home'

    def install(self, check=True):
        if os.name == 'nt':
            cmd = ['powershell.exe', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File',
                   str(self.bundle / 'install-windows.ps1'), '-CodexHome', str(self.dest)]
        else:
            cmd = ['bash', str(self.bundle / 'install-mac.command'), str(self.dest)]
        return subprocess.run(cmd, check=check, capture_output=True, text=True)

    def test_install_and_backup(self):
        self.install()
        for pet in ('cream', 'cheese'):
            target = self.dest / 'pets' / pet
            manifest = json.loads((target / 'pet.json').read_text(encoding='utf-8'))
            self.assertEqual(manifest['id'], pet)
            self.assertEqual(manifest['spriteVersionNumber'], 2)
            for name in ('pet.json', 'spritesheet.webp'):
                self.assertEqual((target / name).read_bytes(), (self.bundle / 'pets' / pet / name).read_bytes())
        previous = b'previous custom pet content'
        (self.dest / 'pets/cheese/pet.json').write_bytes(previous)
        unrelated = self.dest / 'pets/unrelated'
        unrelated.mkdir()
        (unrelated / 'keep.txt').write_text('keep')
        self.install()
        backups = list((self.dest / 'pet-backups').glob('*/cheese/pet.json'))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_bytes(), previous)
        self.assertEqual((unrelated / 'keep.txt').read_text(), 'keep')

    def test_corrupt_download_makes_no_changes(self):
        with (self.bundle / 'pets/cream/spritesheet.webp').open('ab') as f:
            f.write(b'corrupted')
        self.assertNotEqual(self.install(check=False).returncode, 0)
        self.assertFalse(self.dest.exists())


if __name__ == '__main__':
    unittest.main()
