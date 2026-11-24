---
name: release
description: Cut a release for a project that accumulates specs on main until the owner decides to release. Reads CHANGELOG.md's Unreleased section, computes the version bump from the highest severity tag, moves the entries under a new version heading, bumps the version file, and pushes to main. The push starts the project's release workflow, which publishes the package. Use when the user wants to release, publish, or cut a new version of a project with a "by hand" release policy (for example, the node-package stack), or types /release.
---

# Release

Cut a release for a project whose specs accumulate on `main` until the owner decides to
publish. This skill computes the version, updates `CHANGELOG.md` and the version file, and
pushes to `main`. The push starts the existing release workflow, which publishes the package.

The process is in `/Users/lean/work/portfolio/APPROACH.md`.

## Inputs

- **Project:** see "Find the Project" below.
- **Bump:** optional. The user can force `major`, `minor`, or `patch`. Otherwise, compute it.

## Find the Project

Use the same rules as the `/spec` skill: the session folder and the conversation first, then
the name and the description against `/Users/lean/work/portfolio/PROJECTS.md`.

The project's `CLAUDE.md` must have a "Release Policy" section that names `/release` (for
example, the `node-package` stack adds one). If it does not, stop. Tell the user that this
project releases a version on every spec instead, so there is nothing to cut by hand.

## Steps

1. **Check the project.**
   - Run `git status`. If the working tree has changes, stop and tell the user.
   - Run `git checkout main` and `git pull`.
   - Check the latest run of the required CI check on `main`:
     `gh run list --branch main --workflow ci.yml --limit 1 --json conclusion`.
     If it did not succeed, stop and tell the user.

2. **Read `CHANGELOG.md`.** Find the `## [Unreleased]` section.
   - If it has no entries, stop. Tell the user there is nothing to release.

3. **Compute the bump.**
   - Read the severity in parentheses at the start of each `## [Unreleased]` bullet:
     `(major)`, `(minor)`, or `(patch)`. Treat a bullet with no tag as `(patch)`.
   - The bump is the highest severity found: `major` beats `minor` beats `patch`.
   - If the user named a bump in the input, use it instead. Tell the user when it is lower
     than the one the entries call for.

4. **Compute the new version.** Read the current version from the version file that `CLAUDE.md`
   names (for example `package.json`). Apply the bump with semantic versioning.

5. **Rewrite `CHANGELOG.md`.**
   - Rename `## [Unreleased]` to `## [<new version>] - <today, YYYY-MM-DD>`.
   - Add a new, empty `## [Unreleased]` section above it.

6. **Set the version** in the version file to `<new version>`.

7. **Show the user the diff** of `CHANGELOG.md` and the version file, and the computed bump.
   Do not wait for an answer. The user started this by asking for a release.

8. **Commit and push.**
   - Commit `Release v<new version>`, with both co-author lines from the shared rules.
   - Push to `main` directly. The project's branch protection lets the owner bypass the
     required review and checks, so this push needs no pull request.

9. **Report.**
   - The new version and the commit.
   - The release workflow starts on the push. Find the run with
     `gh run list --workflow release.yml --branch main --limit 1`.
   - It publishes the package once its own tests and build pass, and it creates a GitHub
     release and a tag.

## Rules

- Only run this skill when the user asks to release, publish, or cut a version.
- Never run this skill on a project with a per-spec release policy. Its version already
  changes on every merge, and `CLAUDE.md` names no "Release Policy" section.
- Push to `main` only as the last step, after the user has seen the diff.
