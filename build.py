#!/usr/bin/env python3
"""Build script to generate index.html from template and CSV data."""

import csv
import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
TEMPLATE_FILE = SCRIPT_DIR / "flavor-bible-template.html"
CSV_FILE = SCRIPT_DIR / "flavor_bible_full_w_levels.csv"
OUTPUT_FILE = SCRIPT_DIR / "index.html"


def main():
    # Read CSV and convert to list of dicts
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        data = [
            {
                "main": row["MAIN"].lower(),
                "pairing": row["PAIRING"].lower(),
                "level": int(row["RECOMMENDATION_LEVEL"])
            }
            for row in reader
        ]

    # Convert to JSON
    json_data = json.dumps(data, ensure_ascii=False)

    # Read template and inject data
    template = TEMPLATE_FILE.read_text(encoding="utf-8")
    output = template.replace("{{FLAVOR_DATA}}", json_data)

    # Write output
    OUTPUT_FILE.write_text(output, encoding="utf-8")
    print(f"Generated {OUTPUT_FILE.name} ({len(data)} pairings)")


if __name__ == "__main__":
    main()
