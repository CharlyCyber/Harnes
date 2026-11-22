# Skill catalog lifecycle in Harnes

Harnes is the source of truth for the skills and internal modules in this repository. HyperFrames instructions and modules are reviewed and updated here, then distributed only through the Harnes sync process. This workflow deliberately does not let the HyperFrames CLI or an external skills manager install, update, prune, or remove catalog content.

## Do not manage skills from the video workflow

Never invoke the HyperFrames CLI subcommands for skill listing, setup, checking, updating, or removal from a video task. Never invoke another skills package manager or request an unattended/global install.

Do not use `-g`, skip prompts, update a plugin, or install a missing workflow. If a referenced module is not available in the Harnes checkout, name the missing module and continue only with supported guidance. The user's plugin manager owns plugin-bundle updates; Harnes owns the repository catalog.

## Maintainer update workflow

When an operator explicitly requests a Harnes catalog update:

1. Inspect the declared upstream source, commit or release, license, file-level changes, dependencies, scripts, and local-only content.
2. Port only changes that match the existing canon and preserve custom routing, safety rules, and unique files. Do not replace a module wholesale just because upstream is newer.
3. Record source SHA, license, adopted paths, and any exclusions in `skills/REGISTRO.md` and the relevant provenance file.
4. Run focused tests and `git diff --check`. Run `python sync/harnes.py doctor --skip-sync` only when its declared validator is available; do not install it automatically.
5. Review the final Git diff. Do not sync user-level skills unless explicitly asked.

## CLI project versions

A project's `hyperframes` dependency pin is distinct from Harnes skill freshness. Do not change `package.json`, lockfiles, or fetch a CLI release without the user's approval. If the user asks to update the project's CLI, use the launcher in `plugin-installation.md`, make the smallest requested change, run `check`, and report the previous/new version and validation outcome. A successful check establishes validity, not frame-identical output.
