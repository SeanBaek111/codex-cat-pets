# Installation guide

[← Back to Cream & Cheese](README.md)

## Download

**[Download both pets as a ZIP](https://github.com/SeanBaek111/codex-cream-cheese/releases/latest/download/codex-cream-cheese.zip)**

The ZIP contains only the four files needed by the pets:

```text
pets/
  cream/
    pet.json
    spritesheet.webp
  cheese/
    pet.json
    spritesheet.webp
```

No scripts, previews, tests, or development files are included. No GitHub login is needed.

## Manual installation

If the app opens without an installation window, install the files directly. No script is required.

### macOS with Finder

1. [Download the ZIP](https://github.com/SeanBaek111/codex-cream-cheese/releases/latest/download/codex-cream-cheese.zip), extract it, and open its `pets` folder.
2. In Finder, press **Command + Shift + G**, enter `~/.codex/`, and press Return.
3. Open the `pets` folder, or create it if missing. Copy `cream` and `cheese` from the extracted ZIP into it. Back up existing folders with those names before replacing them.
4. Fully quit and reopen Codex, then choose your pet in **Settings > Pets**.

### Individual file downloads

Right-click each link and choose **Save Link As**. Preserve the filenames, including their extensions.

| Pet folder | Manifest | Spritesheet |
| --- | --- | --- |
| `cream` | [pet.json](https://raw.githubusercontent.com/SeanBaek111/codex-cream-cheese/main/pets/cream/pet.json) | [spritesheet.webp](https://raw.githubusercontent.com/SeanBaek111/codex-cream-cheese/main/pets/cream/spritesheet.webp) |
| `cheese` | [pet.json](https://raw.githubusercontent.com/SeanBaek111/codex-cream-cheese/main/pets/cheese/pet.json) | [spritesheet.webp](https://raw.githubusercontent.com/SeanBaek111/codex-cream-cheese/main/pets/cheese/spritesheet.webp) |

Put each pair of files inside its named pet folder. Copy the `cream` and `cheese` folders to the following location:

| Platform | Default destination |
| --- | --- |
| macOS | `~/.codex/pets/` |
| Windows | `%USERPROFILE%\.codex\pets\` |

Keep `pet.json` and `spritesheet.webp` together inside each pet folder. If your app uses a custom `CODEX_HOME`, copy the folders into its `pets` directory instead. For the native Windows app, use the Windows user directory rather than a WSL home directory.

## Package details and validation

- Each pet uses a transparent 1536 x 2288 WebP spritesheet, the v2 format, nine animation states, and 16 look directions.
- Original photographs and local working records are not included.
- Both spritesheets passed asset validation and visual review.
- The repository retains optional installer scripts and tests for developers; they are not included in the ZIP. macOS installer tests passed. Windows execution and playback on other computers remain unverified.

These custom pets were created from photo references using imagegen and hatch-pet. They are not official OpenAI characters.
