# The Air Conditioning Investment Notebook

A personal Quarto book on air-conditioning technology, energy efficiency, market growth, and the public companies positioned to benefit. Audience: just me (Don).

## Build locally

```bash
quarto preview      # live preview while editing
quarto render       # build static site into _book/
```

Requires [Quarto](https://quarto.org) installed locally.

## Structure

| File | Chapter |
|---|---|
| `index.qmd` | Preface / purpose |
| `01-what-is-ac.qmd` | Types of air conditioning |
| `02-efficiency.qmd` | Where efficiency gains come from (inverter, ductless/VRF, heat pumps, SEER2, refrigerants) |
| `regulation-pricing.qmd` | SEER2 rollback risk, ASP uplift, energy-cost backstop, antitrust |
| `03-market-size-growth.qmd` | Market size & growth; recent forecasts; regional data + charts; US vs Europe |
| `data-center-cooling.qmd` | Data-center / liquid cooling deep dive + Vertiv profile |
| `04-players.qmd` | Major public companies |
| `05-financials.qmd` | Populated financial comparison (+ `ac_comp_sheet.xlsx`) |
| `adjacencies.qmd` | Picks & shovels: refrigerant chemicals + components |
| `06-private-conglomerates.qmd` | Private firms and conglomerates |
| `07-watchlist.qmd` | Synthesis, watchlist, open questions |
| `glossary.qmd` | Plain-language glossary of technical terms |
| `references.qmd` | Bibliography (`references.bib`) |

Data and figures live in `data/` (CSVs) and `figures/` (committed PNGs; the market chapter also shows R code to regenerate them).

## Developing in WSL2

This project is intended to live in the WSL2 native filesystem (e.g.
`~/Documents/code_projects/air-conditioning`) for fast R/Python/Quarto/git.
The book has **no executable code chunks** (figures are committed PNGs in
`figures/`, regenerable from `data/*.csv` via the R snippet shown in the
market chapter), so `quarto render` needs only Quarto — no R/Python runtime.

## Publishing to GitHub Pages (when ready)

One-off, local:

```bash
quarto publish gh-pages
```

Or automatically on every push: a ready GitHub Action is included at
`.github/workflows/publish.yml`. Push this repo to GitHub, enable Pages
(Settings → Pages → Build from the `gh-pages` branch), and it deploys on push to `main`.

## Status

First draft — **breadth over precision**. Market-size dollar figures are from secondary aggregators and vary widely; the financial comparison table is an unpopulated scaffold. Re-verify every figure against a primary source before any investment use.
