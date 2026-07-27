# Athlete Dossier — Chiara Greselin

*Phase 2 deliverable, 14 July 2026. Per-second analysis of 106 FIT files plus TP calendar. Charts in `analysis/phase2/`. Race: Ironman 70.3, 17 September — nine weeks out.*

## The headline

The June races changed what we know. On 14 June she raced an Olympic-distance triathlon: 1.36 km open water at 2:03/100m, 40 km on the bike at **32.7 km/h**, then 10 km off the bike at **4:37/km**, average HR 175. Two weeks later, a sprint: 4:33/km run off the bike. Her training data understates her badly — solo GA1 rides at 25 km/h say nothing about what she does with a number on her back. She is a racer.

## Strengths, with evidence

**Aerobic durability.** Run decoupling (HR drift on runs over 45 minutes) has a median of 2-3% and improved every month — April 2.9%, July −1.1%. Anything under 5% is good. Long runs barely fade: the median run gets *faster* in its final quarter. The 19.8 km run on 9 July shows an apparent +70% fade, but the splits reveal two stopped kilometres (km 17 at 12.8 and km 18 at 22.1 min/km — a pause, not a collapse) with a return to 5:36/km at km 19.

**Race execution.** Sustained race HR of 167-175 for two and a half hours, clean transitions (3.9 and 2.2 minutes on 14 June), and an off-the-bike 10 km within 20 seconds/km of her fresh 10 km best. Pacing discipline is not something we need to teach.

**The bike engine.** 1,951 km in fourteen weeks, comfortable at 150+ km distances, 32.7 km/h in a 40 km race.

## Weaknesses, with evidence

**The swim, still.** Race pace 2:03/100m open water is the ceiling so far. Pool SWOLF is trending in the right direction but slowly. She skips swims more than anything except gym (77% compliance) — the improvement is happening despite missed volume, which is both encouraging and the clearest lever available.

**Strength work.** 40% compliance, and she's had soreness-related skips. With a nine-week runway, twice-weekly short strength beats once-weekly skipped strength.

**Long-run inventory.** Two runs over 15 km in fourteen weeks. The half marathon on 17 September needs three or four more 18-21 km runs before the taper.

## Zones — the current settings are wrong

Observed max HR is **206** (14 May 2026, clean ramp, not an artifact), against 199 in her device settings. Estimated LTHR: **~175 running, ~169 cycling** (median of top sustained ≥20-min efforts). The FTP field (195 W) remains unusable — power data exists on too few rides. TrainingPeaks' run TSS is broken in her account: run IF values up to 3.3 and single-run TSS of 1,197 mean the threshold pace setting in TP is nonsense, which silently corrupts any TP-computed fitness chart. Our own load model (hrTSS from heart rate) puts her at **CTL ≈ 64, TSB ≈ −11** on 13 July — solidly fit, mildly fatigued, exactly where a build phase should sit. The CSS estimate from interval blocks (1:34/100m) is not credible against her session paces; a proper 400/200 CSS test is week-one business.

## Data hygiene (fix these, the model gets sharper)

No HR strap on nine rides including the two longest — the biggest sessions are invisible to the load model. TP run threshold pace must be corrected. Pool length alternates 25/50 m, handled in analysis but worth standardising.

## The three highest-leverage moves before 17 September

One: swim frequency to a reliable 2×/week with a CSS test in week one — the discipline with the most improvement still available. Two: build the long run — 15, 17, 19, 21 km on successive weekends with race-pace finishes ("15+3" style, as her coach wrote it). Three: wear the HR strap on every ride and fix the TP settings, so the final three weeks of taper decisions run on real numbers.

## Race prediction — superseded

Earlier versions of this dossier predicted 6:15, then 5:50, then 5:23 — all built by extrapolating from training. Her actual result at this same race last year was **5:22:59**, with splits that show the extrapolation was wrong on every leg even when the total happened to match. See **`race_plan_cervia.md`** for the corrected analysis against real splits.

Headline: the bike is already excellent (33.74 km/h over 304 m of climbing on a road bike), the transitions cost 11:51, and the sub-5 goal is reachable at **4:59:50** only if all four legs improve. Honest projection: **5:02–5:12**.
