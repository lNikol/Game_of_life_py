import time
from world.Game import Game

def main():
    # w h is_hex
    dane = [10, 10, False, False]
    # form = MainForm()
    # form.update()  # This ensures the form is ready to accept user input
    game = None
    if dane[0] != -1:
        game = Game(dane)

    while game.get_world().get_human_is_alive():
        print(f"\n\n\nTurn: {game.get_world().get_turn_count()}")
        game.get_world().take_a_turn()


if __name__ == "__main__":
    main()
