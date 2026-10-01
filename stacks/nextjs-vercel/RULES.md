## Next.js Rules

Append this section to the project `CLAUDE.md`.

### Stack

- Next.js with the App Router, TypeScript in strict mode, and React.
- Tailwind CSS for styles.
- Vitest and React Testing Library for tests.
- ESLint for lint.
- npm for packages. Commit `package-lock.json`.

### Scripts

`package.json` must have these scripts. CI runs each one:

- `lint`: ESLint with no warnings.
- `typecheck`: `tsc --noEmit`.
- `test`: Vitest in run mode (not watch mode).
- `build`: `next build`.

### Code

- Use TSDoc comments for exported functions, components, and types.
- Use server components by default. Add `"use client"` only when a component needs browser APIs or state.
- Put browser storage access in one module. Do not call `localStorage` directly from components.
- Keep secrets in environment variables. Never expose a secret to the client. Only `NEXT_PUBLIC_*` variables reach the browser.
- Document each environment variable in `.env.example`.

### Deploy

- Vercel deploys each merge to `main`. Each pull request gets a preview URL.
- Web apps do not use version numbers. Use `Release: none` in specs. Add changelog entries under `Unreleased`.
