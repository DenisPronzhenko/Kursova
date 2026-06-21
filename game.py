import tkinter as tk
import os

CELL = 34
LEVEL_FILE = os.path.join(os.path.dirname(__file__), "level.txt")

WALL = "#"
PRIZE = "*"
MIRROR1 = "/"
MIRROR2 = "\\"
FINISH = "F"

BG = "#101820"
PANEL = "#17212b"
GRID = "#263544"
WALL_COLOR = "#394b59"
BALL = "#ff4d5a"
BALL_OUTLINE = "#ffb3ba"
PRIZE_COLOR = "#ffd166"
MIRROR_COLOR = "#4cc9f0"
FINISH_COLOR = "#57cc99"
TEXT = "#f5f7fa"
MUTED = "#9fb3c8"

delay = 160
running = False
paused = False
game_started = False


def load_level():
    with open(LEVEL_FILE, "r", encoding="utf-8") as f:
        level_data = [list(line.rstrip("\n")) for line in f]

    width = max(len(row) for row in level_data)

    for row in level_data:
        while len(row) < width:
            row.append(" ")

    return level_data


def count_prizes(level_data):
    return sum(row.count(PRIZE) for row in level_data)


def find_finish(level_data):
    for i in range(len(level_data)):
        for j in range(len(level_data[i])):
            if level_data[i][j] == FINISH:
                return i, j

    return len(level_data) - 2, len(level_data[0]) - 2


def reflect(mirror, dr, dc):
    if mirror == "/":
        return -dc, -dr
    if mirror == "\\":
        return dc, dr
    return dr, dc


def reset_game():
    global level, rows, cols, prizes_left, total_prizes
    global ball_row, ball_col, finish_row, finish_col
    global dr, dc, steps, running, paused, game_started
    global canvas_width, canvas_height

    level = load_level()
    rows = len(level)
    cols = len(level[0])

    total_prizes = count_prizes(level)
    prizes_left = total_prizes

    ball_row = 1
    ball_col = 1

    finish_row, finish_col = find_finish(level)

    dr = 0
    dc = 1

    steps = 0
    running = False
    paused = False
    game_started = False

    canvas_width = cols * CELL + 36
    canvas_height = rows * CELL + 36

    canvas.config(width=canvas_width, height=canvas_height)


def draw_game():
    canvas.delete("all")
    canvas.create_rectangle(0, 0, canvas_width, canvas_height, fill=BG, outline="")

    for i in range(rows):
        for j in range(cols):
            x1 = j * CELL + 18
            y1 = i * CELL + 18
            x2 = x1 + CELL
            y2 = y1 + CELL

            cell = level[i][j]

            canvas.create_rectangle(x1, y1, x2, y2, fill=PANEL, outline=GRID)

            if cell == WALL:
                canvas.create_rectangle(x1, y1, x2, y2, fill=WALL_COLOR, outline=WALL_COLOR)

            elif cell == PRIZE:
                canvas.create_oval(
                    x1 + 9, y1 + 9,
                    x2 - 9, y2 - 9,
                    fill=PRIZE_COLOR,
                    outline="#fff3b0",
                    width=2
                )

            elif cell == "/":
                canvas.create_line(
                    x2 - 7, y1 + 7,
                    x1 + 7, y2 - 7,
                    fill=MIRROR_COLOR,
                    width=5,
                    capstyle=tk.ROUND
                )

            elif cell == "\\":
                canvas.create_line(
                    x1 + 7, y1 + 7,
                    x2 - 7, y2 - 7,
                    fill=MIRROR_COLOR,
                    width=5,
                    capstyle=tk.ROUND
                )

            elif cell == FINISH:
                canvas.create_rectangle(
                    x1 + 6, y1 + 6,
                    x2 - 6, y2 - 6,
                    fill=FINISH_COLOR,
                    outline="#b7f7d4",
                    width=2
                )
                canvas.create_text(
                    x1 + CELL // 2,
                    y1 + CELL // 2,
                    text="F",
                    fill="#0b3d2e",
                    font=("Segoe UI", 13, "bold")
                )

    bx = ball_col * CELL + CELL // 2 + 18
    by = ball_row * CELL + CELL // 2 + 18

    canvas.create_oval(
        bx - 13, by - 13,
        bx + 13, by + 13,
        fill=BALL,
        outline=BALL_OUTLINE,
        width=3
    )

    update_status()


def update_status():
    status_label.config(
        text=f"Призи: {total_prizes - prizes_left}/{total_prizes}    "
             f"Залишилось: {prizes_left}    "
             f"Кроки: {steps}"
    )


def show_start_screen():
    canvas.delete("all")

    canvas.create_rectangle(
        0, 0,
        canvas_width,
        canvas_height,
        fill="#27c3e8",
        outline=""
    )

    for x, y in [(40, 85), (120, 55), (canvas_width - 90, 80), (canvas_width - 180, 120)]:
        canvas.create_oval(x - 35, y - 18, x + 35, y + 18, fill="#bff4ff", outline="")
        canvas.create_oval(x - 10, y - 32, x + 55, y + 20, fill="#bff4ff", outline="")
        canvas.create_oval(x - 60, y - 10, x + 5, y + 28, fill="#bff4ff", outline="")

    canvas.create_polygon(
        0, canvas_height - 210,
        120, canvas_height - 340,
        240, canvas_height - 210,
        fill="#1698ad",
        outline=""
    )
    canvas.create_polygon(
        160, canvas_height - 210,
        330, canvas_height - 360,
        520, canvas_height - 210,
        fill="#118ca3",
        outline=""
    )
    canvas.create_polygon(
        390, canvas_height - 210,
        canvas_width - 80, canvas_height - 355,
        canvas_width, canvas_height - 210,
        fill="#1698ad",
        outline=""
    )

    canvas.create_rectangle(
        0,
        canvas_height - 145,
        canvas_width,
        canvas_height,
        fill="#38b24a",
        outline=""
    )

    canvas.create_rectangle(
        0,
        canvas_height - 120,
        160,
        canvas_height,
        fill="#8b4a25",
        outline=""
    )
    canvas.create_polygon(
        0, canvas_height - 120,
        160, canvas_height - 120,
        145, canvas_height - 96,
        15, canvas_height - 96,
        fill="#2fb344",
        outline=""
    )

    canvas.create_rectangle(
        canvas_width - 140,
        canvas_height - 120,
        canvas_width,
        canvas_height,
        fill="#8b4a25",
        outline=""
    )
    canvas.create_polygon(
        canvas_width - 140, canvas_height - 120,
        canvas_width, canvas_height - 120,
        canvas_width, canvas_height - 96,
        canvas_width - 125, canvas_height - 96,
        fill="#2fb344",
        outline=""
    )

    bridge_y = canvas_height - 110
    for i in range(9):
        x = 150 + i * 42
        canvas.create_polygon(
            x, bridge_y + i * 5,
            x + 48, bridge_y + 8 + i * 5,
            x + 40, bridge_y + 34 + i * 5,
            x - 8, bridge_y + 26 + i * 5,
            fill="#c98643",
            outline="#7a4a26",
            width=2
        )

    canvas.create_text(
        canvas_width // 2 + 3,
        75,
        text="RED BALL",
        font=("Arial", 34, "bold"),
        fill="#a43222"
    )
    canvas.create_text(
        canvas_width // 2,
        70,
        text="RED BALL",
        font=("Arial", 34, "bold"),
        fill="#ff5a3d"
    )

    canvas.create_text(
        canvas_width // 2,
        112,
        text="FOREVER",
        font=("Arial", 21, "bold"),
        fill="white"
    )

    ball_x = canvas_width // 2 - 105
    ball_y = canvas_height // 2 + 5

    canvas.create_oval(
        ball_x - 35,
        ball_y - 35,
        ball_x + 35,
        ball_y + 35,
        fill="#f23b3b",
        outline="#9c1f1f",
        width=3
    )
    canvas.create_oval(ball_x - 15, ball_y - 15, ball_x - 5, ball_y - 5, fill="white", outline="")
    canvas.create_oval(ball_x + 8, ball_y - 15, ball_x + 18, ball_y - 5, fill="white", outline="")
    canvas.create_oval(ball_x - 11, ball_y - 11, ball_x - 6, ball_y - 6, fill="black", outline="")
    canvas.create_oval(ball_x + 12, ball_y - 11, ball_x + 17, ball_y - 6, fill="black", outline="")
    canvas.create_arc(
        ball_x - 18,
        ball_y - 5,
        ball_x + 20,
        ball_y + 25,
        start=200,
        extent=140,
        style=tk.ARC,
        outline="white",
        width=3
    )

    def draw_star(cx, cy, size):
        points = [
            cx, cy - size,
            cx + size * 0.28, cy - size * 0.28,
            cx + size, cy - size * 0.25,
            cx + size * 0.45, cy + size * 0.18,
            cx + size * 0.6, cy + size,
            cx, cy + size * 0.55,
            cx - size * 0.6, cy + size,
            cx - size * 0.45, cy + size * 0.18,
            cx - size, cy - size * 0.25,
            cx - size * 0.28, cy - size * 0.28,
        ]
        canvas.create_polygon(points, fill="#ffd43b", outline="#d28b00", width=2)

    draw_star(canvas_width // 2 + 15, canvas_height // 2 - 25, 19)
    draw_star(canvas_width // 2 + 75, canvas_height // 2 - 45, 22)
    draw_star(canvas_width // 2 + 135, canvas_height // 2 - 15, 17)

    status_label.config(text="Натисни кнопку, щоб почати гру")

    start_button.config(
        text="Почати гру",
        font=("Arial", 17, "bold"),
        bg="#ff5a3d",
        fg="white",
        activebackground="#e84a30",
        activeforeground="white",
        bd=0,
        padx=28,
        pady=10,
        cursor="hand2"
    )

    start_button.pack(pady=8)
    restart_button.pack_forget()


def show_finish_message(title, message):
    draw_game()

    canvas.create_rectangle(
        60, canvas_height // 2 - 95,
        canvas_width - 60, canvas_height // 2 + 95,
        fill="#ffffff",
        outline="#2f80ed",
        width=3
    )

    canvas.create_text(
        canvas_width // 2,
        canvas_height // 2 - 42,
        text=title,
        font=("Segoe UI", 24, "bold"),
        fill="#1b3a57"
    )

    canvas.create_text(
        canvas_width // 2,
        canvas_height // 2 + 2,
        text=message,
        font=("Segoe UI", 14),
        fill="#1b3a57"
    )

    canvas.create_text(
        canvas_width // 2,
        canvas_height // 2 + 42,
        text=f"Кроки: {steps}",
        font=("Segoe UI", 13, "bold"),
        fill="#1b3a57"
    )

    restart_button.pack(pady=8)


def start_game():
    global running, game_started, paused

    running = True
    paused = False
    game_started = True

    start_button.pack_forget()
    restart_button.pack_forget()

    move_ball()


def restart_game():
    reset_game()
    show_start_screen()


def stop_game():
    global running

    if game_started and running:
        running = False
        root.bell()
        show_finish_message(
            "Гру завершено",
            f"Гру зупинено користувачем. Залишилось призів: {prizes_left}"
        )


def toggle_pause():
    global paused

    if game_started and running:
        paused = not paused

        if paused:
            status_label.config(text="Пауза. Натисни Space, щоб продовжити.")
        else:
            move_ball()


def on_key(event):
    if event.keysym == "space":
        toggle_pause()
    elif event.keysym == "Escape":
        stop_game()
    elif game_started and running:
        stop_game()


def set_speed(new_delay):
    global delay
    delay = new_delay


def move_ball():
    global ball_row, ball_col, dr, dc, prizes_left, running, steps

    if not running or paused:
        return

    draw_game()

    if ball_row == finish_row and ball_col == finish_col:
        running = False
        root.bell()

        if prizes_left == 0:
            show_finish_message("Перемога!", "Кулька дійшла до фінішу. Усі призи зібрано.")
        else:
            show_finish_message("Гру завершено", f"Кулька дійшла до фінішу. Залишилось призів: {prizes_left}")

        return

    if steps > 5000:
        running = False
        root.bell()
        show_finish_message("Гру завершено", f"Кулька потрапила в цикл. Залишилось призів: {prizes_left}")
        return

    next_row = ball_row + dr
    next_col = ball_col + dc

    next_cell = level[next_row][next_col]

    if next_cell == WALL:
        dr = -dr
        dc = -dc
        root.bell()
    else:
        ball_row = next_row
        ball_col = next_col

        if next_cell == PRIZE:
            level[ball_row][ball_col] = " "
            prizes_left -= 1
            root.bell()

        elif next_cell == MIRROR1 or next_cell == MIRROR2:
            dr, dc = reflect(next_cell, dr, dc)

    steps += 1
    root.after(delay, move_ball)


root = tk.Tk()
root.title("Рух кульки")
root.configure(bg=BG)
root.resizable(False, False)

title_label = tk.Label(
    root,
    text="Red ball",
    font=("Segoe UI", 16, "bold"),
    bg=BG,
    fg=TEXT
)
title_label.pack(pady=(16, 6))

status_label = tk.Label(
    root,
    text="",
    font=("Segoe UI", 13),
    bg=BG,
    fg=MUTED
)
status_label.pack(pady=(0, 8))

canvas = tk.Canvas(root, bg=BG, highlightthickness=0)
canvas.pack(padx=16, pady=8)

buttons_frame = tk.Frame(root, bg=BG)
buttons_frame.pack(pady=4)

start_button = tk.Button(
    buttons_frame,
    text="Почати гру",
    font=("Arial", 16, "bold"),
    bg="#2d89ef",
    fg="white",
    padx=20,
    pady=8,
    command=start_game
)

restart_button = tk.Button(
    buttons_frame,
    text="Грати ще раз",
    font=("Arial", 16, "bold"),
    bg="#57cc99",
    fg="white",
    padx=20,
    pady=8,
    command=restart_game
)

speed_frame = tk.Frame(root, bg=BG)
speed_frame.pack(pady=5)

tk.Button(speed_frame, text="Повільно", command=lambda: set_speed(260)).pack(side="left", padx=4)
tk.Button(speed_frame, text="Нормально", command=lambda: set_speed(160)).pack(side="left", padx=4)
tk.Button(speed_frame, text="Швидко", command=lambda: set_speed(70)).pack(side="left", padx=4)

hint = tk.Label(
    root,
    text="Space — пауза | Esc або будь-яка інша клавіша — завершити гру",
    font=("Segoe UI", 10),
    bg=BG,
    fg="#6f8396"
)
hint.pack(pady=(4, 14))

root.bind("<Key>", on_key)

reset_game()
show_start_screen()

root.mainloop()