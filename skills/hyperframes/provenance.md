# HyperFrames upstream provenance

- Upstream: `heygen-com/hyperframes`, <https://github.com/heygen-com/hyperframes>.
- Reviewed/synchronized commit: `79e43a33a87dc3b178c7969c6ceaae7efd33b8b4` (2026-11-22).
- License: Apache-2.0; notice in `LICENSE-upstream`.
- On 2026-11-22, common, historically exact upstream Markdown references were refreshed in `hyperframes-cli`, `hyperframes-registry`, `media-use`, and `remotion-to-hyperframes`; local-only references and specialized Harnes routers were retained. The `hyperframes` router and the existing 12-module Harnes layout were not replaced by the upstream's restructured skill set.
- Security refresh: the plugin launcher and tests, media manifest/recipe storage, and transcript-cut implementation/tests were updated from exact upstream files. New helper dependencies were added only where required. Harnes-specific launcher changes reject skill-management subcommands and set `HYPERFRAMES_SKIP_SKILLS=1` for both plugin and standalone invocation. The upstream launcher enforces a CLI security floor and runs npm from the home directory rather than a received project.
- Validation: `plugin-cli.test.mjs`, `manifest.test.mjs`, `recipe-store.test.mjs`, and `transcript-cut.test.mjs` were run. FFmpeg-dependent transcript-cut cases are skipped when FFmpeg/ffprobe are not available. No CLI package, skill, model, or system dependency was installed.
