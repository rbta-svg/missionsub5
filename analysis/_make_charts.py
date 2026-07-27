#!/usr/bin/env python3
"""
Generate training analysis charts from workouts.csv.
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import os

OUT_DIR = "/sessions/magical-relaxed-maxwell/mnt/chiara_coach/analysis"
CSV_PATH = os.path.join(OUT_DIR, "workouts.csv")

SPORT_COLORS = {
    "swim": "#1f77b4",
    "bike": "#ff7f0e",
    "run": "#2ca02c",
    "other": "#808080",
}

plt.rcParams.update({
    "figure.dpi": 150,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": False,
    "font.size": 10,
})

# ---------------------------------------------------------------
# Load & normalize
# ---------------------------------------------------------------
df = pd.read_csv(CSV_PATH)
df["start_time_utc"] = pd.to_datetime(df["start_time_utc"], utc=True)
df["date"] = df["start_time_utc"].dt.tz_localize(None)

def map_sport(s):
    if s == "swimming":
        return "swim"
    if s == "cycling":
        return "bike"
    if s == "running":
        return "run"
    return "other"

df["sport_group"] = df["sport"].apply(map_sport)
df["hours"] = df["total_timer_time_s"] / 3600.0
df["km"] = df["total_distance_m"] / 1000.0

iso = df["date"].dt.isocalendar()
df["iso_year"] = iso["year"]
df["iso_week"] = iso["week"]

print("Row count:", len(df))
print("Sport group counts:\n", df["sport_group"].value_counts())

def pace_formatter():
    def fmt(x, pos=None):
        if x is None or np.isnan(x) or x < 0:
            return ""
        m = int(x)
        s = int(round((x - m) * 60))
        if s == 60:
            m += 1
            s = 0
        return f"{m}:{s:02d}"
    return mticker.FuncFormatter(fmt)

# =================================================================
# CHART 1: weekly_volume.png
# =================================================================
weeks = list(range(15, 30))
week_mask = (df["iso_year"] == 2026) & (df["iso_week"].isin(weeks))
wdf = df[week_mask].copy()

def iso_week_start(year, week):
    return pd.Timestamp.fromisocalendar(year, int(week), 1)

week_starts = {w: iso_week_start(2026, w) for w in weeks}

pivot = (
    wdf.groupby(["iso_week", "sport_group"])["hours"]
    .sum()
    .unstack(fill_value=0.0)
)
pivot = pivot.reindex(weeks, fill_value=0.0)
for sp in ["swim", "bike", "run", "other"]:
    if sp not in pivot.columns:
        pivot[sp] = 0.0
pivot = pivot[["swim", "bike", "run", "other"]]

x_labels = [week_starts[w].strftime("%-d %b") for w in weeks]
x = np.arange(len(weeks))

fig, ax = plt.subplots(figsize=(10, 6))
bottom = np.zeros(len(weeks))
for sp in ["swim", "bike", "run", "other"]:
    vals = pivot[sp].values
    ax.bar(x, vals, bottom=bottom, label=sp, color=SPORT_COLORS[sp], width=0.65)
    bottom += vals

totals = pivot.sum(axis=1).values
for xi, tot in zip(x, totals):
    if tot > 0.01:
        ax.annotate(f"{tot:.1f}", (xi, tot), textcoords="offset points",
                    xytext=(0, 3), ha="center", fontsize=8.5, fontweight="bold")

ax.set_xticks(x)
ax.set_xticklabels(x_labels, rotation=45, ha="right")
ax.set_ylabel("Hours")
ax.set_xlabel("Week starting")
ax.set_title("Weekly Training Volume by Sport (W15–W29 2026)")
ax.legend(title="Sport", frameon=False, loc="upper left")
fig.tight_layout()
fig.savefig(os.path.join(OUT_DIR, "weekly_volume.png"), dpi=150)
plt.close(fig)
print("Saved weekly_volume.png")

# =================================================================
# CHART 2: discipline_trends.png
# =================================================================
fig, axes = plt.subplots(3, 1, figsize=(10, 6.5), sharex=True)

def rolling_trend(x_dates, y_vals, window_days=14):
    y_arr = np.asarray(y_vals, dtype=float)
    s = pd.Series(y_arr, index=pd.DatetimeIndex(x_dates)).sort_index()
    roll = s.rolling(f"{window_days}D", min_periods=2).mean()
    return roll.index, roll.values

# (a) Swim pace per 100m for swims > 1000m
ax = axes[0]
sw = df[(df["sport_group"] == "swim") & (df["total_distance_m"] > 1000)].copy()
sw = sw.dropna(subset=["avg_swim_pace_min_per_100m"]).sort_values("date")
is_ow = sw["sub_sport"] == "open_water"

ax.scatter(sw.loc[~is_ow, "date"], sw.loc[~is_ow, "avg_swim_pace_min_per_100m"],
           color=SPORT_COLORS["swim"], s=28, alpha=0.8, label="Pool swim", zorder=3)
ax.scatter(sw.loc[is_ow, "date"], sw.loc[is_ow, "avg_swim_pace_min_per_100m"],
           color=SPORT_COLORS["swim"], s=180, marker="*", edgecolor="black",
           linewidth=0.6, label="Open water", zorder=4)

tx, ty = rolling_trend(sw["date"], sw["avg_swim_pace_min_per_100m"])
ax.plot(tx, ty, color="black", linewidth=1.5, alpha=0.7, label="Trend (14d rolling)")

ax.invert_yaxis()
ax.yaxis.set_major_formatter(pace_formatter())
ax.set_ylabel("Swim pace\n(min:sec / 100m)")
ax.set_title("Swim Pace Trend (swims > 1000m)")
ax.legend(frameon=False, loc="upper right", fontsize=8)

# (b) Bike avg speed km/h for outdoor rides > 30km
ax = axes[1]
bk = df[(df["sport_group"] == "bike") & (df["total_distance_m"] > 30000)].copy()
bk = bk.dropna(subset=["avg_speed_mps"]).sort_values("date")
bk["speed_kmh"] = bk["avg_speed_mps"] * 3.6

ax.scatter(bk["date"], bk["speed_kmh"], color=SPORT_COLORS["bike"], s=28, alpha=0.8, zorder=3)
tx, ty = rolling_trend(bk["date"], bk["speed_kmh"])
ax.plot(tx, ty, color="black", linewidth=1.5, alpha=0.7, label="Trend (14d rolling)")
ax.set_ylabel("Bike speed\n(km/h)")
ax.set_title("Bike Avg Speed Trend (outdoor rides > 30km)")
ax.legend(frameon=False, loc="upper right", fontsize=8)

# (c) Run pace min/km for runs > 5km
ax = axes[2]
rn = df[(df["sport_group"] == "run") & (df["total_distance_m"] > 5000)].copy()
rn = rn.dropna(subset=["avg_run_pace_min_per_km"]).sort_values("date")

ax.scatter(rn["date"], rn["avg_run_pace_min_per_km"], color=SPORT_COLORS["run"], s=28, alpha=0.8, zorder=3)
tx, ty = rolling_trend(rn["date"], rn["avg_run_pace_min_per_km"])
ax.plot(tx, ty, color="black", linewidth=1.5, alpha=0.7, label="Trend (14d rolling)")
ax.invert_yaxis()
ax.yaxis.set_major_formatter(pace_formatter())
ax.set_ylabel("Run pace\n(min:sec / km)")
ax.set_xlabel("Date")
ax.set_title("Run Pace Trend (runs > 5km)")
ax.legend(frameon=False, loc="upper right", fontsize=8)

ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=mdates.MO, interval=2))
fig.autofmt_xdate(rotation=45, ha="right")

fig.suptitle("Discipline Pace/Speed Trends (Apr–Jul 2026)", fontsize=13, y=0.995)
fig.tight_layout(rect=[0, 0, 1, 0.97])
fig.savefig(os.path.join(OUT_DIR, "discipline_trends.png"), dpi=150)
plt.close(fig)
print("Saved discipline_trends.png")

# =================================================================
# CHART 3: weekly_km_by_sport.png
# =================================================================
pivot_km = (
    wdf.groupby(["iso_week", "sport_group"])["km"]
    .sum()
    .unstack(fill_value=0.0)
    .reindex(weeks, fill_value=0.0)
)
for sp in ["swim", "bike", "run"]:
    if sp not in pivot_km.columns:
        pivot_km[sp] = 0.0

fig, axes = plt.subplots(1, 3, figsize=(10, 6), sharex=False)
sport_titles = {"swim": "Swim (km/week)", "bike": "Bike (km/week)", "run": "Run (km/week)"}

for ax, sp in zip(axes, ["swim", "bike", "run"]):
    vals = pivot_km[sp].values
    ax.bar(x, vals, color=SPORT_COLORS[sp], width=0.65)
    ax.set_xticks(x[::2])
    ax.set_xticklabels([x_labels[i] for i in range(0, len(x), 2)], rotation=60, ha="right", fontsize=7.5)
    ax.set_title(sport_titles[sp], fontsize=10)
    ax.set_ylabel("Kilometres")

fig.suptitle("Weekly Distance by Sport (W15–W29 2026)", fontsize=13)
fig.tight_layout(rect=[0, 0, 1, 0.95])
fig.savefig(os.path.join(OUT_DIR, "weekly_km_by_sport.png"), dpi=150)
plt.close(fig)
print("Saved weekly_km_by_sport.png")

# =================================================================
# CHART 4: session_mix.png
# =================================================================
counts = df["sport_group"].value_counts().reindex(["swim", "bike", "run", "other"], fill_value=0)
hours_by_sport = df.groupby("sport_group")["hours"].sum().reindex(["swim", "bike", "run", "other"], fill_value=0.0)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6))

bars = ax1.bar(counts.index, counts.values, color=[SPORT_COLORS[s] for s in counts.index], width=0.6)
for b, v in zip(bars, counts.values):
    ax1.annotate(str(int(v)), (b.get_x() + b.get_width() / 2, v), textcoords="offset points",
                 xytext=(0, 3), ha="center", fontsize=9, fontweight="bold")
ax1.set_ylabel("Number of sessions")
ax1.set_title("Session Count by Sport")

nonzero = hours_by_sport[hours_by_sport > 0]
colors = [SPORT_COLORS[s] for s in nonzero.index]
wedges, texts, autotexts = ax2.pie(
    nonzero.values,
    labels=nonzero.index,
    autopct=lambda p: f"{p:.0f}%\n({p/100*hours_by_sport.sum():.1f}h)",
    colors=colors,
    startangle=90,
    wedgeprops={"edgecolor": "white", "linewidth": 1.5},
    textprops={"fontsize": 9},
)
ax2.set_title("Total Training Hours Share by Sport")

fig.suptitle("Session Mix Overview", fontsize=13)
fig.tight_layout(rect=[0, 0, 1, 0.95])
fig.savefig(os.path.join(OUT_DIR, "session_mix.png"), dpi=150)
plt.close(fig)
print("Saved session_mix.png")

print("\nAll charts generated.")
