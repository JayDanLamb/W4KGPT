# src/set_army.py

import sys
from setup.list_parser import parse_player_from_list
from setup.state import load_game, save_game

def main():
    if len(sys.argv) != 3:
        print("Usage: python set_army.py <game_id> <army_list_text>")
        sys.exit(1)

    game_id = sys.argv[1]
    army_list_text = sys.argv[2]

    player_data = parse_player_from_list(army_list_text)

    try:
        game = load_game(game_id)
    except FileNotFoundError:
        print(f"❌ Game '{game_id}' not found.")
        sys.exit(1)

    matched = False
    for player in game["players"]:
        if player["name"].lower() == player_data["name"].lower():
            player.update(player_data)
            matched = True
            break

    if not matched:
        print(f"❌ No matching player named '{player_data['name']}' in game '{game_id}'.")
        sys.exit(1)

    save_game(game_id, game)
    print(f"✅ Updated army list for '{player_data['name']}' in game '{game_id}'.")

if __name__ == "__main__":
    main()
