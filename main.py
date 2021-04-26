from tkinter import *
from random import choices
import math

# ---------------------------- CONSTANTS ------------------------------- #
YELLOW = "#fcf4d9"
RED = "#ff7a5a"
BLUE = "#456672"
FONT_NAME = "Courier"
WORK_SEC = 60
NO_WORDS = 200      # Max 1000
timer = None
test_list = []
test_output = ""


# ----------------------------START GAME ----------------------------------------- #
def start_game():
    global test_list, test_output

    start_button.config(state=DISABLED)
    user_input.delete(1.0, END)

    with open("word_list.txt", 'r') as text_file:
        word_list = [line.replace('\n', '') for line in text_file.readlines()]

    test_list = choices(word_list, k=NO_WORDS)
    test_output = ' '.join(test_list)

    text_canvas.itemconfig(test_text, text=test_output, font=(FONT_NAME, 12, "normal"))
    count_down(WORK_SEC)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):

    count_min = math.floor(count/60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    timer_canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}", fill=BLUE)

    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
        if count <= 5:
            timer_canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}", fill=RED)
    else:
        results()
        start_button.config(text="Restart", state=NORMAL)


# -------------------------SHOW RESULTS OF SPEED TEST ---------------------------- #
def results():
    timer_canvas.itemconfig(timer_text, text=f"Test Complete!", fill="green")
    user_answer = user_input.get(1.0, END).replace('\n', '').split(' ')
    if user_answer[0] == '':
        words = 0
    else:
        words = len(user_answer)

    try:
        wpm = int(words * 60 / WORK_SEC)
        score = 0
        for item in range(0, words):
            if test_list[item] == user_answer[item]:
                score += 1
        accuracy = int(round(score / words * 100, 0))
    except ZeroDivisionError:
        wpm = 0
        accuracy = 0

    text_canvas.itemconfig(timer_text,
                           text=f"You typed {wpm} words per minute, with an accuracy of {accuracy}%",
                           font=(FONT_NAME, 12, "bold"))


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Speed Typing Test")
window.config(padx=100, pady=50, bg=YELLOW)

title_label = Label(text="Speed Typing Test", fg=BLUE, bg=YELLOW, font=(FONT_NAME, 30, "bold"))
title_label.grid(column=0, columnspan=2, row=0, pady=20)

timer_canvas = Canvas(width=700, height=30, bg=YELLOW, highlightthickness=0)
timer_text = timer_canvas.create_text(100, 15, text="00:00", fill=BLUE, font=(FONT_NAME, 12, "bold"))
timer_canvas.grid(column=1, row=1)

timer_label = Label(text="Timer:", fg=BLUE, bg=YELLOW, font=(FONT_NAME, 12, "bold"))
timer_label.grid(column=0, row=1)

text_canvas = Canvas(width=800, height=350, bg=YELLOW, highlightthickness=0)
test_text = text_canvas.create_text(400, 175, width=800,
                                    text="Welcome to the speed typing test!\n\nClick 'Start' to begin.",
                                    fill=BLUE,
                                    font=(FONT_NAME, 12, "bold"))
text_canvas.grid(column=0, columnspan=2, row=2)

user_input = Text(width=100, height=20, highlightthickness=0)
user_input.grid(column=0, columnspan=2, row=3)

start_button = Button(text="Start", highlightthickness=0, command=start_game, bg=BLUE, fg="white",
                      width=50, height=2, font=(FONT_NAME, 12, "bold"))
start_button.grid(column=0, columnspan=2, row=4, pady=30)

window.mainloop()

