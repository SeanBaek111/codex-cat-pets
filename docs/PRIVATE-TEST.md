# Private installation test

A generated `private-install-test.html` is a self-contained page for testing the native Codex pet installation flow while the repository stays private.

1. Open the HTML file in Safari or Chrome on the computer where Codex is installed.
2. Click **Open Cream in Codex** or **Open Cheese in Codex**.
3. Allow the browser to open Codex, then review and complete the app's installation flow.

The HTML contains temporary access links to the private pet images. Keep it private. Do not commit it, publish it, or attach it to a public issue. If the app cannot download an image after some time, regenerate the page. No exact expiration time is assumed.

## Generate a fresh test page

For the maintainer: Python 3 and an authenticated GitHub CLI with access to this repository are required. The script uses only Python's standard library.

```sh
python3 scripts/make-private-test.py --output ../private-install-test.html
```

The generator verifies both downloaded spritesheets against the local assets, embeds the preview GIFs, and writes the output with owner-only permissions outside this Git repository. It does not publish anything or change repository visibility.

For a private test release, a maintainer can replace its HTML attachment after generating a fresh page:

```sh
gh release upload v1.1.0 ../private-install-test.html --repo SeanBaek111/codex-cream-cheese --clobber
```

Upload this attachment only while the repository is private. Remove the temporary test attachment before making the repository public. Do not add the generated HTML to Git history.

`docs/index.html` is the static page prepared for future public hosting. Its unsigned public image URLs will not work while this repository remains private. Use the generated private test page now.

The official link format is documented at https://learn.chatgpt.com/docs/reference/commands#pets. Successful image downloads and valid link parameters do not prove installation inside the desktop app; test that separately on the target computer.
