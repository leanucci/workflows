# Review Output: Antigravity

## Files

The workflow put these files in `.review/`:

- `.review/pr.md`: the pull request title and description.
- `.review/pr.diff`: the full diff of the pull request.
- `.review/checks.txt`: the CI check results when the review started. CI can still be running.

Read the rest of the repo when you need context. You can read files, but you cannot change them or run commands. Do not try to post the review yourself.

## Output

End your answer with exactly one JSON block in this format, and nothing after it:

```json
{
  "verdict": "PASS",
  "body": "## Verdict\nPASS\n\n## Blocking\nNone.\n\n## Non-Blocking\n1. ..."
}
```

- `verdict`: `PASS` or `CHANGES REQUESTED`. It must agree with the review body.
- `body`: the full review in the review format, as one JSON string. Escape new lines as `\n` and quotes as `\"`.
