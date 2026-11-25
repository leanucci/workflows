## Node Package Rules

Append this section to the project `CLAUDE.md`.

### Stack

- TypeScript in strict mode. Build to `dist/` with `tsc`.
- Vitest for tests.
- ESLint for lint.
- npm for packages. Commit `package-lock.json`.

### Scripts

`package.json` must have these scripts. CI runs each one:

- `lint`: ESLint with no warnings.
- `typecheck`: `tsc --noEmit`.
- `test`: Vitest in run mode (not watch mode).
- `build`: compile to `dist/`.

### Code

- Use TSDoc comments for exported functions, classes, and types.
- Keep secrets, certificates, and private keys out of the repo. Read them from environment variables or from files the caller provides.

### Release Policy

- Releases happen by hand, with the `/release` skill. Specs accumulate on `main` until then.
- The build agent never changes the version in `package.json`. Each entry it adds under
  `## [Unreleased]` in `CHANGELOG.md` starts with its severity in parentheses, from the spec's
  "Release" field: `(major)`, `(minor)`, or `(patch)`.
- `/release` computes the new version from the highest severity under `## [Unreleased]`, moves
  those entries under that version with today's date, and sets the version in `package.json`.

### Publish

- The package publishes to the public npm registry, under the name in `package.json`.
- Publish only when the `version` field in `package.json` changes. `release.yml` does this.
  `/release` is the only thing that changes it.
- `release.yml` stages the publish with npm trusted publishing (OIDC). It needs no npm token.
- A staged publish is not live. The owner approves it by hand, from their own machine, with
  `npm stage approve <stage-id>`. 2FA always applies to that step. No CI identity can do it.
  Find the stage ID with `npm stage list <package-name>` if it is not in the job's log.
- After the owner approves the staged publish, the owner creates the `v<version>` tag and
  the GitHub release. `release.yml` does not do this, because it does not know when, or if,
  the owner approves.
- Set `"files"` in `package.json` to the built output only, for example `["dist"]`.

### First Release Setup

npm needs the package to exist before it accepts a Trusted Publisher for it. Do this once,
by hand, before the first automated release:

1. Publish a placeholder version from this project, logged in to npm as a human, so the
   package exists. A tool such as `setup-npm-trusted-publish` can do this without publishing
   real content.
2. On npmjs.com, open the package's Settings page and add a Trusted Publisher: GitHub
   Actions, this repository, workflow filename `release.yml` (the filename only, not the
   path). Leave the environment blank.
3. The first automated release still ends in a staged publish. Approve it as the Publish
   section above describes.
