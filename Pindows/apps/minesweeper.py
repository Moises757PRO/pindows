import tkinter as tk
import random

ROWS = 8
COLS = 8
MINES = 10

def content_minesweeper(frame):
    cells = {}
    mine_positions = set()
    game_over = [False]

    def reset_game():
        nonlocal mine_positions, game_over
        for widget in frame.winfo_children():
            widget.destroy()
        cells.clear()
        mine_positions = set()
        game_over[0] = False
        create_grid()

    def create_grid():

        while len(mine_positions) < MINES:
            r = random.randint(0, ROWS - 1)
            c = random.randint(0, COLS - 1)
            mine_positions.add((r, c))

        for r in range(ROWS):
            for c in range(COLS):
                btn = tk.Button(frame, width=2, height=1,
                                command=lambda r=r, c=c: click_cell(r, c))
                btn.bind("<Button-3>", lambda e, r=r, c=c: flag_cell(r, c))
                btn.grid(row=r, column=c)
                cells[(r, c)] = btn

    def click_cell(r, c):
        if game_over[0] or (r, c) not in cells:
            return

        btn = cells[(r, c)]

        if (r, c) in mine_positions:
            btn.config(text="💣", bg="red")
            game_over[0] = True
            reveal_mines()
            return

        count = count_adjacent_mines(r, c)
        btn.config(text=str(count) if count > 0 else "", bg="lightgrey", relief="sunken", state="disabled")

        if count == 0:

            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < ROWS and 0 <= nc < COLS and cells[(nr, nc)]['state'] != "disabled":
                        click_cell(nr, nc)

    def flag_cell(r, c):
        if game_over[0] or (r, c) not in cells:
            return
        btn = cells[(r, c)]
        if btn['text'] == "🚩":
            btn.config(text="")
        elif btn['state'] == "normal":
            btn.config(text="🚩")

    def count_adjacent_mines(r, c):
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if (dr == 0 and dc == 0):
                    continue
                nr, nc = r + dr, c + dc
                if (nr, nc) in mine_positions:
                    count += 1
        return count

    def reveal_mines():
        for r, c in mine_positions:
            btn = cells.get((r, c))
            if btn:
                btn.config(text="💣", bg="black", fg="white")

    tk.Button(frame, text="🔁 Restart", command=reset_game).grid(row=ROWS, column=0, columnspan=COLS, sticky="we")

    create_grid()
