# How to run: python3 get_psn_id.py <directory-containing-json> name_to_psn.json
# Example:    python3 get_psn_id.py ./complete_JSONS_03_01 name_to_psn.json

#extract_id.py
import sys
import json
from pathlib import Path

# PSN platform code in your JSON
PSN_PLATFORM_CODE = 8

def load_json_clean(path: Path) -> dict:
    raw = path.read_bytes()
    # 1) lenient UTF-8 decode
    text = raw.decode('utf-8', errors='replace')
    # 2) drop any replacement chars
    clean = text.replace('\ufffd', '')

    # 3) find the array everyone cares about
    key = '"replayDetailList"'
    idx = clean.find(key)
    if idx == -1:
        raise ValueError(f"No `{key}` found in {path.name!r}")
    arr_start = clean.find('[', idx)
    if arr_start == -1:
        raise ValueError(f"No `[` after `{key}` in {path.name!r}")

    # 4) stream-parse each object
    decoder = json.JSONDecoder()
    pos = arr_start + 1     # skip past the '['
    items = []
    length = len(clean)
    while pos < length:
        try:
            # raw_decode returns (obj, end_pos)
            obj, end = decoder.raw_decode(clean, pos)
            items.append(obj)
            pos = end
            # skip past comma / whitespace before the next object
            while pos < length and clean[pos] in ' \t\r\n,':
                pos += 1
        except json.JSONDecodeError:
            break

    return {"replayDetailList": items}

def main(input_dir: str, output_filename: str):
    # 1) ensure output dir exists
    out_dir = Path("playtime_data")
    out_dir.mkdir(exist_ok=True)

    # 2) validate input directory
    d = Path(input_dir)
    if not d.is_dir():
        print(f"Error: “{input_dir}” is not a directory", file=sys.stderr)
        sys.exit(1)

    # 3) find JSON files
    files = sorted(d.glob("*.json"))
    if not files:
        print(f"Error: no .json files found in {input_dir}", file=sys.stderr)
        sys.exit(1)

    # 4) load and extract
    for file_ in files:
        print(f"🔍 Processing the current file: {file_.name}")

        data = load_json_clean(file_)
        replays = data["replayDetailList"]
        print(f"   ↳ Found {len(replays)} battles in {file_.name}")

        name_to_psnid = {}
        for r in replays:
            if r.get("1pPlatform") == PSN_PLATFORM_CODE:
                name, sid = r.get("1pPlayerName"), r.get("1pOnlineId")
                if name and sid is not None:
                    name_to_psnid[name] = str(sid)
            if r.get("2pPlatform") == PSN_PLATFORM_CODE:
                name, sid = r.get("2pPlayerName"), r.get("2pOnlineId")
                if name and sid is not None:
                    name_to_psnid[name] = str(sid)

        print(f"✅ Extracted {len(name_to_psnid)} PSN players from {file_.name}")
        print(f"Moving onto the next .JSON")

    print(f"✅ Completed .JSON mapping")

    # 5) write into playtime_data/
    out_path = out_dir / output_filename
    out_path.write_text(json.dumps(name_to_psnid, indent=2), encoding="utf-8")
    print(f"📝 Wrote mapping to {out_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_id.py <input_dir> <name_to_psnid.json>", file=sys.stderr)
        sys.exit(1)
    _, input_dir, out_fname = sys.argv
    main(input_dir, out_fname)