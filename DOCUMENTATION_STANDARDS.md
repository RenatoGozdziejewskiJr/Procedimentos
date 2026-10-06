# Documentation Standards

This document defines the writing, naming, and structure rules for new and substantially revised documents in this repository. Existing documents do not need to be renamed or rewritten as part of adopting these rules.

## 1. Language and tone

1. Write the canonical version of each document in British English (EN-GB).
2. Use a professional, clear, and neutral tone. Prefer direct instructions and concise wording.
3. Do not use emojis, slang, or unexplained abbreviations.
4. Preserve product names, command names, code, and other official technical terms as written by their owners.
5. Use consistent British English spelling and terminology in prose.

## 2. File format and names

1. Store documentation as UTF-8 Markdown files with the `.md` extension.
2. Use lower-case ASCII words separated by hyphens in filenames. Avoid spaces, accents, and special characters.
3. Assign each document a unique, four-digit number, starting at `0001`. Do not reuse numbers or renumber existing documents when another document is added.
4. Name each canonical English document using this pattern:

   `0000-notes-<short-description>.md`

   Replace `0000` with the assigned number and use a concise, descriptive slug, for example `0001-notes-configure-ssh-server.md`.
5. Keep optional Portuguese (Brazil) translations in a separate companion file with the same number and a `-pt-br` suffix, for example `0001-notas-configurar-servidor-ssh-pt-br.md`.
6. Keep a translation aligned with its English source. Update both when the documented procedure changes, and link to the companion language version from each document.

## 3. Titles and headings

1. Start each procedure or technical-note document with one level-one heading (`#`).
2. Begin the English title with `Notes about`, followed by the subject. For example: `# Notes about configuring an SSH server`.
3. Begin a Portuguese (Brazil) translation title with `Notas sobre`, followed by the subject.
4. Number sections and subsections hierarchically: `1.`, `1.1`, `1.2`, `2.`. Do not number the document title.
5. Use heading levels consistently: level-two headings for main numbered sections and level-three headings for their subsections.
6. Keep heading text concise and descriptive; do not use emojis in headings.

## 4. Recommended document structure

Use the sections that apply to the subject. Omit sections that do not add useful information rather than filling them with placeholders.

1. **Purpose** — state what the document helps the reader accomplish.
2. **Scope and prerequisites** — identify the applicable environment, required access, tools, and assumptions.
3. **Procedure** — give ordered, reproducible steps. Include commands and configuration examples in fenced code blocks with a language identifier where appropriate.
4. **Verification** — explain how to confirm that the procedure succeeded.
5. **Troubleshooting** — describe relevant symptoms and corrective actions, when applicable.
6. **References** — link to authoritative sources and related repository documents, when applicable.

Use ordered lists for steps that must be performed in sequence and unordered lists for items with no required order. Mark warnings and important data-loss or security implications clearly in plain text; do not rely on colour or emoji alone.

## 5. Links and examples

1. Prefer relative links for other files in this repository and descriptive link text.
2. Use fenced code blocks for commands, code, and configuration. State the shell or language when it affects how an example should be run.
3. Clearly identify values that readers must replace, and do not include real credentials, tokens, or other secrets.
4. Check links, commands, and examples for accuracy when creating or updating a document.

## 6. MkDocs

1. Keep Markdown source files in the existing category folders unless a separate reorganisation is approved.
2. Build and serve the documentation from the repository root using the root `mkdocs.yml` configuration.
3. Install the documentation dependency with `python -m pip install -r requirements.txt`.
4. Preview changes locally with `python -m mkdocs serve` and build the site with `python -m mkdocs build`.
5. Exclude generated build output and local data files from the published site using `exclude_docs` in `mkdocs.yml`.
6. Treat the Markdown files as the source of truth; do not edit generated site output.
