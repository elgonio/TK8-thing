# How to run: python3 get_steam_hours.py <json_from_extractid.py>.json <final_json_with_ID_and_hours_mapped>.json
# Example:    python3 get_steam_hours.py name_to_steamid.json id_to_hours.json

import os
import sys
import json
import time
import argparse
import requests
from requests.exceptions import ReadTimeout, RequestException
from pathlib import Path

# ─── Load .env if present ──────────────────────────────────────────
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ─── Configuration ────────────────────────────────────────────────
API_URL       = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
DEFAULT_APPID = 1778820   # Tekken 8
MAX_RETRIES   = 3         # timeout retry count
RETRY_BACKOFF = 2         # base seconds for exponential backoff
TIMEOUT       = 10        # seconds per HTTP request
# ──────────────────────────────────────────────────────────────────

def get_playtime_for_app(steam_key, steam_id, appid):
    params = {
        "key": steam_key,
        "steamid": steam_id,
        "include_appinfo": 0,
        "include_played_free_games": 1,
        "appids_filter[0]": appid,
    }
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = requests.get(API_URL, params=params, timeout=TIMEOUT)
            r.raise_for_status()
            data = r.json().get("response", {})
            if data.get("game_count", 0) > 0 and data.get("games"):
                mins = data["games"][0]["playtime_forever"]
                return "success", round((mins / 60.0), 1)
            return "private", None

        except ReadTimeout:
            if attempt < MAX_RETRIES:
                wait = RETRY_BACKOFF ** attempt
                print(f"⚠️  {steam_id}: timeout, retrying in {wait}s (#{attempt})…")
                time.sleep(wait)
            else:
                return "timeout", None

        except RequestException as e:
            code = getattr(e.response, "status_code", None)
            return f"http_error_{code or 'unknown'}", str(e)

    return "timeout", None

def main():
    parser = argparse.ArgumentParser(
        description="Fetch Tekken 8 hours via Steam Web API (with retries)."
    )
    parser.add_argument("infile",  help="name_to_steamid.json in playtime_data/")
    parser.add_argument("outfile", help="id_to_hours.json (will go into playtime_data/)")
    parser.add_argument("--appid", type=int, default=DEFAULT_APPID,
                        help=f"Steam AppID (default {DEFAULT_APPID})")
    args = parser.parse_args()

    steam_key = os.getenv("STEAM_API_KEY")
    if not steam_key:
        print("Error: STEAM_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    # 1) ensure playtime_data/ exists and load infile from there
    data_dir = Path("playtime_data")
    data_dir.mkdir(exist_ok=True)
    in_path  = data_dir / args.infile
    if not in_path.is_file():
        print(f"Error: {in_path} not found", file=sys.stderr)
        sys.exit(1)

    name_to_id = json.loads(in_path.read_text(encoding="utf-8"))
    steam_ids  = list({str(v) for v in name_to_id.values()})
    print(f"🔍 Loaded {len(steam_ids)} SteamIDs from {in_path.name}")
    print(f"→ Querying AppID {args.appid}\n")

    # 2) fetch sequentially with retries
    id_to_hours = {}
    for sid in steam_ids:
        status, result = get_playtime_for_app(steam_key, sid, args.appid)
        if status == "success":
            print(f"✅ {sid}: {result:.2f} hours")
            id_to_hours[sid] = {"status": status, "hours": result}
        elif status == "private":
            print(f"⛔ {sid}: private")
            id_to_hours[sid] = {"status": status, "hours": 0}
        elif status == "timeout":
            print(f"❌ {sid}: timed out after {MAX_RETRIES} retries")
            id_to_hours[sid] = {"status": status, "hours": 0}
        else:  # http_error_xxx
            print(f"❌ {sid}: {status} ({result})")
            id_to_hours[sid] = {"status": status, "message": result}

    # 3) write results into playtime_data/
    out_path = data_dir / args.outfile
    out_path.write_text(json.dumps(id_to_hours, indent=2), encoding="utf-8")
    print(f"\n📝 Wrote {len(id_to_hours)} entries to {out_path}")

if __name__ == "__main__":
    main()


# DecAPI Implementation: A little obsolete since I am using the official Steam Web API now
# # extract_hours.py

# import json
# import sys
# import time
# import os
# import requests

# # ─── Configuration ────────────────────────────────────────────────
# APP_LIST_URL = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
# DECAPI_URL   = "https://decapi.me/steam/hours"
# GAME_NAME    = "Tekken 8"    # exact Steam title
# DELAY        = 3             # seconds between each DecAPI call
# # ──────────────────────────────────────────────────────────────────

# def get_appid(game_name: str) -> int:
#     """Fetch Steam's full app list once and find the exact appid."""
#     print(f"🔍 Fetching app list to find AppID for '{game_name}'…")
#     resp = requests.get(APP_LIST_URL, timeout=10)
#     resp.raise_for_status()
#     apps = resp.json()["applist"]["apps"]
#     target = game_name.lower()
#     for a in apps:
#         if a["name"].lower() == target:
#             print(f"→ Found AppID: {a['appid']}\n")
#             return a["appid"]
#     raise RuntimeError(f"Could not find Steam app named '{game_name}'")

# def fetch_playtime(steam_id: str, appid: int) -> str:
#     """Query DecAPI for hours played for a public SteamID."""
#     params = {"id": steam_id, "appid": appid}
#     resp = requests.get(DECAPI_URL, params=params, timeout=10)
#     resp.raise_for_status()
#     return resp.text.strip()

# def main(input_file: str, output_file: str):
#     # 1) validate input
#     if not os.path.isfile(input_file):
#         print(f"Error: '{input_file}' is not a file", file=sys.stderr)
#         sys.exit(1)

#     # 2) load name→SteamID mapping
#     with open(input_file, "r", encoding="utf-8") as f:
#         name_to_id = json.load(f)
#     steam_ids = list({str(v) for v in name_to_id.values()})
#     print(f"🔍 Loaded {len(steam_ids)} unique Steam IDs from '{input_file}'\n")

#     # 3) resolve Tekken 8 AppID
#     appid = get_appid(GAME_NAME)

#     # 4) fetch each playtime, one by one, with delay
#     id_to_hours = {}
#     for sid in steam_ids:
#         try:
#             result = fetch_playtime(sid, appid)
#             if result.lower().startswith("error"):
#                 print(f"❌ {sid}: PRIVATE or NO DATA → {result}")
#                 id_to_hours[sid] = {"status": "private_or_no_data", "message": result}
#             else:
#                 print(f"✅ {sid}: PLAYTIME → {result}")
#                 id_to_hours[sid] = {"status": "success", "playtime": result}
#         except requests.HTTPError as e:
#             code = e.response.status_code
#             print(f"❌ {sid}: HTTP {code} error")
#             id_to_hours[sid] = {"status": f"http_{code}_error", "message": str(e)}
#         except Exception as e:
#             print(f"❌ {sid}: Unexpected error → {e}")
#             id_to_hours[sid] = {"status": "error", "message": str(e)}

#         print(f"⏱ Waiting {DELAY}s before next call…\n")
#         time.sleep(DELAY)

#     # 5) write out the results
#     with open(output_file, "w", encoding="utf-8") as f:
#         json.dump(id_to_hours, f, indent=2)
#     print(f"\n📝 Wrote {len(id_to_hours)} entries to '{output_file}'")

# if __name__ == "__main__":
#     if len(sys.argv) != 3:
#         print("Usage: python extract_hours.py <name_to_steamid.json> <id_to_hours.json>", file=sys.stderr)
#         sys.exit(1)
#     _, inp, outp = sys.argv
#     main(inp, outp)