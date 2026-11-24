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

### Publish

- The package publishes to the public npm registry, under the name in `package.json`.
- Publish only when the `version` field in `package.json` changes. `release.yml` does this.
- Store the npm token in the `NPM_TOKEN` repo secret.
- Set `"files"` in `package.json` to the built output only, for example `["dist"]`.
