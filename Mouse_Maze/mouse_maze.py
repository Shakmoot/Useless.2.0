import tkinter as tk
import math

# Maze layout with finish blocked off
maze = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1],
    [1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
    [1,0,0,0,0,1,0,0,0,1,0,0,0,1,0,1],
    [1,0,1,1,1,1,1,1,0,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1],  # finish blocked here
    [1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1],
    [1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1],
    [1,0,1,1,0,1,1,1,1,1,1,1,0,1,0,1],
    [1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1],
    [1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1]
]

root = tk.Tk()
root.title("Mouse Maze: No Escape Edition")
root.attributes('-fullscreen', True)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

rows = len(maze)
cols = len(maze[0])

taunt_area_height = int(screen_height * 0.15)

cell_width = screen_width // cols
cell_height = (screen_height - taunt_area_height) // rows
cell_size = min(cell_width, cell_height)

width = cols * cell_size
height = rows * cell_size

canvas_x = (screen_width - width) // 2
canvas_y = taunt_area_height

canvas = tk.Canvas(root, width=width, height=height, bg="white")
canvas.place(x=canvas_x, y=canvas_y)

# Draw maze
walls = []
for i in range(rows):
    for j in range(cols):
        x1 = j * cell_size
        y1 = i * cell_size
        x2 = x1 + cell_size
        y2 = y1 + cell_size
        if maze[i][j] == 1:
            wall = canvas.create_rectangle(x1, y1, x2, y2, fill="black")
            walls.append((x1, y1, x2, y2))

# Draw finish (still unreachable)
finish_x = (cols - 1) * cell_size
finish_y = (rows // 2) * cell_size
canvas.create_rectangle(finish_x, finish_y, finish_x + cell_size, finish_y + cell_size, fill="gold", outline="black")
canvas.create_text(finish_x + cell_size // 2, finish_y + cell_size // 2, text="🏁", font=("Arial", cell_size // 2))

# Taunting messages
taunts = [
    "You'll never reach the finish!",
    "Is that all you've got?",
    "Too slow! My grandma moves faster!",
    "Careful! You might get lost forever.",
    "This maze is too smart for you!",
    "Haha! It's literally impossible!"
]
taunt_index = 0

taunt_label = tk.Label(root, text=taunts[0], font=("Arial", 36, "bold"), fg="red", bg="white")
taunt_label.place(x=20, y=20)

def switch_taunt():
    global taunt_index
    taunt_index = (taunt_index + 1) % len(taunts)
    taunt_label.config(text=taunts[taunt_index])
    root.after(3000, switch_taunt)

root.after(3000, switch_taunt)

# Mouse icon radius
mouse_radius = cell_size // 4

# Find a safe starting point in the maze (e.g., first open cell)
start_row, start_col = None, None
for i in range(rows):
    for j in range(cols):
        if maze[i][j] == 0:
            start_row, start_col = i, j
            break
    if start_row is not None:
        break

start_x = start_col * cell_size + cell_size // 2
start_y = start_row * cell_size + cell_size // 2

mouse_icon = canvas.create_oval(
    start_x - mouse_radius, start_y - mouse_radius,
    start_x + mouse_radius, start_y + mouse_radius,
    fill="pink", outline="black"
)

# Collision detection
def is_colliding(x, y):
    for x1, y1, x2, y2 in walls:
        if x1 <= x <= x2 and y1 <= y <= y2:
            return True
    return False

# Follow mouse smoothly with collision-safe interpolation
def follow_cursor(event):
    target_x = event.x_root - canvas_x
    target_y = event.y_root - canvas_y

    current_coords = canvas.coords(mouse_icon)
    if not current_coords:
        return

    cx = (current_coords[0] + current_coords[2]) / 2
    cy = (current_coords[1] + current_coords[3]) / 2

    dx = target_x - cx
    dy = target_y - cy
    dist = math.hypot(dx, dy)

    max_step = cell_size / 5
    steps = max(1, int(dist / max_step))

    for i in range(1, steps + 1):
        ix = cx + dx * i / steps
        iy = cy + dy * i / steps
        if is_colliding(ix, iy):
            break
        canvas.coords(mouse_icon, ix - mouse_radius, iy - mouse_radius, ix + mouse_radius, iy + mouse_radius)

root.bind("<Motion>", follow_cursor)

# Close button
close_btn = tk.Button(root, text="Close", command=root.destroy, font=("Arial", 14), bg="red", fg="white")
close_btn.place(x=screen_width - 100, y=20)

root.mainloop()
