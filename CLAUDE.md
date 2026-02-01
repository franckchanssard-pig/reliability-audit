# CLAUDE.md

This file provides guidance for AI assistants working with this repository.

## Repository Overview

**Change Readiness Survey** — A web app for Pigment customers to assess change management readiness via a 15-question Likert survey. Computes per-dimension and overall scores (0–100), surfaces top risks and gating warnings, and provides rule-based recommendations.

## Project Structure

```
change-readiness-survey/           # Next.js 14+ App Router project
├── src/
│   ├── app/
│   │   ├── page.tsx               # Landing page — context form (Step 1)
│   │   ├── layout.tsx             # Root layout
│   │   ├── globals.css            # Tailwind + CSS custom properties
│   │   ├── survey/[id]/page.tsx   # Survey page — 15 Likert questions (Step 2)
│   │   ├── results/[id]/page.tsx  # Results dashboard (Step 3)
│   │   └── api/responses/         # REST API routes
│   │       ├── route.ts           # POST /api/responses
│   │       └── [id]/
│   │           ├── route.ts       # GET /api/responses/[id]
│   │           ├── answers/route.ts     # POST answers
│   │           └── export.csv/route.ts  # GET CSV export
│   └── lib/
│       ├── types.ts               # TypeScript types
│       ├── questionnaire.ts       # 15 questions, 5 dimensions, gating flags
│       ├── scoring.ts             # Score computation + recommendation rules
│       ├── db.ts                  # SQLite persistence via sql.js
│       └── sql.js.d.ts            # Type declarations for sql.js
├── data/                          # SQLite DB + wasm (gitignored)
├── package.json
├── README.md
└── CLAUDE.md                      # This file (repo root)
```

## Development Setup

```bash
cd change-readiness-survey
npm install          # Installs deps + copies sql-wasm.wasm to data/
npm run dev          # Starts dev server at http://localhost:3000
```

## Common Commands

```bash
npm run dev          # Start development server (Turbopack)
npm run build        # Production build
npm start            # Start production server
npm run lint         # ESLint
rm data/survey.db    # Reset the SQLite database
```

## Tech Stack

- **Next.js 16** with App Router, TypeScript, Turbopack
- **Tailwind CSS v4** for styling
- **sql.js** (SQLite → WebAssembly) for server-side persistence
- **uuid** for response IDs
- No auth, no external services

## Code Style & Conventions

- TypeScript strict mode via `tsconfig.json`
- ESLint with `eslint-config-next`
- Tailwind utility classes with CSS custom properties for theme colors (`--primary`, `--green`, `--orange`, `--red`)
- Client components use `"use client"` directive; API routes are server-only
- All API responses return JSON (except CSV export)

## Architecture Notes

- **Database**: Single SQLite file (`data/survey.db`), auto-created on first request. Answers stored as JSON blob (`answers_json` column) for simplicity.
- **Scoring**: `((avg - 1) / 4) * 100` maps Likert 1–5 to 0–100. Traffic light thresholds: Red < 40, Orange 40–69, Green ≥ 70.
- **Gating questions**: Q1, Q8, Q13. If ≤ 2, trigger warnings regardless of dimension average.
- **Recommendations**: Rule-based in `scoring.ts` — each dimension has a threshold (< 60) plus gating overrides.
- **Questionnaire data**: Defined in `questionnaire.ts` as a typed array — easy to edit questions, dimensions, and gating flags.

## Important Caveats

- `sql.js` wasm binary must exist at `data/sql-wasm.wasm` — the `postinstall` script handles this automatically.
- The DB singleton is held in module scope; in dev mode with hot reload, this can occasionally cause stale connections. Restarting the dev server fixes it.
- No authentication — anyone with the URL can view results.
