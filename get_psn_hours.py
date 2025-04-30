#!/usr/bin/env python3
import sys
import json
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

# The specific game to extract from Exophase
DEFAULT_GAME = "TEKKEN 8"
# Directory to store input/output data
DATA_DIR = Path("playtime_data")


def fetch_playtime_for_game(psn_id: str, game: str) -> float:
    """
    Fetch playtime for a single PSN ID and game from Exophase.
    Returns hours as float, or 0.0 on any error or missing data.
    """
    url = f"https://www.exophase.com/psn/user/{psn_id}/"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            )
        )
        try:
            resp = page.goto(url, timeout=30_000)
        except Exception:
            browser.close()
            return 0.0

        if not resp or resp.status != 200:
            browser.close()
            return 0.0

        try:
            page.wait_for_selector("i.exo-icon-playtime-white", timeout=10_000)
        except Exception:
            browser.close()
            return 0.0

        html = page.content()
        browser.close()

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    for icon in soup.select("i.exo-icon-playtime-white"):
        raw = icon.next_sibling.strip() if icon.next_sibling else ""
        m = re.match(r"(\d+)h\s*(\d+)m", raw)
        hours = (int(m.group(1)) + int(m.group(2))/60) if m else 0.0

        container = icon.find_parent("div", class_="col-game")
        if not container:
            continue
        title_el = container.find("h3")
        if not title_el:
            continue
        if title_el.get_text(strip=True) == game:
            return round(hours, 2)

    return 0.0


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Batch-fetch PSN playtime for a specific game (Exophase)"
    )
    parser.add_argument(
        "infile",
        help="Filename (in playtime_data/) of JSON mapping in-game names to PSN IDs"
    )
    parser.add_argument(
        "outfile",
        help="Filename (in playtime_data/) for output PSN ID→hours JSON"
    )
    parser.add_argument(
        "--game",
        default=DEFAULT_GAME,
        help=f"Game to extract playtime for (default: {DEFAULT_GAME})"
    )
    args = parser.parse_args()

    # Ensure data directory exists
    DATA_DIR.mkdir(exist_ok=True)

    # Build paths for input and output inside playtime_data/
    in_path = DATA_DIR / args.infile
    out_path = DATA_DIR / args.outfile

    if not in_path.is_file():
        print(f"Error: '{in_path}' not found", file=sys.stderr)
        sys.exit(1)

    try:
        name_to_psnid = json.loads(in_path.read_text(encoding='utf-8'))
    except Exception as e:
        print(f"Error reading '{in_path}': {e}", file=sys.stderr)
        sys.exit(1)

    # Unique PSN IDs
    psn_ids = list({str(v) for v in name_to_psnid.values()})
    print(f"🔍 Loaded {len(psn_ids)} PSN IDs from {in_path.name}")
    print(f"→ Querying playtime for '{args.game}'\n")

    results = {}
    for psn_id in psn_ids:
        hours = fetch_playtime_for_game(psn_id, args.game)
        print(f"{psn_id}: {hours}h")
        results[psn_id] = hours

    try:
        out_path.write_text(json.dumps(results, indent=2), encoding='utf-8')
    except Exception as e:
        print(f"Error writing '{out_path}': {e}", file=sys.stderr)
        sys.exit(1)

    print(f"\n📝 Wrote {len(results)} entries to '{out_path}'")

if __name__ == "__main__":
    main()
