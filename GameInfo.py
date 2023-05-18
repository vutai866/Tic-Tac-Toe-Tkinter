import tkinter as tk
from datetime import timedelta, datetime
from tkinter import messagebox


class Player(tk.Frame):
    def __init__(self, player_name, master=None):
        super().__init__(master)
        self.master = master
        self.player_name = player_name
        self.score = 0
        self.player_score = None

    def display_player(self, row, col):
        player = tk.Label(text=self.player_name, borderwidth=2, relief="ridge", font="Times 40")
        self.player_score = tk.Label(text="0", borderwidth=2, relief="ridge", font="Times 40")

        player.grid(row=row, column=col, padx=15, pady=5)
        self.player_score.grid(row=row+1, column=col, padx=5, pady=5)

    def update_score(self):
        self.score += 1
        self.player_score.config(text=f"{str(self.score)}")


class Stopwatch(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.elapsed_time = timedelta()
        self.running = False
        self.timer_label = tk.Label(master, text="00:00:00", borderwidth=2, font="Times 40")

    def display_timer(self, row, col):
        self.timer_label.grid(row=row, column=col)

    def start(self):
        if not self.running:
            self.running = True
            self.start_time = datetime.now()
            self.update()

    def stop(self):
        if self.running:
            self.running = False

    def reset(self):
        self.stop()
        self.timer_label.config(text="00:00:00")

    def update(self):
        if self.running:
            elapsed_time = datetime.now() - self.start_time
            elapsed_time_str = str(elapsed_time).split(".")[0]
            self.timer_label.config(text=elapsed_time_str)
            self.master.after(1000, self.update)


class Game(tk.Frame):
    def __init__(self, player1, player2, timer, master=None):
        super().__init__(master)
        self.master = master
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.timer = timer
        self.buttons = []
        self.game_over = False
        self.running = False
        self.counter = 66600

    def create_board(self, row, col):
        for i in range(3):
            row_list = []
            for j in range(3):
                button = tk.Button(self.master, width=11, height=6, command=lambda x=i, y=j: self.on_button_click(x, y))
                button.grid(row=i + row, column=j + col, padx=5, pady=10)
                row_list.append(button)
            self.buttons.append(row_list)

    def start(self):
        # Draw on window
        Player.display_player(self.player1, 0, 0)
        Player.display_player(self.player2, 0, 2)
        Stopwatch.display_timer(self.timer, 0, 1)
        self.create_board(3, 0)

    def on_button_click(self, x, y):
        if self.game_over:
            return

        button = self.buttons[x][y]
        if button["state"] == "disabled":
            return
        button.config(text=self.current_player.player_name, state="disabled")

        # Check for win condition
        if self.check_win(self.current_player):
            messagebox.showinfo("Game Over", f"Player {self.current_player.player_name} wins!")
            print(f"Player {self.current_player.player_name} wins!")
            # Add 1 point to winner
            self.current_player.update_score()
            # Perform win action here
            self.game_over = True
            self.disable_all_buttons()
            # Stops timer
            self.timer.stop()
            self.restart_game()
            return

        # Check for tie condition
        if self.check_tie():
            messagebox.showinfo("Game Over", "It's a tie!")
            print("It's a tie!")
            # Perform tie action here
            self.game_over = True
            self.disable_all_buttons()
            # Stops timer
            self.timer.stop()
            self.restart_game()
            return

        # Switch players
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2
        self.timer.start()
        self.timer.update()

    def check_win(self, player):
        # Check rows
        for row in self.buttons:
            if all(button["text"] == player.player_name for button in row):
                return True

        # Check columns
        for j in range(3):
            if all(self.buttons[i][j]["text"] == player.player_name for i in range(3)):
                return True

        # Check diagonals
        if (self.buttons[0][0]["text"] == self.buttons[1][1]["text"] == self.buttons[2][2]["text"] == player.player_name or
                self.buttons[0][2]["text"] == self.buttons[1][1]["text"] == self.buttons[2][0]["text"] == player.player_name):
            return True

        return False

    def check_tie(self):
        for row in self.buttons:
            for button in row:
                if button["state"] != "disabled":
                    return False
        return True

    def disable_all_buttons(self):
        for row in self.buttons:
            for button in row:
                button.config(state="disabled")

    def restart_game(self):
        for row in self.buttons:
            for button in row:
                button.config(text="", state="normal")
        self.current_player = self.player1
        self.game_over = False
        self.timer.reset()

