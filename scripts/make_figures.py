#!/usr/bin/env python3
"""Generate the figures used in the book from the CSVs in data/.

Run from the repo root:

    python scripts/make_figures.py

Requires: matplotlib  (pip install matplotlib)

Reads:
    data/ac_penetration_by_region.csv
    data/ac_unit_growth_2024.csv
Writes:
    figures/ac_penetration_by_region.png
    figures/ac_unit_growth_2024.png

These PNGs are committed to the repo so the Quarto book renders with no
runtime dependencies. Re-run this script whenever the underlying CSVs change.
"""
from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

BLUE = "#1b6ca8"
GREEN = "#27ae60"
RED = "#c0392b"


def load(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def penetration_chart() -> None:
    rows = load(DATA / "ac_penetration_by_region.csv")
    rows.sort(key=lambda r: float(r["penetration_pct"]))
    labels = [r["region"] for r in rows]
    vals = [float(r["penetration_pct"]) for r in rows]

    fig, ax = plt.subplots(figsize=(8, 4.2))
    bars = ax.barh(labels, vals, color=BLUE)
    ax.set_xlabel("% of households with air conditioning")
    ax.set_title("Household AC penetration by region (mixed vintage 2018–2024)")
    ax.set_xlim(0, 100)
    for b, v in zip(bars, vals):
        ax.text(v + 1.5, b.get_y() + b.get_height() / 2, f"{v:.0f}%",
                va="center", fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIG / "ac_penetration_by_region.png", dpi=130)
    plt.close(fig)


def unit_growth_chart() -> None:
    rows = load(DATA / "ac_unit_growth_2024.csv")
    rows.sort(key=lambda r: float(r["growth_pct"]))
    labels = [r["region"] for r in rows]
    vals = [float(r["growth_pct"]) for r in rows]
    colors = [RED if v < 0 else GREEN for v in vals]

    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.barh(labels, vals, color=colors)
    ax.set_xlabel("2024 room-AC unit sales growth (%)")
    ax.set_title("2024 room-AC unit growth by region (JARN/IIR)")
    ax.axvline(0, color="#333", lw=0.8)
    for b, v in zip(bars, vals):
        ax.text(v + (0.6 if v >= 0 else -0.6), b.get_y() + b.get_height() / 2,
                f"{v:+.1f}%", va="center",
                ha="left" if v >= 0 else "right", fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIG / "ac_unit_growth_2024.png", dpi=130)
    plt.close(fig)


def growth_pool_chart() -> None:
    rows = load(DATA / "growth_pool_cagr.csv")
    rows.sort(key=lambda r: float(r["cagr_pct"]))
    labels = [r["pool"] for r in rows]
    vals = [float(r["cagr_pct"]) for r in rows]

    fig, ax = plt.subplots(figsize=(8.5, 4))
    bars = ax.barh(labels, vals, color=BLUE)
    ax.set_xlabel("Approximate annual growth (%)")
    ax.set_title("Where the growth is: AC/cooling growth pools\n(illustrative; bases differ — units vs dollars vs cyclical)",
                 fontsize=11)
    for b, v in zip(bars, vals):
        ax.text(v + 0.4, b.get_y() + b.get_height() / 2, f"~{v:.0f}%",
                va="center", fontsize=9)
    ax.set_xlim(0, 26)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIG / "growth_pool_cagr.png", dpi=130)
    plt.close(fig)


def screen_chart() -> None:
    rows = load(DATA / "screen_scores.csv")
    fig, ax = plt.subplots(figsize=(8, 5.2))
    xs = [float(r["ev_ebitda"]) for r in rows]
    ys = [float(r["growth_quality"]) for r in rows]
    # quadrant guides at medians
    xmed = sorted(xs)[len(xs) // 2]
    ymed = sorted(ys)[len(ys) // 2]
    ax.axvspan(0, xmed, ymin=0, ymax=1, color="#eaf4ea", zorder=0)  # cheaper half
    ax.axhline(ymed, color="#bbb", lw=0.8, ls="--")
    ax.axvline(xmed, color="#bbb", lw=0.8, ls="--")
    ax.scatter(xs, ys, s=90, color=BLUE, zorder=3)
    for r in rows:
        ax.annotate(f"{r['company']} ({r['ticker']})",
                    (float(r["ev_ebitda"]), float(r["growth_quality"])),
                    textcoords="offset points", xytext=(8, 5), fontsize=9)
    ax.set_xlabel("EV / EBITDA  (cheaper →  left)")
    ax.set_ylabel("Growth-quality score (0–10, higher = better)")
    ax.set_title("Quality of growth vs. price\n(upper-left = high-quality growth at a lower multiple)",
                 fontsize=11)
    ax.text(0.02, 0.97, "sweet spot", transform=ax.transAxes, fontsize=8,
            color="#2e7d32", va="top")
    ax.set_xlim(0, 55)
    ax.set_ylim(0, 10)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIG / "growth_quality_vs_price.png", dpi=130)
    plt.close(fig)


def sensitivity_chart() -> None:
    rows = load(DATA / "screen_sensitivity.csv")
    companies = [r["company"] for r in rows]
    schemes = [("base", "Base", "#1b6ca8"),
               ("dc_heavy", "Data-center-heavy", "#e8a33d"),
               ("value", "Value/defensive", "#2e7d32")]
    n = len(companies)
    x = list(range(n))
    w = 0.26
    fig, ax = plt.subplots(figsize=(9, 4.6))
    for i, (key, label, color) in enumerate(schemes):
        vals = [float(r[key]) for r in rows]
        ax.bar([xi + (i - 1) * w for xi in x], vals, width=w, label=label, color=color)
    ax.set_xticks(x)
    ax.set_xticklabels(companies)
    ax.set_ylabel("Growth-quality score (0–10, normalized)")
    ax.set_title("Screen sensitivity: growth-quality score under three weightings")
    ax.set_ylim(0, 10)
    ax.legend(fontsize=8, frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIG / "screen_sensitivity.png", dpi=130)
    plt.close(fig)


def main() -> None:
    penetration_chart()
    unit_growth_chart()
    growth_pool_chart()
    screen_chart()
    sensitivity_chart()
    print(f"Wrote figures to {FIG}")


if __name__ == "__main__":
    main()
