import tkinter as tk
from tkinter import messagebox
import random
import time
import threading
from PIL import Image, ImageDraw, ImageTk

# Configuration
EYE_WIDTH = 120
EYE_HEIGHT = 80
BLINK_INTERVAL = 5
MESSAGE_INTERVAL = 10

# Thickness settings
BORDER_THICKNESS = 6 * 2
EYEBROW_THICKNESS = 6 * 20

messages = [
    "I thirst for blood...",
    "The night is eternal.",
    "You can't escape me.",
    "I see your soul.",
    "Your heartbeat quickens...",
    "Welcome to the darkness."
]

# Load background image
bg_path = "blood_background.png"
bg_img = Image.open(bg_path)
WINDOW_WIDTH, WINDOW_HEIGHT = bg_img.size

root = tk.Tk()
root.title("Dracula Eye Tracker")
root.attributes('-fullscreen', True)
root.configure(bg="black")

canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)

# Draw background image
bg_photo = ImageTk.PhotoImage(bg_img)
canvas.create_image(0, 0, image=bg_photo, anchor=tk.NW)
canvas.bg_photo = bg_photo

# Close button
def close_app():
    root.destroy()

close_button = tk.Button(root, text="Close App", command=close_app, bg="darkred", fg="white", font=("Arial", 12, "bold"))
close_button.place(x=WINDOW_WIDTH - 120, y=20)

# Escape key to close
root.bind("<Escape>", lambda e: close_app())

eyes = []

def create_dracula_eye(x, y):
    eye_img = Image.new("RGBA", (EYE_WIDTH, EYE_HEIGHT + 40), (0, 0, 0, 0))
    draw = ImageDraw.Draw(eye_img)

    draw.arc((0, 0, EYE_WIDTH, 30), start=0, end=180, fill="black", width=EYEBROW_THICKNESS)
    draw.ellipse((0, 40, EYE_WIDTH, 40 + EYE_HEIGHT), fill="white", outline="black", width=BORDER_THICKNESS)

    iris_width = 50
    iris_height = 40
    iris_x = (EYE_WIDTH - iris_width) // 2
    iris_y = 40 + (EYE_HEIGHT - iris_height) // 2
    draw.ellipse((iris_x, iris_y, iris_x + iris_width, iris_y + iris_height), fill="red")

    pupil_size = 20
    pupil_x = (EYE_WIDTH - pupil_size) // 2
    pupil_y = 40 + (EYE_HEIGHT - pupil_size) // 2
    draw.ellipse((pupil_x, pupil_y, pupil_x + pupil_size, pupil_y + pupil_size), fill="black")

    eye_photo = ImageTk.PhotoImage(eye_img)
    eye_id = canvas.create_image(x, y, image=eye_photo, anchor=tk.NW)
    return {"image": eye_photo, "id": eye_id, "x": x, "y": y, "photo": eye_photo}

def update_eye(event=None):
    eye = eyes[0]
    if event:
        cursor_x = event.x
        cursor_y = event.y
    else:
        cursor_x = WINDOW_WIDTH // 2
        cursor_y = WINDOW_HEIGHT // 2

    dx = cursor_x - (eye["x"] + EYE_WIDTH // 2)
    dy = cursor_y - (eye["y"] + EYE_HEIGHT // 2)
    max_offset = 15
    iris_offset_x = max(min(dx // 10, max_offset), -max_offset)
    iris_offset_y = max(min(dy // 10, max_offset), -max_offset)

    eye_img = Image.new("RGBA", (EYE_WIDTH, EYE_HEIGHT + 40), (0, 0, 0, 0))
    draw = ImageDraw.Draw(eye_img)

    draw.arc((0, 0, EYE_WIDTH, 30), start=0, end=180, fill="black", width=EYEBROW_THICKNESS)
    draw.ellipse((0, 40, EYE_WIDTH, 40 + EYE_HEIGHT), fill="white", outline="black", width=BORDER_THICKNESS)

    iris_center = (EYE_WIDTH // 2 + iris_offset_x, 40 + EYE_HEIGHT // 2 + iris_offset_y)
    draw.ellipse((iris_center[0] - 25, iris_center[1] - 20,
                  iris_center[0] + 25, iris_center[1] + 20), fill="red")
    draw.ellipse((iris_center[0] - 10, iris_center[1] - 10,
                  iris_center[0] + 10, iris_center[1] + 10), fill="black")

    eye_photo = ImageTk.PhotoImage(eye_img)
    canvas.itemconfig(eye["id"], image=eye_photo)
    eye["image"] = eye_photo
    eye["photo"] = eye_photo

def blink():
    while True:
        time.sleep(BLINK_INTERVAL)
        eye = eyes[0]
        blink_img = Image.new("RGBA", (EYE_WIDTH, EYE_HEIGHT + 40), (0, 0, 0, 0))
        draw = ImageDraw.Draw(blink_img)
        draw.rectangle((0, 40, EYE_WIDTH, 40 + EYE_HEIGHT), fill="black")
        draw.arc((0, 0, EYE_WIDTH, 30), start=0, end=180, fill="black", width=EYEBROW_THICKNESS)
        blink_photo = ImageTk.PhotoImage(blink_img)
        canvas.itemconfig(eye["id"], image=blink_photo)
        eye["image"] = blink_photo
        eye["photo"] = blink_photo
        time.sleep(0.2)
        update_eye()

def show_message():
    while True:
        time.sleep(MESSAGE_INTERVAL)
        msg = random.choice(messages)
        messagebox.showinfo("A Message", msg)

eye_x = (WINDOW_WIDTH - EYE_WIDTH) // 2
eye_y = (WINDOW_HEIGHT - EYE_HEIGHT) // 2 - 50
eyes.append(create_dracula_eye(eye_x, eye_y))

canvas.bind("<Motion>", update_eye)
canvas.focus_set()

threading.Thread(target=blink, daemon=True).start()
threading.Thread(target=show_message, daemon=True).start()

root.mainloop()
