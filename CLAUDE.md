# Flavor Bible

Interactive visualization of food pairings based on The Flavor Bible. Users select ingredients to explore a network graph of complementary flavors.

## Build

```bash
python3 build.py
```

Reads `flavor_bible_full.csv` and generates `flavor-bible-deploy.html` (self-contained, no server required).

## Test

```bash
.venv/bin/pytest test_flavor_bible.py -v
```

Requires Playwright: `.venv/bin/python -m playwright install chromium`

## Architecture

- `build.py` - Injects CSV data into template
- `flavor-bible-template.html` - HTML with `{{FLAVOR_DATA}}` placeholder
- `flavor_bible_full.csv` - Source data (main, pairing columns)
- `flavor-bible-deploy.html` - Generated output (not tracked in git)
- `test_flavor_bible.py` - Playwright regression tests
- `requirements.txt` - Test dependencies (playwright, pytest)
