# src/start_game.py

import sys
from setup.list_parser import parse_player_from_list
from setup.state import create_game

def main():
    if len(sys.argv) != 4:
        print("Usage: python start_game.py <game_id> <player1_list> <player2_list>")
        sys.exit(1)

    game_id = sys.argv[1]
    player1_list = sys.argv[2]
    player2_list = sys.argv[3]

    try:
        players = [
            parse_player_from_list(player1_list),
            parse_player_from_list(player2_list)
        ]
        create_game(game_id, players)
        print(f"✅ Game '{game_id}' created successfully.")
    except FileExistsError:
        print(f"⚠️ Game '{game_id}' already exists.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
