# Flavor Bible

Interactive visualization of food pairings based on The Flavor Bible. Users select ingredients to explore a network graph of complementary flavors.

## Build

```bash
python3 build.py
```

Reads `flavor_bible_full_w_levels.csv` and generates `index.html` (self-contained, no server required).

## Test

```bash
.venv/bin/pytest test_flavor_bible.py -v
```

Requires Playwright: `.venv/bin/python -m playwright install chromium`

## Architecture

- `build.py` - Injects CSV data into template
- `flavor-bible-template.html` - HTML with `{{FLAVOR_DATA}}` placeholder
- `flavor_bible_full_w_levels.csv` - Source data (MAIN, PAIRING, RECOMMENDATION_LEVEL columns)
- `index.html` - Generated output (tracked for GitHub Pages deployment)
- `test_flavor_bible.py` - Playwright regression tests
- `requirements.txt` - Test dependencies (playwright, pytest)

## Recommendation Levels

RECOMMENDATION_LEVEL (1-4) indicates how many chefs recommend the pairing:

| Level | Description | Distribution | Visual |
|-------|-------------|--------------|--------|
| 1 | Basic | 77.6% | Thin gray |
| 2 | Moderate | 17.6% | Medium gray |
| 3 | Strong | 4.5% | Blue |
| 4 | Classic | 0.2% | Thick red |

Users can filter by level in the sidebar. "Best Only" shows levels 3-4.

## Debugging "Missing" Connections

If a pairing appears missing in the visualization:

1. **Check the CSV** - Verify the pairing exists: `grep "^CHICKEN,oregano" flavor_bible_full_w_levels.csv`
2. **Check level filters** - Most pairings are level 1 (77.6%), which are hidden by "Best Only"
3. **Data flow**: CSV (uppercase MAIN) → build.py (lowercases all) → JSON in HTML → `smallerData` (filters to pairings where both ingredients are MAIN entries)
