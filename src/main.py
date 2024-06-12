import time
from world.World import World


def main():
    # w h is_hex
    dane = [5, 5, False, False]
    # form = MainForm()
    # form.update()  # This ensures the form is ready to accept user input
    world = None

    while True:
        if dane[0] != -1:
            world = World(dane[0], dane[1], dane[2], dane[3])
            break
        # Delay to avoid high CPU usage
        time.sleep(0.5)


if __name__ == "__main__":
    main()
