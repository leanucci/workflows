## Go Rules

Append this section to the project `CLAUDE.md`.

### Stack

- Go modules. Commit `go.sum`.
- Standard library `testing` package. Run tests with `go test ./...`.
- `go vet ./...` for lint. No separate linter.

### Code

- Use Go doc comments: a sentence starting with the identifier's name, directly above each
  exported function, type, and constant.
- Keep secrets, certificates, and private keys out of the repo. Read them from environment
  variables or from files the caller provides.

### Release Policy

- Releases happen by hand, with the `/release` skill. Specs accumulate on `main` until then.
- The build agent never changes `VERSION`. Each entry it adds under `## [Unreleased]` in
  `CHANGELOG.md` starts with its severity in parentheses, from the spec's "Release" field:
  `(major)`, `(minor)`, or `(patch)`.
- `/release` computes the new version from the highest severity under `## [Unreleased]`,
  moves those entries under that version with today's date, and sets `VERSION`.

### Publish

- There is no publish step and no registry account. Go's module proxy
  (`proxy.golang.org`) discovers a version from its git tag the first time anything fetches
  it.
- `release.yml` creates and pushes the `v<version>` tag, and the GitHub release, once
  `VERSION` changes. No secret, no token, no approval.

### First Release Setup

Nothing to set up. The first `v<version>` tag `release.yml` creates is the first thing the
module proxy indexes.
