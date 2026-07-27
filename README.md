# Chiara — Cervia 70.3

Training dashboard and race analysis for Ironman 70.3 Emilia-Romagna, Cervia, 17 September 2026.

**Target 4:59:45.** Personal best 5:22:59 (same course, 2025).

## The dashboard

`index.html` is a single self-contained page — no build step, no dependencies, no framework. It reads `data/plan.json` at runtime and shows:

- **Today's training** — the day's sessions in full, with sets and detail
- **Calendar** — all 53 days from 27 July to race day, grouped by block, click any day to expand
- **Race plan** — target splits leg by leg

Works offline once loaded, reads well on a phone, and follows the system light/dark setting.

### Run it locally

Just double-click `index.html`. The plan is baked into the page, so it works straight from disk with no server.

Optionally, to have edits to `data/plan.json` appear without rebuilding:

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

When served over http the page prefers the live `data/plan.json`; opened from disk it falls back to the embedded copy.

## Deploying

**One-time setup, required before the first run:**

Repository → **Settings → Pages → Build and deployment → Source: GitHub Actions** → Save.

Without this the workflow fails with `Get Pages site failed … Not Found`. The action cannot enable Pages itself — its `enablement` option needs a personal access token rather than the default `GITHUB_TOKEN`.

Then push to `main`, or run the workflow manually from the Actions tab. It bakes `data/plan.json` into `index.html` and publishes.

> **Note the date.** `configure-pages`, `upload-pages-artifact` and `deploy-pages` still run on Node 20, which GitHub removes from runners on **16 September 2026 — the day before the race.** Until then it is only a warning. Check for newer major versions in early September and bump them. If the deploy ever breaks, `index.html` still works offline, so nothing is lost on race day.

> **Privacy.** GitHub Pages is public, and this dashboard carries a named athlete's training and race data. If that isn't wanted, use a **private repo with GitHub Pages on a paid plan**, or remove the name from `data/plan.json` and `index.html`. The `.gitignore` already excludes all raw health data — `raw/`, every `.FIT` file, and every per-session CSV. Check `git status` before the first push.

## Editing the plan

Everything lives in `data/plan.json`. No code changes needed.

After editing, run `python3 build.py` to bake the change into `index.html` so the offline copy stays in step. The GitHub Action runs this automatically on deploy, so forgetting it only affects the local file.

```jsonc
{
  "date": "2026-08-08",
  "block": "Block 1 · Build",
  "note": "optional, shown once for the day",
  "sessions": [
    {
      "sport": "run",          // swim | bike | run | brick | strength | rest | race
      "title": "Long run 16 km",
      "priority": "A",         // A never skip · B move it · C nice to have
      "duration": "1:40",
      "detail": "13 km easy, then 3 km at 4:40/km.",
      "sets": ["optional", "list of steps"]
    }
  ]
}
```

## Repository layout

```
index.html              the dashboard
data/plan.json          the training plan — the only file to edit
docs/                   analysis and written plans
  race_plan_cervia.md       target splits and where the time comes from
  training_plan_to_cervia.md  the full written plan with glossary
  coach_playbook.md         how the previous coach programmed
  athlete_dossier.md        strengths, weaknesses, zones
  athlete_baseline.md       first-pass baseline
  coach_replacement_plan.md the overall project plan
analysis/charts/        fitness, decoupling, volume, swim charts
analysis/_make_charts.py  regenerates the charts
raw/                    FIT files and TrainingPeaks exports — gitignored
.github/workflows/      Pages deployment
```

## The short version

Three levers decide the race, and only one is training:

1. **Run** — 10 minutes. Long run to 21 km, race-pace finishes. She ran 4:26/km off the bike at Karlsfelder in July.
2. **Bike** — 7 minutes. Aero helmet, bike fit, and time spent in the bars. Bought, not trained.
3. **Transitions** — 2 to 3 minutes. Cervia's transitions are structurally slow; the winner took 8:00. Drill them anyway.

The swim is at maintenance. It has been flat since May and six weeks will not move it.

**Her power meter reads nonsense** — 89 W recorded during a 35 km/h race. All bike pacing is written in heart rate: 152-158 on race day.
