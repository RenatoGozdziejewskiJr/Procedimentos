# Notes about Conventional Comments

[Português (Brasil)](0007-notas-conventional-comments-pt-br.md)

A brief summary based on https://conventionalcomments.org/ for standardising review feedback.

## 1. Objective

- Make review comments clearer, actionable and easier to understand.
- Reduce noise and ambiguity in pull requests (PRs).
- Keep comments human-friendly and machine-parseable.

## 2. Standard Format

Use this format:

```text
<label> [decorations]: <subject>

[discussion]
```

- label: comment type.
- decorations (optional): additional context in parentheses, separated by commas.
- subject: main message.
- discussion (optional): context, rationale and next steps.

## 3. Recommended Labels

- praise: sincere positive feedback.
- nitpick: a trivial preference request that is naturally non-blocking.
- suggestion: a proposal to improve the current implementation.
- issue: an identified problem (functional, technical, UX, etc.).
- todo: a small but necessary change.
- question: a concern or clarification request.
- thought: a non-blocking idea for the future.
- chore: a process task needed before formal acceptance.
- note: an informational, non-blocking remark.

### 3.1 Common Additional Labels

- typo: a spelling mistake.
- polish: a quality or finishing improvement.
- quibble: a lighter alternative to nitpick.

## 4. Common Decorations

- (non-blocking): should not block approval.
- (blocking): should block approval until resolved.
- (if-minor): resolve only if the change is minor or trivial.

Other decorations may be used according to the technical context, for example:

- (security), (performance), (test), (ux), (docs).

## 5. Best Practices

- Prefer specific comments with a clear action.
- For issue comments, include a paired suggestion when possible.
- Avoid using too many decorations in one comment.
- Include at least one sincere praise comment per review when appropriate.

## 6. Quick Reference for Azure PR Comments

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

## 7. Quick Reference for Git Commits

Conventional Comments is for review feedback. The related pattern for commit messages is Conventional Commits.

Format:

```text
<type>(<optional scope>): <short description>
```

Most common types:

- feat: a new feature.
- fix: a bug fix.
- docs: documentation.
- refactor: code restructuring with no functional change.
- test: testing.
- chore: maintenance or infrastructure.
- perf: a performance improvement.
- ci: pipeline or automation.

Examples:

```text
feat(auth): add automatic token renewal
fix(api): handle retry timeout correctly
docs(dev): add devcontainer build guide
chore(ci): update agent version in pipeline
```

## 8. Copy and Paste: 10 Ready-to-Use PR Messages (Azure)

```text
1) issue (blocking): There is a NullReference risk when the API response is empty.

2) suggestion: We could extract this validation into a helper to reduce duplication across methods.

3) question: Is this behaviour defined by business rules, or is it a side effect of the current implementation?

4) nitpick (non-blocking): Rename this variable to better reflect the payload.

5) todo: Add test coverage for the 401 error scenario to prevent regression.

6) chore: Update the pipeline so this job also runs on release branches.

7) note (non-blocking): This change affects the endpoint contract and may impact legacy consumers.

8) thought (non-blocking): In a future iteration, consider local caching to reduce sequential calls.

9) suggestion (if-minor): If this is a minor change, standardise log messages to match other modules.

10) praise: Nice separation of concerns; this is much easier to test and maintain.
```
