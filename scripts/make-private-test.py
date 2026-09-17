#!/usr/bin/env python3
"""Create a local, self-contained test page without publishing private pet assets."""
import argparse
import base64
import hashlib
import html
import json
from pathlib import Path
import re
import subprocess
import sys
from datetime import datetime, timezone
from urllib.parse import urlencode, urlsplit
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
REPO = 'SeanBaek111/codex-cat-pets'


def github(path):
    result = subprocess.run(['gh', 'api', path], capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError('GitHub request failed. Check gh authentication and repository access.')
    return json.loads(result.stdout)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    output = args.output.expanduser().resolve()
    if output == ROOT or ROOT in output.parents:
        raise RuntimeError('Write the private test page outside the Git repository.')
    page = (ROOT / 'docs/index.html').read_text(encoding='utf-8')
    for pet in ('cheese', 'cream'):
        manifest = json.loads((ROOT / 'pets' / pet / 'pet.json').read_text(encoding='utf-8'))
        record = github(f'repos/{REPO}/contents/pets/{pet}/spritesheet.webp')
        url = record.get('download_url', '')
        parsed = urlsplit(url)
        if parsed.scheme != 'https' or parsed.hostname != 'raw.githubusercontent.com':
            raise RuntimeError('Unexpected GitHub download URL.')
        # Do not log URLs: private download URLs may contain temporary access tokens.
        with urlopen(url, timeout=30) as response:
            received = response.read()
        expected = (ROOT / 'pets' / pet / 'spritesheet.webp').read_bytes()
        if hashlib.sha256(received).digest() != hashlib.sha256(expected).digest():
            raise RuntimeError('Downloaded image does not match the local pet asset.')
        link = 'codex://pets/install?' + urlencode({
            'name': manifest['displayName'],
            'description': manifest['description'],
            'imageUrl': url,
            'spriteVersionNumber': '2',
        })
        page, count = re.subn(r'(id="install-' + pet + r'" href=")[^"]*(")',
                             lambda match: match[1] + html.escape(link, quote=True) + match[2], page)
        if count != 1:
            raise RuntimeError('Installation button is missing or duplicated.')
        gif = base64.b64encode((ROOT / 'previews' / f'{pet}.gif').read_bytes()).decode('ascii')
        page = page.replace(f'../previews/{pet}.gif', 'data:image/gif;base64,' + gif)
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    notice = ('<aside class="notice"><strong>Private installation test</strong>'
              '<p>This local page contains temporary access links to your private pet images. '
              'Keep the file private. It can be opened on your other Mac or PC without a server. '
              'If a link expires, generate a fresh page. Your repository remains private.</p>'
              '<p>Generated ' + timestamp + '. Opening the page alone does not install anything.</p></aside>')
    page = page.replace('<!-- TEST_NOTICE -->', notice)
    page = re.sub(r'<!-- DOWNLOAD_LINK -->.*?<!-- /DOWNLOAD_LINK -->', '', page, flags=re.S)
    output.parent.mkdir(parents=True, exist_ok=True)
    # Create or replace with owner-only permissions before writing private URLs.
    import os
    fd = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    os.fchmod(fd, 0o600)
    with os.fdopen(fd, 'w', encoding='utf-8') as handle:
        handle.write(page)
    print('Private test page created; both image downloads verified. No URLs logged.')


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        # Suppress exception details that might contain a private URL.
        print('Private page creation failed (' + type(error).__name__ + '). Check GitHub access and try again.', file=sys.stderr)
        sys.exit(1)
