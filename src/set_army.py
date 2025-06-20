# src/set_army.py

import sys
from setup.list_parser import parse_player_from_list
from setup.state import load_game, save_game

def main():
    if len(sys.argv) != 4:
        print("Usage: python set_army.py <game_id> <player_name> <army_list_text>")
        sys.exit(1)

    game_id = sys.argv[1]
    player_name = sys.argv[2].strip().lower()
    army_list_text = sys.argv[3]

    player_data = parse_player_from_list(army_list_text)

    try:
        game = load_game(game_id)
    except FileNotFoundError:
        print(f"❌ Game '{game_id}' not found.")
        sys.exit(1)

    matched = False
    for player in game["players"]:
        if player["name"].strip().lower() == player_name:
            player.update(player_data)
            matched = True
            break

    if not matched:
        print(f"❌ No matching player named '{player_name}' in game '{game_id}'.")
        sys.exit(1)

    save_game(game_id, game)
    print(f"✅ Updated army list for '{player_name}' in game '{game_id}'.")

if __name__ == "__main__":
    main()
