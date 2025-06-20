# src/setup/state.py

import json
from pathlib import Path

GAMES_DIR = Path("games")
GAMES_DIR.mkdir(exist_ok=True)

def get_game_path(game_id):
    return GAMES_DIR / f"{game_id}.json"

def create_game(game_id, players):
    path = get_game_path(game_id)
    if path.exists():
        raise FileExistsError(f"Game '{game_id}' already exists.")

    data = {
        "name": game_id,
        "players": players,
        "phase": "setup",
        "turn": 1,
        "log": []
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_game(game_id):
    path = get_game_path(game_id)
    if not path.exists():
        raise FileNotFoundError(f"Game '{game_id}' not found.")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_game(game_id, data):
    path = get_game_path(game_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
