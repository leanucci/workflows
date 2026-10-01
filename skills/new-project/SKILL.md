---
name: new-project
description: Create a new portfolio project that uses the agent cycle. Creates a public GitHub repo under leanucci from the leanucci/workflows skeleton and stack files, fills in CLAUDE.md, sets the Claude token secret from the macOS Keychain, sets labels and branch protection, and adds the project to the portfolio list. Use when the user wants to start a new project, app, library, or gem, or types /new-project.
---

# New Project

Create a project that is ready for the agent cycle. After this skill, the user can start the first feature with `/spec`.

The process is in `/Users/lean/work/portfolio/APPROACH.md`. The shared files are in `/Users/lean/work/workflows`.

## Inputs

| Input | Example | If missing |
|---|---|---|
| Name | `pomodoro` | Suggest a short kebab-case name. |
| Purpose | "A Pomodoro timer web app" | Ask. |
| Type | `web app` or `library` | Get it from the purpose. |
| Stack | Next.js | Ask. The user chooses the stack for each project. |
| Deploy target | Vercel, RubyGems | Ask, unless the stack sets it. |

The stack must match a folder in `/Users/lean/work/workflows/stacks/`. If no folder matches, stop. Tell the user that the stack needs CI workflows first, and offer to add them.

## Steps

1. **Check.**
   - Run `git -C /Users/lean/work/workflows pull`.
   - `gh repo view leanucci/<name>` fails, so the name is free.
   - `/Users/lean/work/<name>` does not exist.
   - `security find-generic-password -s claude-oauth-token > /dev/null` succeeds, so the token exists. Do not print the token.

2. **Copy the files.** `K=/Users/lean/work/workflows`, `S=$K/stacks/<stack>`, `P=/Users/lean/work/<name>`.
   - `mkdir -p $P` and `cp -R $K/skeleton/. $P/`
   - Copy each `$S/*.yml` into `$P/.github/workflows/`.
   - Copy `$S/gitignore` to `$P/.gitignore`.
   - Copy each other config file from `$S`, for example `vercel.json`, into `$P/`.
   - Do not copy `RULES.md` or `required-checks`.

3. **Fill in `CLAUDE.md`.**
   - Replace each `TODO` with the real value. Use the commands and the doc format from `$S/RULES.md`.
   - Web apps: "Version file: none. Web apps do not use version numbers."
   - Append `$S/RULES.md` without its line "Append this section to the project `CLAUDE.md`."
   - Write a short `README.md`: the name, the purpose, a link to `specs/`, and a link to `https://github.com/leanucci/portfolio/blob/main/APPROACH.md`.

4. **Create the repo.**
   - `git init -b main`, `git add -A`, and commit: `Add the project setup from leanucci/workflows`, with both co-author lines.
   - `gh repo create leanucci/<name> --public --description "<purpose>"`
   - `git remote add origin git@github.com:leanucci/<name>.git` (SSH: the `gh` token cannot push workflow files).
   - `git push -u origin main`

5. **Set the secrets.**
   - `security find-generic-password -s claude-oauth-token -w | gh secret set CLAUDE_CODE_OAUTH_TOKEN --repo leanucci/<name>`
   - Never print the token. Never put it in a variable that you echo.
   - Stack secrets, for example `RUBYGEMS_API_KEY`: you cannot set them. Give the user the command: `! gh secret set <NAME> --repo leanucci/<name>`.

6. **Set the GitHub settings.**
   - Read the checks from `$S/required-checks`, one for each line.
   - Run `$K/bin/setup-repo leanucci/<name> "<check 1>" "<check 2>" ...`
   - Check the result: `gh label list`, and `gh api repos/leanucci/<name>/branches/main/protection`. The protection must have the checks, 1 approval, and `enforce_admins` true.

7. **Update the portfolio.**
   - Add a section to `/Users/lean/work/portfolio/PROJECTS.md`: Type, Summary, Stack, Repo, Deploy, Local copy, and `Cycle: agent`.
   - Commit `Add <name> to the project list`, with both co-author lines. Push.

8. **Report.**
   - The repo URL and what you set up.
   - What the user must do:
     - Give the Claude GitHub App access to the repo, if the app does not have access to all repos: https://github.com/apps/claude
     - Deploy target setup. Vercel: import the repo at https://vercel.com/new. Do not choose a template. `vercel.json` sets the framework.
     - Stack secrets from step 5.
   - The next step: describe the first feature, and use `/spec`.

## Rules

- All repos go in subfolders of `/Users/lean/work`.
- Push the first commit before you run `setup-repo`. After that, branch protection blocks direct pushes to `main`.
- Do not write application code. The build agent writes it from the first spec.
