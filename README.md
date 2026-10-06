# workflows

Shared agent workflows for my projects. The process is in [APPROACH.md](https://github.com/leanucci/portfolio/blob/main/APPROACH.md).

## The Cycle

1. **Spec:** The `/spec` skill pushes `specs/NNN-name.md` on the branch `build/NNN-name`. It opens no PR.
2. **Build:** The push starts the build agent. It adds the code to the same branch and opens one PR with the spec and the code.
3. **Review:** The review agent reviews the PR. It adds `review-passed` or `changes-requested`. The default reviewer is Google Antigravity (Gemini). Set `reviewer: claude` in the caller to use Claude.
4. **Fix:** `changes-requested` starts the fix agent. With Antigravity, `review.yml` calls `fix.yml` directly, because labels from `GITHUB_TOKEN` do not start workflows. It pushes fixes, and the push starts a new review. After 3 rounds, the PR gets `needs-human`.
5. **Approve:** The owner gets a review request. The owner approves the spec and the code together, and merges.
6. **Release:** The release workflow publishes when the version changes.

## Contents

| Path | Use | Projects use it by |
|---|---|---|
| `.github/workflows/agent.yml` | Router: sends each event to build, review, or fix | Reference |
| `.github/workflows/build.yml` | Build agent | Reference |
| `.github/workflows/review.yml` | Review agent | Reference |
| `.github/workflows/fix.yml` | Fix agent | Reference |
| `.github/workflows/ci-ruby.yml` | Ruby tests | Reference |
| `.github/workflows/release-ruby-gem.yml` | Gem release | Reference |
| `.github/workflows/ci-node.yml` | Node tests: lint, type check, test, build | Reference |
| `prompts/` | Agent instructions | Reference |
| `scripts/review_antigravity.py` | Runs the Antigravity review | Reference |
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
   - `gh secret set GEMINI_API_KEY --repo <owner/repo>`. The value is a Gemini API key from https://aistudio.google.com/apikey. The Antigravity reviewer uses it.
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
- **Branch protection.** A merge to `main` needs one approval and the required checks. Admins cannot bypass it. The build agent opens all PRs, so the owner can always approve. Agents never approve or merge.
- **Models.** Build and fix use `claude-opus-5-5`. Review uses Google Antigravity. It tries the SDK default Gemini model, then `gemini-3.7-flash`, then `gemini-2.5-flash`, with 6 minutes for each. A caller can change them with the `model` and `antigravity_models` inputs.
- **Antigravity reviewer.** The SDK runs in read-only mode. It cannot change files or run commands. The agent returns its verdict as JSON, and the workflow posts the review with `GITHUB_TOKEN`.

## Versions

Projects call `@v1`. To release a change, move the tag:

```
git tag -f v1 && git push -f origin v1
```

Use a new major tag (`v2`) for a change that breaks the callers.
