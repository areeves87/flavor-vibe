# Flavor Bible

An interactive visualization of food pairings based on The Flavor Bible. Select ingredients to explore a network graph of complementary flavors.

## Usage

### Build

```bash
python3 build.py
```

This reads `flavor_bible_full.csv` and generates `flavor-bible-deploy.html` — a self-contained HTML file with all data embedded.

### Deploy

Open `flavor-bible-deploy.html` in a browser, or host it anywhere as a static file. No server required.

### Test

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m playwright install chromium
.venv/bin/pytest test_flavor_bible.py -v
```

Tests verify that the graph renders the correct number of nodes and edges for various ingredient selections.

## Project Structure

```
flavor-bible/
├── build.py                     # Injects CSV data into template
├── flavor-bible-template.html   # HTML with {{FLAVOR_DATA}} placeholder
├── test_flavor_bible.py         # Playwright regression tests
├── requirements.txt             # Test dependencies
├── flavor_bible_full.csv        # Source data (not tracked)
└── flavor-bible-deploy.html     # Generated output (not tracked)
```

## Data

The CSV file should have `main` and `pairing` columns:

```csv
main,pairing
chicken,lemon
chicken,garlic
...
```
