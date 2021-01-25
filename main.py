from tkinter import *
import pandas
from random import choice

BACKGROUND_COLOR = "#B1DDC6"
ENGLISH_TEXT_FONT = ("Arial", 40, "italic")
SERBIAN_TEXT_FONT = ("Arial", 60, "bold")
current_word = {}
to_learn = {}

# ---------------------------- CREATE NEW FLASH CARDS ------------------------------- #
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/english_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_word, flip_timer
    window.after_cancel(flip_timer)
    canvas.itemconfig(image, image=card_front_img)
    canvas.itemconfig(card_title, text="English", fill="black")
    current_word = choice(to_learn)
    canvas.itemconfig(card_word, text=current_word["English"], fill="black")
    flip_timer = window.after(3000, flip_card)


def is_known():
    to_learn.remove(current_word)
    new_data = pandas.DataFrame(to_learn)
    new_data.to_csv("data/words_to_learn.csv", index=False)

    next_card()


# ---------------------------- FLIP THE CARDS ------------------------------- #
def flip_card():
    canvas.itemconfig(image, image=card_back_img)
    canvas.itemconfig(card_title, text="Serbian", fill="white")
    canvas.itemconfig(card_word, text=current_word["Serbian"], fill="white")


# ---------------------------- UI SETUP ------------------------------- #
#        []       {}      ✔
# Window start
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)
# CANVAS start
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)

card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
image = canvas.create_image(400, 263, image=card_front_img)

card_title = canvas.create_text(400, 150, text="Title", font=ENGLISH_TEXT_FONT)
card_word = canvas.create_text(400, 263, text="word", font=SERBIAN_TEXT_FONT)

canvas.grid(column=0, row=0, columnspan=2)
# CANVAS end

# BUTTONS start
right_button_img = PhotoImage(file="images/right.png")
known_button = Button(image=right_button_img, highlightthickness=0, bg=BACKGROUND_COLOR, command=is_known)
known_button.grid(column=0, row=1)

wrong_button_img = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=wrong_button_img, highlightthickness=0, bg=BACKGROUND_COLOR, command=next_card)
unknown_button.grid(column=1, row=1)

# BUTTONS end

next_card()

window.mainloop()
# Window end
