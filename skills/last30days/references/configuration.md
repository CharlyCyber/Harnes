# Configuration and installation boundary

This Harnes copy contains guidance only. It does not contain the upstream engine, setup wizard, scripts, or storage system, so the old environment-variable examples and shell commands are intentionally not reproduced here.

If the user explicitly asks to acquire the upstream runtime, first review the pinned source, license, prerequisites, network access, credential handling and installation scope. Ask before installing packages, changing project/global configuration, or storing credentials. Do not run `npx skills add -g`, bypass prompts, read secret files, or ask for API keys in chat. Prefer the user's approved secret manager and the current upstream setup documentation.

Pinned upstream documentation: [Last30Days v4.5.0](https://github.com/mvanhorn/last30days-skill/tree/e63f8e8732f1b934449b363f211b3654531b8ef2/skills/last30days). The upstream's required runtime and configuration may change; do not use old snippets from this Harnes module as current setup instructions.
