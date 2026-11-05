---
name: ship
description: >
  Complete release workflow: semantic version bump from conventional commits,
  CHANGELOG generation, build verification, git tag, push, CI/CD trigger, and
  post-release verification. Includes rollback plan. Use ONLY when user explicitly
  requests "/ship", "release", "publish version", "ship it", "do a release".
  NEVER auto-trigger — this is a destructive workflow.
---

**IMPORTANT SAFETY RULE: Never auto-trigger this skill. Only execute on explicit user command. Always ask for confirmation before each destructive step (tag, push, release publish).**

## Pre-Flight Checklist

Run all checks before proceeding. If any fail, stop and report.

```bash
# 1. Working tree clean
git status --porcelain
# must be empty — if not, ask user to commit/stash first

# 2. On correct branch (main/master/release)
git branch --show-current
# must be main or release branch

# 3. Up to date with remote
git fetch origin
git log HEAD..origin/$(git branch --show-current) --oneline
# must be empty (no unpushed commits)

# 4. CI passing on latest commit
gh run list --branch $(git branch --show-current) --limit 1 --json conclusion,status
# must show conclusion: "success" and status: "completed"

# 5. Tests pass locally
# Run the project's test command
```

## Phase 1: Version Bump

### Determine Bump Type
Scan commits since last tag using conventional commits:
```bash
# get commits since last tag
git log $(git describe --tags --abbrev=0)..HEAD --oneline
```

Rules:
- **MAJOR**: any commit with `!` or `BREAKING CHANGE` footer
- **MINOR**: `feat:` commits (no breaking)
- **PATCH**: `fix:`, `docs:`, `chore:`, `refactor:`, `style:`, `perf:`, `test:` (no breaking, no feat)

Ask user: *"Detected <type> bump: v<current> → v<next>. Correct?"*

### Update Version
```bash
# Read current version from file (package.json, Cargo.toml, pyproject.toml, etc.)
# Update to new version
```

Approach depends on project type:
- **Node**: `npm version <major|minor|patch> --no-git-tag-version`
- **Python**: update `__version__` or `pyproject.toml`
- **Rust**: `cargo set-version <version>`
- **Generic**: update version file(s) directly, ensure consistency

## Phase 2: CHANGELOG

Generate from conventional commits since last tag:

```markdown
# Changelog

## [<version>] — <date>

### Breaking Changes
- <commit messages with `!` or BREAKING CHANGE>

### Features
- <feat: commit messages>

### Bug Fixes
- <fix: commit messages>

### Documentation
- <docs: commit messages>

### Maintenance
- <chore | refactor | style | perf | test messages>
```

Ask user: *"Review CHANGELOG content above. Approve?"*

## Phase 3: Build & Verify

```bash
# Build the project
# Run lint
# Run tests
# Run benchmarks if baseline exists
```

If build/lint/test fails: **STOP**. Report failure. Do not proceed.

## Phase 4: Commit & Tag

```bash
# Stage version files + CHANGELOG
git add <version-files> CHANGELOG.md

# Commit
git commit -m "chore: release v<version>"

# Annotated tag
git tag -a v<version> -m "Release v<version>"
```

Ask user: *"Ready to push? This will trigger CI/CD. Push v<version> to origin?"*

## Phase 5: Push & Release

```bash
# Push commit + tag
git push origin $(git branch --show-current)
git push origin v<version>

# Create GitHub Release
gh release create v<version> --title "v<version>" --notes-file CHANGELOG.md --verify-tag
```

## Phase 6: Post-Release Verification

```bash
# Verify release published
gh release view v<version> --json tagName,name,createdAt,isLatest

# Check CI run for the tag
gh run list --workflow <ci-workflow> --branch v<version> --limit 1
```

Wait for CI to complete (poll up to 10 min):
```bash
gh run watch <run-id>
```

If CI fails: **IMMEDIATELY report to user**. Ask if they want to revert or hotfix.

## Rollback Plan

If release needs to be rolled back:

```bash
# 1. Revert the commit
git revert --no-edit HEAD

# 2. Delete the remote tag (force if needed)
git push --delete origin v<version>

# 3. Delete GitHub Release
gh release delete v<version> --yes

# 4. Push revert
git push origin $(git branch --show-current)

# 5. Create hotfix branch
git checkout -b hotfix/v<version>
```

**Ask user before executing any rollback step.**

---

## Gate pre-push opcional

Si el proyecto ya usa el proxy `no-mistakes` (worktree aislado + review → test → docs → lint → PR → CI antes de tocar el remoto), el push se hace contra el gate, no contra `origin`:

```bash
git push no-mistakes <branch>
```

Detalle del gate, instalacion y hallazgos escalables: [`references/pre-push.md`](./references/pre-push.md).
