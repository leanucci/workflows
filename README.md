# workflows

Shared agent workflows for my projects. The process is in [APPROACH.md](https://github.com/leanucci/portfolio/blob/main/APPROACH.md).

## The Cycle

1. **Spec:** An agent pushes `specs/NNN-name.md` on the branch `spec/NNN-name`. The spec workflow opens the PR as `github-actions[bot]` and requests the owner's review. The owner approves and merges.
2. **Build:** The merge starts the build agent. It writes the code and opens a PR on the branch `build/NNN-name`.
3. **Review:** The review agent reviews the PR. It adds `review-passed` or `changes-requested`.
4. **Fix:** `changes-requested` starts the fix agent. It pushes fixes, and the push starts a new review. After 3 rounds, the PR gets `needs-human`.
5. The owner gets a review request and merges.
6. **Release:** The release workflow publishes when the version changes.

## Contents

| Path | Use | Projects use it by |
|---|---|---|
| `.github/workflows/spec-pr.yml` | Opens spec PRs | Reference |
| `.github/workflows/build.yml` | Build agent | Reference |
| `.github/workflows/review.yml` | Review agent | Reference |
| `.github/workflows/fix.yml` | Fix agent | Reference |
| `.github/workflows/ci-ruby.yml` | Ruby tests | Reference |
| `.github/workflows/release-ruby-gem.yml` | Gem release | Reference |
| `.github/workflows/ci-node.yml` | Node tests: lint, type check, test, build | Reference |
| `prompts/` | Agent instructions | Reference |
| `skeleton/` | Start files for every project | Copy |
| `stacks/<stack>/` | Start files for one stack | Copy |
| `bin/setup-repo` | Labels, workflow permissions, and branch protection | Run one time |

## New Project

1. Create the repo and clone it into a subfolder of `/Users/lean/work`.
2. Copy `skeleton/` into the repo, including `.github/`.
3. Copy the stack files:
   - `stacks/<stack>/*.yml` into `.github/workflows/`.
   - `stacks/<stack>/gitignore` to `.gitignore`.
   - Append `stacks/<stack>/RULES.md` to `CLAUDE.md`.
4. Fill in the `TODO` values in `CLAUDE.md`.
5. Push to `main`.
6. Set the secrets:
   - `gh secret set CLAUDE_CODE_OAUTH_TOKEN --repo <owner/repo>`. The value comes from `claude setup-token`. It uses the owner's Claude subscription. As an alternative, set `ANTHROPIC_API_KEY` to use API billing.
   - Stack secrets, for example `gh secret set RUBYGEMS_API_KEY`.
7. Run `bin/setup-repo <owner/repo> "<required check>"`.
8. Make sure that the [Claude GitHub App](https://github.com/apps/claude) can access the repo.

## Setup Notes

- **Agent identity.** The agents use the Claude GitHub App token. Events from that token start other workflows. Events from the default `GITHUB_TOKEN` do not.
- **Push events.** The Claude action does not run on `push`. So the build workflow finds new specs on `push` and starts one `workflow_dispatch` run for each spec.
- **Rerun a build:** `gh workflow run build.yml -f spec=specs/NNN-name.md`
- **Branch protection.** A merge to `main` needs one approval and the required checks. Admins cannot bypass it. Bots open all PRs, so the owner can always approve. Agents never approve or merge.
- **Workflow permissions.** `bin/setup-repo` lets workflows create PRs. GitHub has one setting for "create and approve", but no workflow here approves.
- **CI on spec branches.** PRs that `GITHUB_TOKEN` opens do not start `pull_request` workflows. So CI also runs on push to `spec/**`, and its checks attach to the spec commit.
- **Models.** Build and fix use `claude-opus-5-5`. Review uses `claude-sonnet-5-5`. A caller can change them with the `model` input.

## Versions

Projects call `@v1`. To release a change, move the tag:

```
git tag -f v1 && git push -f origin v1
```

Use a new major tag (`v2`) for a change that breaks the callers.
