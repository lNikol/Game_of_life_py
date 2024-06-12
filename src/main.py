import time
from world.Game import Game


def main():
    # w h is_hex
    read_log_file = False
    w = 0
    h = 0
    is_hex = False
    game = Game(read_log_file, is_hex)
    while game.get_world().get_human_is_alive():
        print(f"\n\n\nTurn: {game.get_world().get_turn_count()}")
        game.get_world().take_a_turn()
        game.write_to_log()


if __name__ == "__main__":
    main()
