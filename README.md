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

## Project Structure

```
flavor-bible/
├── build.py                     # Injects CSV data into template
├── flavor-bible-template.html   # HTML with {{FLAVOR_DATA}} placeholder
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
