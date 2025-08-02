import tkinter as tk
from PIL import Image, ImageTk

# Initialize fullscreen window
root = tk.Tk()
root.title("RAM Gobbler Test")
root.attributes("-fullscreen", True)
root.configure(bg="black")

# Load monster image
monster_img = Image.open("monster.png")
monster_size = 150
monster_photo = ImageTk.PhotoImage(monster_img.resize((monster_size, monster_size)))
monster_label = tk.Label(root, image=monster_photo, bg="black")
monster_label.place(x=root.winfo_screenwidth() // 2 - monster_size // 2,
                    y=root.winfo_screenheight() // 2 - monster_size // 2)

# RAM feed counter
feed_count = 0
dragging = False
ram_label = None
growing = False

# Load RAM icon
ram_img = Image.open("ram.png").resize((50, 50))
ram_photo = ImageTk.PhotoImage(ram_img)

def spawn_ram():
    global ram_label
    ram_label = tk.Label(root, image=ram_photo, bg="black")
    ram_label.place(x=50, y=root.winfo_screenheight() - 100)
    ram_label.bind("<ButtonPress-1>", on_drag_start)
    ram_label.bind("<B1-Motion>", on_drag_motion)
    ram_label.bind("<ButtonRelease-1>", on_drag_release)

def grow_monster():
    global monster_size, monster_photo
    if growing:
        monster_size += 20
        new_monster = ImageTk.PhotoImage(monster_img.resize((monster_size, monster_size)))
        monster_label.config(image=new_monster)
        monster_label.image = new_monster
        monster_label.place(x=root.winfo_screenwidth() // 2 - monster_size // 2,
                            y=root.winfo_screenheight() // 2 - monster_size // 2)
        root.after(50, grow_monster)

def check_collision(ram_x, ram_y):
    global feed_count, monster_size, monster_photo, ram_label, growing

    monster_x = monster_label.winfo_x()
    monster_y = monster_label.winfo_y()
    monster_w = monster_label.winfo_width()
    monster_h = monster_label.winfo_height()

    # Check if RAM overlaps monster
    if (monster_x < ram_x < monster_x + monster_w) and (monster_y < ram_y < monster_y + monster_h):
        feed_count += 1
        monster_size += 50
        new_monster = ImageTk.PhotoImage(monster_img.resize((monster_size, monster_size)))
        monster_label.config(image=new_monster)
        monster_label.image = new_monster
        monster_label.place(x=root.winfo_screenwidth() // 2 - monster_size // 2,
                            y=root.winfo_screenheight() // 2 - monster_size // 2)

        ram_label.destroy()
        ram_label = None

        if feed_count >= 6:
            root.configure(bg="red")
            message_label.config(text="💥 The monster ate all your RAM! 💥", fg="white", font=("Arial", 24))
            growing = True
            grow_monster()
            root.after(3000, root.destroy)
        else:
            spawn_ram()

def on_drag_start(event):
    global dragging
    dragging = True

def on_drag_motion(event):
    if dragging and ram_label:
        ram_label.place(x=event.x_root - root.winfo_rootx() - 25, y=event.y_root - root.winfo_rooty() - 25)
        check_collision(event.x_root - root.winfo_rootx(), event.y_root - root.winfo_rooty())

def on_drag_release(event):
    global dragging
    dragging = False
    if ram_label:
        ram_label.place(x=50, y=root.winfo_screenheight() - 100)

# Message label
message_label = tk.Label(root, text="Drag RAM to feed the monster!", font=("Arial", 18), bg="black", fg="lime")
message_label.pack()

# Spawn the first RAM icon
spawn_ram()

root.mainloop()
