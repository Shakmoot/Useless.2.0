import tkinter as tk
from tkinter import ttk
import random

# Data
ironic_quotes = [
    "Why try when you can cry?",
    "Procrastination builds character.",
    "Success is overrated.",
    "Tomorrow is a better day to start.",
    "You miss 100% of the naps you don’t take."
]

quiz_questions = [
    "Are you truly ready to begin?",
    "What is your spirit vegetable?",
    "How many tabs are too many?",
    "Is cereal a soup?",
    "Can you procrastinate procrastination?"
]

# App Setup
app = tk.Tk()
app.title("Procrastinator Deluxe")
app.attributes('-fullscreen', True)
app.configure(bg="black")

# Scrollable canvas to hold all content
canvas = tk.Canvas(app, bg="lightyellow")
scroll_y = tk.Scrollbar(app, orient="vertical", command=canvas.yview)
frame = tk.Frame(canvas, bg="lightyellow")

canvas.create_window((0, 0), window=frame, anchor='nw')
canvas.configure(yscrollcommand=scroll_y.set)

canvas.pack(side="left", fill="both", expand=True)
scroll_y.pack(side="right", fill="y")

def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox('all'))

frame.bind('<Configure>', on_configure)

# Title
tk.Label(frame, text="Procrastinator Deluxe", font=("Comic Sans MS", 24), bg="lightyellow").pack(pady=10)

# --- Motivational Quote Generator ---
quote_frame = tk.LabelFrame(frame, text="Motivational Quotes", font=("Comic Sans MS", 14), bg="lightblue", padx=10, pady=10)
quote_frame.pack(fill="x", padx=20, pady=10)

quote_label = tk.Label(quote_frame, text="", font=("Comic Sans MS", 12), wraplength=1000, bg="lightblue")
quote_label.pack()

def show_quote():
    quote_label.config(text=random.choice(ironic_quotes))

tk.Button(quote_frame, text="Inspire Me", command=show_quote, font=("Comic Sans MS", 12)).pack(pady=5)

# --- Fake Focus Mode ---
focus_frame = tk.LabelFrame(frame, text="Focus Mode", font=("Comic Sans MS", 14), bg="lightgreen", padx=10, pady=10)
focus_frame.pack(fill="x", padx=20, pady=10)

progress = ttk.Progressbar(focus_frame, orient="horizontal", length=1000, mode="indeterminate")
progress.pack(pady=5)
progress.start(10)

tk.Label(focus_frame, text="Loading productivity...", font=("Comic Sans MS", 12), bg="lightgreen").pack()

# --- Endless Productivity Quiz ---
quiz_frame = tk.LabelFrame(frame, text="Productivity Quiz", font=("Comic Sans MS", 14), bg="peachpuff", padx=10, pady=10)
quiz_frame.pack(fill="x", padx=20, pady=10)

question_label = tk.Label(quiz_frame, text="", font=("Comic Sans MS", 12), wraplength=1000, bg="peachpuff")
question_label.pack()

def next_question():
    question_label.config(text=random.choice(quiz_questions))

tk.Button(quiz_frame, text="Next Question", command=next_question, font=("Comic Sans MS", 12)).pack(pady=5)

# --- Progress Tracker ---
progress_frame = tk.LabelFrame(frame, text="Progress Tracker", font=("Comic Sans MS", 14), bg="lightcoral", padx=10, pady=10)
progress_frame.pack(fill="x", padx=20, pady=10)

canvas_graph = tk.Canvas(progress_frame, width=1000, height=200, bg="white")
canvas_graph.pack()

def draw_graph():
    canvas_graph.delete("all")
    for i in range(10):
        x = i * 100
        y = 200 - (i * random.randint(1, 10))  # downward trend
        canvas_graph.create_oval(x, y, x+10, y+10, fill="red")

tk.Button(progress_frame, text="Update Progress", command=draw_graph, font=("Comic Sans MS", 12)).pack(pady=5)

# --- Fake Meltdown on Quit ---
def meltdown_and_quit():
    meltdown = tk.Toplevel(app)
    meltdown.attributes('-fullscreen', True)
    meltdown.configure(bg="red")
    tk.Label(meltdown, text="SYSTEM FAILURE", font=("Courier", 48, "bold"), fg="white", bg="red").pack(expand=True)
    tk.Label(meltdown, text="Melting down in 3... 2... 1...", font=("Courier", 24), fg="white", bg="red").pack()
    meltdown.after(3000, app.quit)

# Quit Button
quit_frame = tk.Frame(frame, bg="lightyellow")
quit_frame.pack(pady=20)
tk.Button(quit_frame, text="Quit", command=meltdown_and_quit, font=("Comic Sans MS", 14), bg="red", fg="white").pack()

# Escape to exit fullscreen
def exit_fullscreen(event):
    app.attributes('-fullscreen', False)

app.bind("<Escape>", exit_fullscreen)

app.mainloop()
