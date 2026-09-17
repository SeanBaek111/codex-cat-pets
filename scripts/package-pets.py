#!/usr/bin/env python3
"""Build a pet-only release ZIP; never archive the whole repository."""
import argparse
import hashlib
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path, required=True, help='Output directory')
args = parser.parse_args()
args.output.mkdir(parents=True, exist_ok=True)
archive = args.output / 'codex-cat-pets.zip'
files = [f'pets/{pet}/{name}' for pet in ('cheese', 'cream')
         for name in ('pet.json', 'spritesheet.webp')]
with ZipFile(archive, 'w', ZIP_DEFLATED) as bundle:
    for name in files:
        bundle.write(root / name, name)
with ZipFile(archive) as bundle:
    assert bundle.namelist() == files
    assert bundle.testzip() is None
    for name in files:
        assert bundle.read(name) == (root / name).read_bytes()
digest = hashlib.sha256(archive.read_bytes()).hexdigest()
archive.with_suffix('.zip.sha256').write_text(f'{digest}  {archive.name}\n')
print(f'Verified {archive}: {len(files)} pet files, {archive.stat().st_size:,} bytes')
