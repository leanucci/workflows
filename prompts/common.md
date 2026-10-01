# Shared Rules

These rules apply to all agents in all projects.

## Project Rules

- Read `CLAUDE.md` in the repo root before you start. Project rules override these shared rules.
- Read the related spec in `specs/`. The spec is the source of truth for what to build.
- Do not change files in `.github/workflows/`. Do not change spec files.

## Writing

Write all text in ASD-STE100 (Simplified Technical English): commit messages, pull request text, review comments, and code comments.

- Write short sentences (20 words maximum).
- Use the active voice.
- Use simple, common words. Use one meaning for each word.
- Write instructions as commands.

## Code Documentation

- Document all public classes, modules, and functions.
- Use the standard doc format of the language. `CLAUDE.md` names the format.
- Apply this rule to all new code and changed code.

## Git Commits

- Make commits atomic: include only one coherent change or fix.
- Do not mix unrelated work in a single commit.
- Write succinct commit messages that describe the change.
- Add both co-authors to each commit message:
  ```
  Co-Authored-By: Leandro Marcucci <leanucci@gmail.com>
  Co-Authored-By: Claude <noreply@anthropic.com>
  ```

## Safety

- Never print, log, or commit secrets.
- Do not merge pull requests. Do not approve pull requests. Only the owner merges.
- Do not push to `main`.
