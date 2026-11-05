---
name: triage
description: >
  Automated triage of GitHub Issues and PRs. Scan, categorize, detect duplicates,
  classify risk, deep-analyze diffs, and execute actions (comment, label, close, merge)
  with explicit validation. Use when user says "/triage", "triage issues", "triage PRs",
  "review backlog", or when >10 untriaged issues or >5 unreviewed PRs are detected.
  Auto-triggers on "triage" or "backlog" keywords.
---

Three-phase triage for Issues and/or PRs. Always ask before destructive actions (close, merge).

## Phase 1: Audit

### Issues
```bash
# List open issues sorted by creation date (newest first)
gh issue list --state open --limit 50 --json number,title,labels,createdAt,updatedAt,comments,author,body --jq '.'

# Count by label
gh issue list --state open --json labels --jq 'group_by(.labels[].name) | map({label: .[0].labels[0].name, count: length})'
```

Categorize each issue:
- **bug** — unexpected behavior, crash, error
- **feature** — new capability request
- **enhancement** — improvement to existing feature
- **question** — how-to, usage clarification
- **docs** — documentation gap
- **chore** — maintenance, CI, deps

Detect duplicates by comparing title + body with Jaccard similarity (token overlap). Flag pairs with >0.6 similarity.

Cross-reference: search for linked PRs via `#N` patterns in issue body.

Risk classification:
- **critical**: crash, data loss, security, P0
- **high**: broken feature, regression, no workaround
- **medium**: annoyance, missing edge case
- **low**: cosmetic, nice-to-have

Stale detection: no activity in 60+ days → tag `stale` and comment asking if still relevant.

### PRs
```bash
# List open PRs sorted by size/complexity
gh pr list --state open --limit 50 --json number,title,labels,createdAt,headRefName,baseRefName,additions,deletions,author,reviews --jq '.'

# Check mergeability
gh pr view <N> --json mergeable,reviews,state,statusCheckRollup
```

Size estimation (lines changed):
- **XS**: <50 lines
- **S**: 50-200 lines
- **M**: 200-500 lines
- **L**: 500-1500 lines
- **XL**: >1500 lines

Check status:
- Merge conflicts? (`mergeable != "MERGEABLE"`)
- CI passing? (`statusCheckRollup`)
- Required reviews? (`reviews`)
- CLA signed?

## Phase 2: Deep Analysis

Prompt the user: *"Deep-analyze [N issues / N PRs]? This will take ~X tokens. Proceed?"*

### Issues
For each issue being analyzed, use `gh issue view <N> --json title,body,comments,labels` and parse. Then spawn parallel subagents for:

1. **Root cause analysis** — read code paths mentioned, hypothesize cause
2. **Fix complexity estimation** — XS/S/M/L/XL based on code involved
3. **Cross-ref PR detection** — `rg '#\d+'` in issue body → check each ref against PR list

Output per issue:
```
## #<N>: <title>
- Category: bug|feature|enhancement|question|docs|chore
- Risk: critical|high|medium|low
- Duplicate of: #<M> (or none)
- Related PRs: #<P>, #<Q>
- Stale: yes (last activity <date>) | no
- Suggested action: label|comment|close|defer
```

### PRs
For each PR, `gh pr view <N> --json title,body,additions,deletions,files,reviews,comments,statusCheckRollup`.

1. **Diff summary**: list files changed, categorize (logic/test/docs/config)
2. **Risk hotspots**: files in core logic, unsafe patterns (`eval`, `exec`, raw SQL, unsafe `unwrap`)
3. **Test coverage**: are there tests? CI passing?
4. **Review status**: approved? changes requested? pending?

Output per PR:
```
## #<N>: <title>
- Size: XS|S|M|L|XL (<additions>+<deletions> lines)
- Mergeable: yes|no|unknown
- CI: passing|failing|pending
- Reviews: approved|changes-requested|pending (<N> of <M>)
- Risk: low|medium|high|critical
- Hotspots: <file list>
- Suggested action: merge|request-changes|wait-for-ci|confer
```

## Phase 3: Actions

**IMPORTANT: Always ask user before executing destructive actions (close, merge, request-changes).**

```bash
# Add label
gh issue edit <N> --add-label <label>

# Add comment
gh issue comment <N> --body "<comment>"

# Close with reason
gh issue close <N> --comment "<reason>" --reason completed|not_planned

# Reopen
gh issue reopen <N>

# Merge PR (after user confirmation)
gh pr merge <N> --merge|--squash|--rebase --subject "<title>" --body "<body>"

# Request changes via review
gh pr review <N> --request-changes --body "<reason>"

# Approve
gh pr review <N> --approve --body "<summary>"
```

### Triage Summary Output
After all actions, generate a markdown summary:
```markdown
# Triage Summary — <date>

## Issues: <N> open, <M> triaged
- <count> bugs (critical: <c>, high: <h>)
- <count> features/enhancements
- <count> questions
- <count> stale
- <count> duplicates closed

## PRs: <N> open, <M> reviewed
- <count> ready to merge
- <count> need changes
- <count> blocked (CI/conflicts)
- <count> unreviewed
```
