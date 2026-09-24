# victor-resum-web

Static portfolio and blog site for Victor Kipruto Rop, deployed to
Cloudflare Workers as a static-asset-only site.

## Repository layout

| Path        | Purpose                                                                                     |
| ----------- | ------------------------------------------------------------------------------------------- |
| `public/`   | **The only published directory.** Everything Cloudflare Workers serves lives here.          |
| `content/`  | Source content: hand-written posts (`posts/`) and AI-generated drafts (`ai-generated/`).     |
| `ops/`      | Private tooling: automation scripts, subscriber data, analytics, distribution, notifications. |
| `.github/`  | CI workflows (notification, distribution, image assignment, maintenance, Pages deploy).      |

Browser URLs are rooted at the domain (e.g. `/blog`, `/posts/...`,
`/assets/...`). `public/` is a filesystem/deployment boundary only — it is
never a URL segment.

## Requirements

- Node.js 18+ and npm
- Wrangler (installed via `npm install`)

## Commands

```bash
npm install         # install dev dependencies (wrangler)
npm run dev         # local development server (wrangler dev)
npm run dry-run     # validate the deploy without publishing
npm run deploy      # deploy to Cloudflare Workers
```

`wrangler.jsonc` pins the asset directory to `./public`. Do not change it to
`"."` — that would upload `ops/` (including subscriber data) with the site.

## Private data

`ops/subscribers/`, `ops/dispatch_logs/`, `ops/notifications/`,
`ops/analytics/`, `ops/state/`, and any `.env` files are operational data.
They must never be moved into `public/`. `public/.assetsignore` is a second
line of defense that excludes them from the asset upload if they ever are.

## GitHub Pages (legacy)

The `static.yml` workflow still builds `_site/` from `public/` via
`ops/tools/build_site.py` and can deploy to GitHub Pages. The canonical
target is Cloudflare Workers.
