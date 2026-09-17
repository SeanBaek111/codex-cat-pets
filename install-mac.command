#!/bin/bash
set -euo pipefail
bundle_dir="$(cd "$(dirname "$0")" && pwd)"
pet_home="${CODEX_HOME:-$HOME/.codex}"
if [ "$#" -gt 1 ]; then
  echo 'Usage: bash install-mac.command [codex-home-directory]' >&2
  exit 1
fi
if [ "$#" -eq 1 ]; then pet_home="$1"; fi
if [ -z "$pet_home" ]; then echo 'Destination must not be empty.' >&2; exit 1; fi

# Check the whole bundle before writing anything to the destination.
(cd "$bundle_dir" && shasum -a 256 -c SHA256SUMS)
backup_dir=''
for pet_id in cheese cream; do
  target="$pet_home/pets/$pet_id"
  if [ -L "$target" ]; then echo "Refusing symlink: $target" >&2; exit 1; fi
done
for pet_id in cheese cream; do
  target="$pet_home/pets/$pet_id"
  if [ -e "$target" ]; then
    if [ -z "$backup_dir" ]; then
      mkdir -p "$pet_home/pet-backups"
      backup_dir="$(mktemp -d "$pet_home/pet-backups/cat-pets-$(date +%Y%m%d-%H%M%S)-XXXXXX")"
    fi
    cp -R "$target" "$backup_dir/$pet_id"
  fi
  mkdir -p "$target"
  cp "$bundle_dir/pets/$pet_id/pet.json" "$target/pet.json"
  cp "$bundle_dir/pets/$pet_id/spritesheet.webp" "$target/spritesheet.webp"
  cmp "$bundle_dir/pets/$pet_id/pet.json" "$target/pet.json"
  cmp "$bundle_dir/pets/$pet_id/spritesheet.webp" "$target/spritesheet.webp"
done
echo "Installed Cheese and Cream in: $pet_home/pets"
if [ -n "$backup_dir" ]; then echo "Previous files backed up in: $backup_dir"; fi
echo 'Open Codex > Settings > Pets and select Cheese or Cream.'
echo 'If they are missing, quit and reopen Codex.'
