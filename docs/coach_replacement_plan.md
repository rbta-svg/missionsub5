# Replacing the Coach — A Plan

*14 July 2026. Race: Ironman 70.3, 17 September — nine weeks out. Subject: the athlete in the TrainingPeaks data ("Chiara").*

## The idea in one paragraph

Rebuild the coach in three layers. First, learn how the old coach programmed — her weekly template, her session types, her voice. Second, study the athlete harder than the coach ever did, down to the per-second record data. Third, put both into an AI coach that lives in a dashboard: it watches new sessions arrive, evaluates them against the plan, and writes next week's training in the old coach's style — then pushes it into TrainingPeaks so it lands on the athlete's Garmin as a structured workout.

## What we already have, and what's missing

We have 106 completed workout files (April–July) and a parsed dataset (`analysis/workouts.csv`). We do not have the *plan*: the FIT export contains only what was done, not what was assigned. The coach's programming — workout titles, descriptions, structure, pre- and post-session comments, planned-vs-completed compliance — lives in the TrainingPeaks calendar, and we have the credentials. We are also missing January–March entirely. Both problems have the same fix: pull it from the TP web app directly.

A note on the credentials: the coach handed them over, so consent exists, but automated use of an account is grey territory under TP's terms. Low risk in practice; worth knowing.

---

## Phase 0 — Get all the data (this week)

Log into TrainingPeaks in the browser (Claude drives Chrome) and extract, month by month since January: every calendar entry with its title, description, planned structure, planned duration/TSS, the completed values next to it, and every comment thread between coach and athlete. Save as JSON next to the FIT data. Also export January–March workout files if they exist in the account. This single scrape feeds both Phase 1 and Phase 2.

## Phase 1 — The coach persona study

From the scraped calendar, reconstruct the coach's playbook: the weekly skeleton (which discipline on which day, how often the rest day moves), the session archetypes she reused (name them, catalogue their structure), how she progressed load (build weeks vs recovery weeks, long-ride and long-run growth rates), how she reacted when sessions were missed or botched, and her language — how she titled things, how she praised, how she corrected. The output is a **coach playbook**: a persona document plus a session template library. This is what keeps the new training feeling like *her* training.

## Phase 2 — The deep analysis the old coach never did

Go past session summaries into the per-second records inside each FIT file. The questions worth answering: aerobic efficiency trend (pace-vs-HR and power-vs-HR decoupling on long sessions, month over month), swim mechanics (stroke count, SWOLF, pace decay across sets), run durability (pace fade in the final third of long runs, brick-run penalty vs fresh-run pace), heat sensitivity, and real training zones — the FTP field in her files is junk, so we derive zones from observed data and propose one field test per discipline to confirm. Also compute our own training load (hrTSS/rTSS from HR and pace), since TSS is absent from most files; without it there is no honest fitness/fatigue model. The output is an **athlete dossier**: evidenced strengths and weaknesses, zones, and the three highest-leverage things to fix before 17 September.

## Phase 3 — The AI coach dashboard

A live dashboard (built as a Cowork artifact, so it persists and refreshes) with four panes: fitness and fatigue (CTL/ATL/TSB from our computed TSS), this week planned vs completed, discipline trends, and race countdown with predicted splits updating as form changes.

Behind it, two engines:

**Session evaluator.** Each new workout is compared against what was planned and scored — did she hit the targets, how did HR behave, what does it change about the week. It writes feedback in the coach's voice, using the Phase 1 persona.

**Week generator.** Given the race date, current form, compliance last week, and her availability, it assembles next week from the Phase 1 template library, adjusted by the Phase 2 dossier. Generation at a week's notice is the design requirement; a fallback rule set handles curveballs (illness, travel, missed long ride).

## Phase 4 — Run the race build

Nine weeks: roughly five of build, two of peak, two of taper. Weekly rhythm: Sunday — evaluate the week, generate the next, push to TP; daily — evaluate incoming sessions. The prediction model updates its 6:15 estimate as evidence arrives.

---

## Talking to TrainingPeaks — the honest answer

**Yes, it's a thing — three ways, and we can use two of them.**

**1. File import (official, easiest).** TrainingPeaks lets coaches and athletes import planned structured workouts as `.zwo` files into the Workout Library (⋮ menu on a library folder → Import Workout; bulk import supported), then drag them onto the calendar. Once on the calendar, structured workouts sync automatically to her Garmin as on-device workouts. Catch: `.zwo` is the only accepted format and it is a power-based cycling format — perfect for bike sessions, not for run pace or swim workouts.

**2. Browser automation with the coach account (full fidelity).** We hold coach credentials, and TP's own Structured Workout Builder supports bike, run and swim workouts natively. Claude drives the browser, builds each workout in the builder, and places it on her calendar — exactly as the old coach did, comments and all. This covers everything `.zwo` can't, and it's the path I recommend as the primary channel.

**3. The official Partner API (not for us).** It can push planned workouts to athlete calendars — this is how Zwift and Garmin integrate — but access is granted only to approved commercial developers, with a review process. Not available for personal use, so not part of this plan. A community TrainingPeaks MCP server exists and is worth a look for read access, but writes still go through paths 1–2.

Completed workouts need nothing from us: her Garmin already pushes them to TP automatically, which is where our FIT files came from.

## Decision points for Robert

Whether the dashboard should also message the athlete directly (email/WhatsApp digest) or stay a thing you check; whether we schedule the daily evaluation as an automatic task or run it manually at first; and whether to ask her for a fresh FTP/threshold test in week one — I recommend yes, the zones are guesswork without it.

## Sources

- [TrainingPeaks API — Help Center](https://help.trainingpeaks.com/hc/en-us/articles/234441128-TrainingPeaks-API)
- [TrainingPeaks Partner API — GitHub](https://github.com/TrainingPeaks/PartnersAPI)
- [Import Planned Workouts into TrainingPeaks (.zwo) — Help Center](https://help.trainingpeaks.com/hc/en-us/articles/32432105650573-Import-Planned-Workouts-into-TrainingPeaks)
- [Structured Workout Sync and Manual Export — Help Center](https://help.trainingpeaks.com/hc/en-us/articles/115000325647-Structured-Workout-sync-and-Manual-Export)
- [Community TrainingPeaks MCP server](https://lobehub.com/mcp/nagelflorian-trainingpeaks-mcp-server)
