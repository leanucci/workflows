# workflows

Shared agent workflows for my projects. The process is in [APPROACH.md](https://github.com/leanucci/portfolio/blob/main/APPROACH.md).

## The Cycle

1. **Spec:** The `/spec` skill pushes `specs/NNN-name.md` on the branch `build/NNN-name`. It opens no PR.
2. **Build:** The push starts the build agent. It adds the code, an entry in `JOURNAL.md`, and opens one PR with the spec and the code.
3. **Review:** The review agent reviews the PR. It adds `review-passed` or `changes-requested`, and `needs-human` when the change is sensitive (authentication, secrets, or an external API, service, or tool).
4. **Fix:** `changes-requested` starts the fix agent. It pushes fixes, and the push starts a new review. After 3 rounds, the PR gets `needs-human` instead, and the owner gets a review request.
5. **Merge:** `review-passed` starts the merge agent. It merges the PR, unless `needs-human` is set or the spec sets `Human approval: required`. In that case, the owner gets a review request and approves and merges by hand.
6. **Release:** The release workflow publishes when the version changes.

## Contents

| Path | Use | Projects use it by |
|---|---|---|
| `.github/workflows/agent.yml` | Router: sends each event to build, review, or fix | Reference |
| `.github/workflows/build.yml` | Build agent | Reference |
| `.github/workflows/review.yml` | Review agent | Reference |
| `.github/workflows/fix.yml` | Fix agent | Reference |
| `.github/workflows/merge.yml` | Merge agent | Reference |
| `.github/workflows/ci-ruby.yml` | Ruby tests | Reference |
| `.github/workflows/release-ruby-gem.yml` | Gem release | Reference |
| `.github/workflows/ci-node.yml` | Node tests: lint, type check, test, build | Reference |
| `.github/workflows/release-npm.yml` | npm package release | Reference |
| `prompts/` | Agent instructions | Reference |
| `skeleton/` | Start files for every project | Copy |
| `stacks/<stack>/` | Start files, rules, and required checks for one stack | Copy |
| `skills/` | Claude Code skills: `/spec` and `/new-project` | Link into `~/.claude/skills/` |
| `bin/setup-repo` | Labels and branch protection | Run one time |

## New Project

Use the `/new-project` skill. It does these steps:

1. Create the repo and clone it into a subfolder of `/Users/lean/work`.
2. Copy `skeleton/` into the repo, including `.github/`. Its only caller is `.github/workflows/agent.yml`.
3. Copy the stack files:
   - `stacks/<stack>/*.yml` into `.github/workflows/`.
   - `stacks/<stack>/gitignore` to `.gitignore`.
   - Append `stacks/<stack>/RULES.md` to `CLAUDE.md`.
4. Fill in the `TODO` values in `CLAUDE.md`.
5. Push to `main`.
6. Set the secrets:
   - `gh secret set CLAUDE_CODE_OAUTH_TOKEN --repo <owner/repo>`. The value comes from `claude setup-token`. It uses the owner's Claude subscription. As an alternative, set `ANTHROPIC_API_KEY` to use API billing.
   - Stack secrets, for example `gh secret set RUBYGEMS_API_KEY`.
7. Run `bin/setup-repo <owner/repo>` with the checks from `stacks/<stack>/required-checks`.
8. Make sure that the [Claude GitHub App](https://github.com/apps/claude) can access the repo.

## Skills

Install the skills one time:

```
ln -s /Users/lean/work/workflows/skills/spec ~/.claude/skills/spec
ln -s /Users/lean/work/workflows/skills/new-project ~/.claude/skills/new-project
```

- `/spec`: turns an idea into a spec and pushes it on a `build/` branch. The push starts the build.
- `/new-project`: creates a project that is ready for the cycle.

## Setup Notes

- **Agent identity.** The agents use the Claude GitHub App token. Events from that token start other workflows. Events from the default `GITHUB_TOKEN` do not.
- **One caller.** Projects call only `agent.yml`, from one caller file with all triggers and permissions. Changes to the shared workflows need no change in the projects.
- **Push events.** The Claude action does not run on `push`. So `agent.yml` finds the new spec on a push to `build/*` and starts a `workflow_dispatch` run on that branch. Pushes from `claude[bot]` do not start a build.
- **Rerun a build:** `gh workflow run agent.yml --ref build/NNN-name -f spec=specs/NNN-name.md`
- **Branch protection.** A merge to `main` needs one approval and the required checks.
  `enforce_admins` is off, so the owner can merge by hand when a pull request needs human
  approval, since a real review already happened.
- **Identities.** The build agent opens pull requests under the project owner's own identity
  (the Claude Code OAuth token), not a bot. GitHub blocks a self-review, so the owner can never
  approve or request changes on these pull requests directly. The review agent approves a PASS
  verdict as the separate `claude` bot identity, which satisfies the approval requirement
  without being a self-review. The merge agent then merges with the default `GITHUB_TOKEN`, a
  third identity.
- **Auto-merge.** `bin/setup-repo` turns on "Allow auto-merge" for the repo. The merge agent uses `gh pr merge --auto`, so the merge waits for the required checks even when they are still running.
- **Models.** Build and fix use `claude-opus-5-5`. Review uses `claude-sonnet-5-5`, a different model, so the two agents make different mistakes. A caller can change them with the `model` input.

## Versions

Projects call `@v1`. To release a change, move the tag:

```
git tag -f v1 && git push -f origin v1
```

Use a new major tag (`v2`) for a change that breaks the callers.
