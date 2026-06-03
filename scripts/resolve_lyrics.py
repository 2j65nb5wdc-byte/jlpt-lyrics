import argparse
import csv
import json
import os
from pathlib import Path


def norm(text):
    return "".join(str(text or "").lower().split())


def load_records(path):
    suffix = path.suffix.lower()
    if suffix == ".jsonl":
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    yield json.loads(line)
    elif suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            data = data.get("songs", [])
        for item in data:
            yield item
    elif suffix == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            yield from csv.DictReader(f)
    else:
        raise ValueError("lyrics library must be .jsonl, .json, or .csv")


def main():
    parser = argparse.ArgumentParser(description="Resolve lyrics from a local licensed/user-provided lyrics library.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--artist", required=True)
    parser.add_argument("--library", type=Path, default=None)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    library = args.library or os.environ.get("JLPT_LYRICS_LIBRARY")
    if not library:
        raise SystemExit("Set --library or JLPT_LYRICS_LIBRARY to a local .jsonl/.json/.csv lyrics library.")
    library = Path(library)

    wanted_title = norm(args.title)
    wanted_artist = norm(args.artist)
    matches = []
    for record in load_records(library):
        if norm(record.get("song_title") or record.get("title")) == wanted_title and norm(record.get("artist")) == wanted_artist:
            matches.append(record)

    if not matches:
        raise SystemExit("No matching lyrics found in the configured library.")
    if len(matches) > 1:
        licensed = [m for m in matches if norm(m.get("license_status")) in {"licensed", "owned", "user_provided"}]
        matches = licensed or matches

    record = matches[0]
    status = norm(record.get("license_status") or record.get("source"))
    allowed = {"licensed", "owned", "user_provided", "licensed_internal"}
    if status and status not in allowed:
        raise SystemExit(f"Matching lyrics found, but license_status/source is not allowed: {status}")

    output = {
        "song_title": record.get("song_title") or record.get("title") or args.title,
        "song_title_cn": record.get("song_title_cn", ""),
        "artist": record.get("artist") or args.artist,
        "source_note": record.get("source") or record.get("license_note") or "本地歌词库",
        "lyrics_raw": record.get("lyrics", ""),
    }

    if args.out:
        args.out.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
        print(args.out)
    else:
        print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
