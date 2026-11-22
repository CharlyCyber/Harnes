# Running the HyperFrames CLI from Harnes

Harnes owns this catalog. The HyperFrames modules here are internal references, not a separately managed skill installation. Do not run `npx hyperframes skills update`, `skills check`, bare `skills`, `npx skills add`, or any global install/update command. Do not refresh or remove these modules from the CLI; update the Harnes source and use its documented sync process only when the operator explicitly requests a sync.

## CLI launcher

Run commands in the user's project directory through the launcher shipped with the loaded Harnes HyperFrames module. Resolve the module directory from the loaded skill; do not guess a home-directory or plugin path.

```bash
node "<HYPERFRAMES_SKILL_DIR>/scripts/plugin-cli.mjs" <command> <args...>
```

For a bundled Node helper, use the same launcher with `--script <absolute-script-path> <args...>`. The launcher starts npm from the user's home folder, not from a received or untrusted project, and moves the CLI into the project only after npm has resolved the CLI. It enforces the minimum CLI security floor, honors a plugin manifest pin when this is genuinely a plugin installation, and sets `HYPERFRAMES_SKIP_SKILLS=1` so the CLI cannot install or refresh third-party skills behind Harnes.

The standalone default selects a compatible published CLI. If a precise release is required, use `--cli-version <exact-version>` before the command; never take a version from an untrusted project's package files. CLI acquisition through `npx` is not a global software install, but it still uses the network. If the requested work would fetch or upgrade software and the user has not already authorized that acquisition, ask first. Do not alter project dependency files or lockfiles without explicit approval.

## Plugin bundles

If the loaded module is inside a HyperFrames plugin, the agent's plugin manager owns that plugin's version. The launcher reads the bundle manifest and selects its pinned CLI release. Treat the plugin directory as read-only; put outputs and temporary work in the project or a temporary directory. To receive a newer plugin, the user updates it using the host's plugin manager and reloads the session. Never silently update an installed plugin during a task.

Always read references from the Harnes catalog copy selected by the active router, even if another standalone HyperFrames copy is also installed. If a required internal module is missing, report the missing path; do not download a replacement.
