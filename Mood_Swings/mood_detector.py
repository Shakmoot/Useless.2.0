import tkinter as tk
from PIL import Image, ImageTk
import random

# Define moods and their questions
moods = {
    "anger": [
        "Are you angry?",
        "You're a little bit angry, right?",
        "I know you have some anger in you.",
        "You seem pretty mad today, don't you?"
    ],
    "sadness": [
        "Are you feeling down?",
        "You've been a bit sad lately, haven't you?",
        "I can sense some sadness in you.",
        "You're not really smiling today, are you?"
    ],
    "happiness": [
        "Are you feeling happy?",
        "You've got a smile on, right?",
        "I bet you're having a good day.",
        "You're glowing with joy, aren't you?"
    ],
    "anxiety": [
        "Are you feeling anxious?",
        "Something's bothering you, right?",
        "You seem a bit tense.",
        "You're worried about something, aren't you?"
    ]
}

# Randomly select a mood
selected_mood = random.choice(list(moods.keys()))
questions = moods[selected_mood]

# Initialize window
root = tk.Tk()
root.title("Mood Detector")
root.geometry("600x400")
root.configure(bg="black")

question_index = 0

# Question label
question_label = tk.Label(root, text=questions[question_index], font=("Arial", 18), fg="white", bg="black", wraplength=500)
question_label.pack(pady=60)

# Button frame
button_frame = tk.Frame(root, bg="black")
button_frame.pack()

def next_question():
    global question_index
    question_index += 1
    if question_index < len(questions):
        question_label.config(text=questions[question_index])
    else:
        show_result()

def show_result():
    for widget in root.winfo_children():
        widget.destroy()

    result_label = tk.Label(root, text=f"Your mood is: {selected_mood.upper()}", font=("Arial", 22), fg="white", bg="black")
    result_label.pack(pady=20)

    try:
        mood_img = Image.open(f"{selected_mood}.png").resize((200, 200))
        mood_photo = ImageTk.PhotoImage(mood_img)
        img_label = tk.Label(root, image=mood_photo, bg="black")
        img_label.image = mood_photo
        img_label.pack(pady=10)
    except Exception as e:
        error_label = tk.Label(root, text="(Image not found)", font=("Arial", 14), fg="red", bg="black")
        error_label.pack()

# Yes/No buttons
yes_button = tk.Button(button_frame, text="Yes", font=("Arial", 16), width=10, command=next_question)
no_button = tk.Button(button_frame, text="No", font=("Arial", 16), width=10, command=next_question)
yes_button.grid(row=0, column=0, padx=20)
no_button.grid(row=0, column=1, padx=20)

root.mainloop()
