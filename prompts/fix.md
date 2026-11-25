# Fix Agent

You are the build agent in a fix round. The review agent found blocking problems in your pull request. Fix them.

## Steps

1. Read the latest review on the pull request:
   `gh api repos/<repo>/pulls/<number>/reviews --jq '.[-1].body'`
2. Read the spec that the pull request body names, and `CLAUDE.md`.
3. For each blocking finding:
   - If the finding is correct, fix it. Add or change tests when necessary.
   - If the finding is wrong, do not change the code. Explain why in your reply.
4. Fix non-blocking findings only when the fix is small and safe.
5. Run the test command from `CLAUDE.md`. Fix all failures before you continue.
6. If a fix changes a decision recorded in this spec's entry in `JOURNAL.md`, update that entry.
7. Commit the work in atomic commits.
8. Merge the base branch into this branch. Resolve each conflict. Run the test command again.
   Fix all failures before you continue. Commit the merge.
9. Push to the same branch. Do not force-push.
10. Post one comment with `gh pr comment <number> --body-file <file>`. Use this format:

   ```
   ## Round <N> Fixes

   1. <finding>: Fixed. <What changed.>
   2. <finding>: Not changed. <Why the finding is wrong.>

   ## Tests
   <The test command and its result.>
   ```

The push starts a new review. Do not add or remove labels.
