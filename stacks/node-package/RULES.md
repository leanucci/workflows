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
- `release.yml` publishes with npm trusted publishing (OIDC). It needs no npm token.
- Set `"files"` in `package.json` to the built output only, for example `["dist"]`.

### First Release Setup

npm needs the package to exist before it accepts a Trusted Publisher for it. Do this once,
by hand, before the first automated release:

1. Run `npm publish` from this project, logged in to npm as a human. This publishes the
   first version.
2. On npmjs.com, open the package's Settings page and add a Trusted Publisher: GitHub
   Actions, this repository, workflow filename `release.yml`. Leave the environment blank.
3. Tell the owner to create the matching git tag and GitHub release by hand for the version
   from step 1, since the automated workflow did not run for it.
