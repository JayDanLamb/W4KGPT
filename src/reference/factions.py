# .github/scripts/get_factions.py

import requests
import xml.etree.ElementTree as ET
import json
import time
import argparse
from pathlib import Path

REPO = "BSData/wh40k-10e"
BRANCH = "main"
GITHUB_API = f"https://api.github.com/repos/{REPO}/contents"
GITHUB_RAW = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}"
CACHE_PATH = Path("../../.cache/factions.json")
CACHE_DURATION = 86400  # 1 day

# BattleScribe XML namespace
NS = {"bs": "http://www.battlescribe.net/schema/catalogueSchema"}

def list_cat_files():
    response = requests.get(GITHUB_API)
    response.raise_for_status()
    files = response.json()
    return [f["name"] for f in files if f["name"].endswith(".cat")]

def fetch_raw_file(filename):
    url = f"{GITHUB_RAW}/{filename.replace(' ', '%20')}"
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def extract_catalogue_data(xml_content):
    root = ET.fromstring(xml_content)

    catalogue = {
        "id": root.attrib.get("id", "unknown"),
        "name": root.attrib.get("name", "Unnamed Catalogue"),
        "author": root.attrib.get("authorName", "unknown"),
        "gameSystem": {
            "name": root.attrib.get("gameSystemName", "unknown"),
            "revision": root.attrib.get("gameSystemRevision", root.attrib.get("revision", "unknown"))
        },
        "forces": [],
        "publications": [],
        "linked_catalogues": [],
        "entry_links": [],
        "profiles": []
    }

    for force in root.findall(".//bs:force", NS):
        name = force.attrib.get("name")
        if name:
            catalogue["forces"].append(name)

    for pub in root.findall(".//bs:publication", NS):
        name = pub.attrib.get("name")
        if name:
            catalogue["publications"].append(name)

    for link in root.findall(".//bs:catalogueLink", NS):
        name = link.attrib.get("name")
        if name:
            catalogue["linked_catalogues"].append(name)

    for entry in root.findall(".//bs:entryLink", NS):
        name = entry.attrib.get("name")
        if name:
            catalogue["entry_links"].append(name)

    for profile in root.findall(".//bs:profile", NS):
        name = profile.attrib.get("name")
        type_name = profile.attrib.get("typeName", "unknown")
        if name:
            catalogue["profiles"].append({"name": name, "type": type_name})

    return catalogue

def is_cache_valid():
    return CACHE_PATH.exists() and (time.time() - CACHE_PATH.stat().st_mtime < CACHE_DURATION)

def load_from_cache():
    with open(CACHE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_to_cache(data):
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def main(reset_cache=False):
    if not reset_cache and is_cache_valid():
        print("✅ Loaded from cache.")
        data = load_from_cache()
    else:
        cat_files = list_cat_files()
        print(f"🔍 Found {len(cat_files)} .cat files")

        data = []
        for file in cat_files:
            print(f"📄 Parsing: {file}")
            try:
                content = fetch_raw_file(file)
                parsed = extract_catalogue_data(content)
                data.append(parsed)
                print(f"  ✅ {parsed['name']}")
            except Exception as e:
                print(f"  ❌ Error parsing {file}: {e}")

        save_to_cache(data)
        print("💾 Saved parsed data to cache.")

    print(f"\n📦 Total catalogues loaded: {len(data)}")

if __name__ == "__main__":
    reset_cache = False
    main(reset_cache=reset_cache)
