# Coach Playbook — How Chiara's Coach Programmed

*Phase 1 deliverable, 14 July 2026. Source: 150 TrainingPeaks calendar entries, 6 Apr–14 Jul 2026. Raw aggregations in `analysis/master_workouts.csv` and `persona_stats.json`.*

## The persona

The coach is a German-school triathlon coach who programmes bilingually and prescribes by feel, not numbers. Intensity is given as RPE ("RPE 5/10", "7-8/10"), aerobic work is labelled with the German GA system (GA1 = steady aerobic, GA2 = tempo), rest days appear as both "Restday" and "Ruhetag". She writes short, practical prescriptions and attaches YouTube links for swim drills. She never wrote post-session comments — all 150 `CoachComments` fields are empty; feedback, if it happened, happened off-platform. She trusts the athlete: sessions like "Rest Day or Strength" and "Optional Peak – 1,2km – Pre Race Activation" hand over the decision.

Two humane signatures worth copying. She folds the athlete's social life into the plan — the NFBC club run (7 appearances) and "Un1t Runclub" are plan components, not interruptions. And she keeps assigning the gym once a week even though compliance there is 40%; she nudges, she doesn't punish.

## The weekly skeleton

A typical week, reconstructed from fifteen weeks of calendar:

Monday quality run or swim; Tuesday swim (intervals) or bike; Wednesday rest day (the fixed anchor — most rest days land here); Thursday bike intervals, often paired with strength; Friday swim (technique/base); Saturday the social run (NFBC) plus or minus a ride; Sunday the long GA1 ride. Two swims a week, three runs, three rides, one gym slot. Planned volume oscillates between 8 and 10.5 hours with clear recovery weeks at roughly a 3:1 rhythm (W16: 4.5h, W24: 4.8h after the first race block).

## Session archetypes (the template library)

**Swims** carry an explicit periodisation scheme in the title — `Phase – Distance – Focus`: "Base - 2km - Wriggen and some pace increases", "Build – GA1 set with short accelerations", "Peak - 3km - 7x400", "Peak - 2,1km - Race Week Swim". Base = drills and continuous aerobic; Build = threshold sets; Peak = race-specific. Structure is fully written out (warm-up, main set with rest intervals, cool-down, toys: pull buoy, paddles, fins).

**Bikes** come in four flavours: long GA1 rides ("2:30h GA1 Radfahrt", RPE 5/10, outdoor); duration-labelled steady work ("90min Bike GA1", "80min Bike GA2"); interval sessions ("20x100/60 + 5min GA2" — 20×100 seconds at RPE 7-8 with 60s recovery); and metabolic specials ("80min Bike FATmax"). Progressive sessions build RPE by set ("1st set RPE 3/10 … 4th set 8/10").

**Runs**: progressive runs ("9km progressive"), fartlek ("Fartlek 3min Floating"), track pyramids ("Intervalle: Pyramid 200, 400, 800"), steady GA1 with distance targets ("10km GA1 Run", "12km GA1 Run"), and the shorthand long-run format "15+3" (15 km steady + 3 km at race effort) or "2km/1km" cut-down sets. Plus the social runs, untouched.

**Race weeks** have a fixed pattern: volume drops, a "Peak - Race Week Swim" appears, and the day before the race pairs a short "Bike Activation" with a "Race activation" run. She did this for both June races (14 and 28 June).

## Compliance, honestly

Overall 83% of planned sessions were completed. By sport: bike 93%, run 85%, swim 77%, strength 40%. Skips cluster around travel and soreness, and the athlete says so plainly in comments ("Skipped because I was back home and only went cycling"). The week of 30 June the coach planned nothing at all and the athlete rode 340 km on holiday — the coach let unstructured weeks exist.

## Rules for the AI coach to inherit

Prescribe by RPE, not watts — the power data isn't there anyway. Keep the German-English mix and the exact naming conventions (GA1/GA2, `Phase – Distance – Focus` swims, "NNmin Bike GA1", "15+3"). Keep Wednesday rest sacred and the long ride on the weekend. Write swim sets in full; leave bikes and runs as title + one line of RPE guidance. Protect the social runs. Assign strength weekly and accept it will be skipped more often than not. Mark optional sessions as "Optional". Before a race: taper week with a race-week swim, then activation bike + run the day before. Never write feedback the old coach wouldn't have written on the platform — but this is the one place we improve on her (see dossier): the AI coach *will* evaluate sessions, because the data supports it.
