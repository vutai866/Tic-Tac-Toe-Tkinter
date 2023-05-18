from GameInfo import *

WINDOW_GEOMETRY = "500x500"


def run():
    # Create window
    window = tk.Tk()
    window.geometry(WINDOW_GEOMETRY)
    window.title("Tic-Tac-Toe Game ")
    window.eval('tk::PlaceWindow . center')

    # Create players
    player1 = Player("Player 1", window)
    player2 = Player("Player 2", window)
    # Create timer
    timer = Stopwatch(window)

    # Start game
    game = Game(player1, player2, timer, master=window)
    game.start()

    # tkinter mainloop
    tk.mainloop()


if __name__ == "__main__":
    run()
