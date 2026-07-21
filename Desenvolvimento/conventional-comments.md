# Conventional Comments

Quick summary based on https://conventionalcomments.org/ to standardize review feedback.

## Objective

- Make review comments clearer, actionable, and easier to understand.
- Reduce noise and ambiguity in PRs.
- Keep comments human-friendly and machine-parseable.

## Standard format

Use this format:

```text
<label> [decorations]: <subject>

[discussion]
```

- label: comment type.
- decorations (optional): extra context in parentheses, comma-separated.
- subject: main message.
- discussion (optional): context, rationale, and next steps.

## Recommended labels

- praise: sincere positive feedback.
- nitpick: trivial preference request, naturally non-blocking.
- suggestion: proposal to improve the current implementation.
- issue: identified problem (functional, technical, UX, etc.).
- todo: small but necessary change.
- question: concern or clarification request.
- thought: non-blocking idea for future improvement.
- chore: process/task needed before formal acceptance.
- note: informational, non-blocking remark.

Common additional labels:

- typo: spelling mistake.
- polish: quality/finish improvement.
- quibble: lighter alternative to nitpick.

## Common decorations

- (non-blocking): should not block approval.
- (blocking): should block approval until resolved.
- (if-minor): resolve only if the change is minor/trivial.

Other decorations can be used by technical context, for example:

- (security), (performance), (test), (ux), (docs).

## Best practices

- Prefer specific comments with a clear action.
- For issue comments, include a paired suggestion when possible.
- Avoid too many decorations in a single comment.
- Include at least one sincere praise per review when appropriate.

## Quick reference for Azure PR comments

Use these directly in PR comments:

```text
suggestion: Can we extract this block to reduce duplication?
```

```text
issue (blocking): This flow breaks when the token expires.
```

```text
nitpick (non-blocking): Rename this variable to better reflect the returned value.
```

```text
question: Is this endpoint always expected to return data sorted by date?
```

```text
praise: Great test coverage for this critical scenario.
```

## Quick reference for Git commits

Conventional Comments is for review feedback.
For commit messages, the related pattern is Conventional Commits.

Format:

```text
<type>(<optional scope>): <short description>
```

Most common types:

- feat: new feature.
- fix: bug fix.
- docs: documentation.
- refactor: code restructure with no functional change.
- test: test-related changes.
- chore: maintenance/infra.
- perf: performance improvements.
- ci: pipeline/automation changes.

Examples:

```text
feat(auth): add automatic token renewal
fix(api): handle retry timeout correctly
docs(dev): add devcontainer build guide
chore(ci): update agent version in pipeline
```

## Copy and paste: 10 ready-to-use PR messages (Azure)

```text
1) issue (blocking): There is a NullReference risk when the API response is empty.

2) suggestion: We could extract this validation into a helper to reduce duplication across methods.

3) question: Is this behavior defined by business rules, or is it a side effect of the current implementation?

4) nitpick (non-blocking): Rename this variable to better represent the payload.

5) todo: Add test coverage for the 401 error scenario to prevent regression.

6) chore: Update the pipeline so this job also runs on release branches.

7) note (non-blocking): This change affects the endpoint contract and may impact legacy consumers.

8) thought (non-blocking): In a future iteration, consider local caching to reduce sequential calls.

9) suggestion (if-minor): If this is a minor change, standardize log messages to match other modules.

10) praise: Nice separation of concerns, this is much easier to test and maintain.
```
