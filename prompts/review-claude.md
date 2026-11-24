# Review Output: Claude

## Tools

You have a limited tool set. Commands outside it fail.

- Read the pull request with `gh pr view <number>` and `gh pr diff <number>`.
- Use the Read, Glob, and Grep tools to read files. Do not use `cat`, `head`, `grep`, or `find` in Bash.
- Run each command alone. Do not use pipes (`|`), `&&`, `;`, or redirects (`>`).
- Allowed commands: `gh pr view`, `gh pr diff`, `gh pr review`, `gh pr edit`, `gh pr checks`, `gh api`, `git log`, `git diff`, `git show`, `git status`, `git rev-parse`, and `ls`.
- You cannot write files. You cannot run tests. Use the CI result: `gh pr checks <number>`.

## Output

1. Post one review. Put the full review text in the `--body` value in both cases:
   - CHANGES REQUESTED: `gh pr review <number> --comment --body "<review>"`.
   - PASS: `gh pr review <number> --approve --body "<review>"`. This formally approves the pull
     request. The branch protection review requirement does not block the owner later, even when
     the merge waits for the owner for another reason.
2. Set one verdict label:
   - CHANGES REQUESTED: `gh pr edit <number> --add-label changes-requested`
   - PASS: `gh pr edit <number> --add-label review-passed`
3. When "Needs Human" is not "None.", also run `gh pr edit <number> --add-label needs-human`.

Never use `--request-changes`. Never change code. Never push.
