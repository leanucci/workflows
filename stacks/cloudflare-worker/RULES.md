## Cloudflare Worker Rules

Append this section to the project `CLAUDE.md`.

### Stack

- TypeScript in strict mode. Wrangler builds and deploys the Worker.
- Vitest for tests.
- ESLint for lint.
- npm for packages. Commit `package-lock.json`.

### Scripts

`package.json` must have these scripts. CI runs each one:

- `lint`: ESLint with no warnings.
- `typecheck`: `tsc --noEmit`.
- `test`: Vitest in run mode (not watch mode).
- `build`: `wrangler deploy --dry-run --outdir dist`. This checks the Worker bundles. It does
  not deploy and does not need a Cloudflare token.

### Code

- Use TSDoc comments for exported functions, classes, and types.
- Keep secrets out of the repo. Read them from Worker secrets (`wrangler secret put <NAME>`),
  never from a committed file.

### Deploy Policy

- The Worker deploys on every merge to `main`. No version file, and no accumulated release.
  This stack ships continuously, like a web app.
- `deploy.yml` runs after CI passes, and deploys the current `main` with `wrangler deploy`.

### First Deploy Setup

Do this once, by hand, before the first automated deploy:

1. Create the Worker on Cloudflare. Note the account ID.
2. Create a Cloudflare API token scoped to edit Workers for this account.
3. Set `name` in `wrangler.toml` to the repo name.
4. Set both secrets on the repo:
   `! gh secret set CLOUDFLARE_API_TOKEN --repo leanucci/<name>`
   `! gh secret set CLOUDFLARE_ACCOUNT_ID --repo leanucci/<name>`
5. Any secret the Worker reads at runtime (for example, a GitHub App credential):
   `! wrangler secret put <NAME>`, run locally, once. Worker secrets do not come from
   GitHub Actions secrets; `deploy.yml` never sets them.
