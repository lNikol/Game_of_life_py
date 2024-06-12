import time
from world.Game import Game

def main():
    # w h is_hex
    dane = [7, 7, False, False]
    # form = MainForm()
    # form.update()  # This ensures the form is ready to accept user input
    game = None

    while True:
        if dane[0] != -1:
            game = Game(dane)
            break
        # Delay to avoid high CPU usage
        time.sleep(0.5)


if __name__ == "__main__":
    main()
