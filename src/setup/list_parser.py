# src/setup/list_parser.py

def parse_player_from_list(text: str):
    lines = text.strip().splitlines()
    header = lines[0]
    name = header.split("LIST")[0].strip()
    faction = lines[2].strip() if len(lines) > 2 else "Unknown"

    return {
        "name": name,
        "faction": faction,
        "points": extract_points(header),
        "list_text": text,
    }

def extract_points(header: str):
    import re
    match = re.search(r"\((\d+)\s*points?\)", header)
    return int(match.group(1)) if match else None
