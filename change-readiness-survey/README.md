# Change Readiness Survey

A minimal, production-quality web app for assessing change management readiness for Pigment implementations. 15 Likert-scale questions across 5 dimensions, with automated scoring, risk analysis, and recommendations.

## Quick Start

```bash
cd change-readiness-survey
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## How It Works

1. **Start** — Enter company/project context and begin the survey
2. **Survey** — Answer 15 questions (Likert 1–5) grouped into 5 dimensions
3. **Results** — View scores per dimension, overall readiness, top risks, and recommendations

Results are persisted in SQLite and accessible via a shareable URL (`/results/{id}`).

## Tech Stack

- **Next.js 14+** with App Router and TypeScript
- **Tailwind CSS** for styling
- **sql.js** (SQLite compiled to WebAssembly) for persistence
- No authentication, no external services

## Scoring

- Each question is scored 1–5 (Strongly Disagree → Strongly Agree)
- Dimension score = `((average - 1) / 4) × 100` → 0–100
- Overall score = average of all 5 dimension scores
- Traffic light: **Red** < 40, **Orange** 40–69, **Green** ≥ 70

## Gating Questions

Three questions are marked as "gating" (Q1, Q8, Q13). If scored ≤ 2, they trigger explicit warnings regardless of dimension averages.

## Export CSV

Click "Export CSV" on any results page, or fetch directly:

```
GET /api/responses/{id}/export.csv
```

## Reset Database

Delete the SQLite file and restart:

```bash
rm data/survey.db
npm run dev
```

## API Routes

| Method | Route | Description |
|--------|-------|-------------|
| POST | `/api/responses` | Create a new response (returns `{ id }`) |
| POST | `/api/responses/[id]/answers` | Save 15 answers |
| GET | `/api/responses/[id]` | Fetch response + computed scores |
| GET | `/api/responses/[id]/export.csv` | Download CSV export |

## Project Structure

```
src/
├── app/
│   ├── page.tsx                          # Landing page + context form
│   ├── survey/[id]/page.tsx              # Survey questions
│   ├── results/[id]/page.tsx             # Results dashboard
│   └── api/responses/                    # API routes
├── lib/
│   ├── types.ts                          # TypeScript types
│   ├── questionnaire.ts                  # 15 questions, dimensions
│   ├── scoring.ts                        # Score computation + recommendations
│   └── db.ts                             # SQLite persistence layer
data/
└── survey.db                             # SQLite database (auto-created)
```
