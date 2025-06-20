# src/start_game.py

import sys
from setup.state import create_game

def generate_game_id(names):
    return "-vs-".join(n.lower() for n in names)

def main():
    if len(sys.argv) != 2:
        print("Usage: python start_game.py <comma-separated player names>")
        sys.exit(1)

    raw_names = sys.argv[1]
    names = [name.strip() for name in raw_names.split(",") if name.strip()]

    if len(names) < 2:
        print("❌ At least two players are required.")
        sys.exit(1)

    game_id = generate_game_id(names)
    players = [{"name": name, "faction": None, "points": None, "list_text": None} for name in names]

    try:
        create_game(game_id, players)
        print(f"✅ Game '{game_id}' created successfully with players: {', '.join(names)}")
    except FileExistsError:
        print(f"⚠️ Game '{game_id}' already exists.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
