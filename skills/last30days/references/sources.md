# Last30Days source families

The upstream v4.5.0 engine advertises support for Reddit, X, YouTube, TikTok, Hacker News, Polymarket, GitHub and web search, with additional providers depending on its release and configuration. This list describes the upstream project only; it does not mean a source is connected or available in this Harnes session.

Before reporting on a source, check the actual search result or source status returned by the active tool. Distinguish:

- **Results found** — cite the returned items.
- **No results** — a clean search returned none for the stated query/window.
- **Partial or failed** — timeout, rate limit, authentication failure, schema change, unconfigured source, or unavailable tool. This is not evidence that the source was quiet.

Never infer source access from environment-variable names, browser cookies, installed packages, or a prior run. Do not read `.env`, browser profiles, cookies, tokens, or keychains unless the user explicitly authorizes the relevant operation. Never ask the user to paste secrets into chat.

For the pinned upstream implementation and its current source descriptions, see [the v4.5.0 source tree](https://github.com/mvanhorn/last30days-skill/tree/e63f8e8732f1b934449b363f211b3654531b8ef2/skills/last30days).
