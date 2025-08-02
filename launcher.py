import tkinter as tk
import subprocess
import random
import threading
import time

# App paths
apps = {
    "Procrastinator Deluxe": "Procrastinator_Deluxe/procrastinator.py",
    "Mood Swings": "Mood_Swings/mood_detector.py",
    "Mouse Maze": "Mouse_Maze/mouse_maze.py",
    "Eye Tracker": "Eye_Tracker/eye_tracker.py",
    "Unhelpful Weather": "Unhelpful_Weather/weather.py"
}

opened_apps = set()

def launch_app(name):
    path = apps[name]
    subprocess.Popen(["python", path])
    opened_apps.add(name)
    if len(opened_apps) == len(apps):
        ram_button.config(state="normal")

def launch_ram_gobbler():
    subprocess.Popen(["python", "RAM_Gobbler/ram_monster.py"])

def trigger_bsod():
    time.sleep(random.randint(20, 30))
    bsod = tk.Toplevel(root)
    bsod.attributes('-fullscreen', True)
    bsod.configure(bg="blue")
    tk.Label(bsod, text="A problem has been detected and Windows has been shut down...", font=("Courier", 24), fg="white", bg="blue").pack(expand=True)
    tk.Label(bsod, text="Just Kidding JK, got you", font=("Courier", 32, "bold"), fg="yellow", bg="blue").pack()
    bsod.after(5000, bsod.destroy)

# Main launcher window
root = tk.Tk()
root.title("Appocalypse Launcher")
root.attributes('-fullscreen', True)
root.configure(bg="black")

tk.Label(root, text="Appocalypse", font=("Comic Sans MS", 36), fg="red", bg="black").pack(pady=20)

for name in apps:
    tk.Button(root, text=name, command=lambda n=name: launch_app(n), font=("Comic Sans MS", 16), bg="gray", fg="white").pack(pady=10)

ram_button = tk.Button(root, text="RAM Gobbler", command=launch_ram_gobbler, font=("Comic Sans MS", 16), bg="darkred", fg="white", state="disabled")
ram_button.pack(pady=20)

tk.Button(root, text="Quit", command=root.quit, font=("Comic Sans MS", 14), bg="red", fg="white").pack(pady=10)

# Escape key to exit fullscreen
root.bind("<Escape>", lambda e: root.attributes('-fullscreen', False))

# Start BSOD prank thread
threading.Thread(target=trigger_bsod, daemon=True).start()

root.mainloop()
