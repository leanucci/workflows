---
name: spec
description: Turn a feature idea into a spec file and start the agent cycle. Writes specs/NNN-name.md from the project template and pushes it on a build/NNN-name branch. The push starts the build agent, which adds the code and opens one PR with the spec and the code. Use when the user describes a feature to build in a project that uses the agent cycle (a repo with specs/TEMPLATE.md and the leanucci/workflows callers), or types /spec.
---

# Spec

Turn the user's idea into one spec and start the build. The push of the spec starts the build agent. The agent adds the code to the same branch and opens one pull request. The owner approves the spec and the code together.

The process is in `/Users/lean/work/portfolio/APPROACH.md`.

## Inputs

- **Project:** see "Find the Project" below.
- **Idea:** what the user wants. It can be short.

## Find the Project

`/Users/lean/work/portfolio/PROJECTS.md` lists all projects. Use only projects with `Cycle: agent`.

Use the first rule that gives one project:

1. **Name.** The request names a project, for example "add sign-in to pomodoro".
2. **Description.** The request matches the summary of exactly one project, for example "the timer app".
3. **Session folder.** The session runs inside the local copy of a project.
4. **Conversation.** Earlier messages in this session talk about one project.

If no rule gives exactly one project, ask the user. List the projects with `Cycle: agent`, with their summaries. Do not guess.

Before you write the spec, state the project in one line, for example "Project: pomodoro". Then the user can correct it.

Ask a question only when you cannot write a testable spec without the answer. Otherwise, choose, and list the choice under "Notes".

## Steps

1. **Check the project.**
   - The repo has `specs/TEMPLATE.md` and `.github/workflows/agent.yml`. If not, stop. The project does not use the cycle, or it uses an old setup.
   - Run `git status`. If the working tree has changes, stop and tell the user.
   - Run `git checkout main` and `git pull`.

2. **Read the context.**
   - `CLAUDE.md`: the stack, the rules, and the version file.
   - `specs/TEMPLATE.md`: the format.
   - All files in `specs/`: earlier specs, so you do not repeat work and you continue the numbers.
   - The code, when the idea changes existing behavior.

3. **Set the number and the name.**
   - Number: the highest `NNN` in `specs/` plus 1, with three digits (`001`, `002`).
   - Name: 2 to 4 words in kebab case, for example `google-auth`.
   - Check that the branch `build/NNN-name` does not exist on the remote.

4. **Size the work.** A spec is one build cycle: one pull request that a reviewer can check.
   - If the idea is too large, divide it. Write the first part as this spec. List the other parts under "Out of Scope" with their future numbers. Tell the user about the division.

5. **Set the Release field.**
   - Web app: always `none`.
   - Library: `major` for a breaking change, `minor` for a new feature, `patch` for a fix. `none` for docs or CI only.

6. **Write `specs/NNN-name.md`.** Follow the template.
   - **Summary:** what and why, in 2 to 4 sentences.
   - **Requirements:** numbered. Each one is testable. Group them with `###` headings when there are more than 8.
   - **Acceptance Criteria:** numbered. Use "Given ..., when ..., then ...". Each requirement has at least one criterion.
   - **Out of Scope:** what this spec does not include. Name later specs.
   - **Notes:** your choices, constraints, and links.
   - Describe behavior, not code. Name a library or a file only when the user asks, or when `CLAUDE.md` requires it.
   - Write in ASD-STE100: short sentences, active voice, simple words.

7. **Show the spec.** Show the full spec to the user in the chat before you push. Do not wait for an answer. The user can stop the build later.

8. **Commit and push.**
   - Run `git checkout -b build/NNN-name`.
   - Commit only the spec file. Message: `Add spec NNN: <title>`, with both co-author lines from the shared rules.
   - Run `git push -u origin build/NNN-name`.
   - Run `git checkout main`.

9. **Report the build.**
   - The push starts the Agent workflow. It starts the build in about 30 seconds. Find the run with `gh run list --workflow agent.yml --branch build/NNN-name`.
   - Give the user the run URL, the Release value, and your choices from "Notes".
   - Tell the user what happens next: the build agent opens one pull request with the spec and the code. The review agent reviews it. Then GitHub asks the owner to approve and merge it.
   - Tell the user how to stop the build: `gh run cancel <run id>`.

## Changes to a Spec

If the user asks for changes before the build ends:

1. Cancel the build run: `gh run cancel <run id>`.
2. Run `git checkout build/NNN-name` and `git pull`.
3. Change the spec. Commit and push.
4. If the build agent made no commits, the push starts a new build. If it made commits, tell the user. The user decides if you delete the branch and start again.
5. Run `git checkout main`.

After the pull request opens, the owner asks for changes with a pull request review and the `changes-requested` label. The label starts the fix agent. The fix agent reads the latest review.

## Rules

- Never push to `main`. Never merge a pull request.
- Never change a spec that is on `main`. Write a new spec for a change.
- One spec for each branch and each pull request.
- Do not open a pull request. The build agent opens it.
