from tkinter import *
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Arial"

new_card = {}


def remove_card():
    # print(len(data_dict))
    data_dict.remove(new_card)
    # print(len(data_dict))
    data_to_learn = pandas.DataFrame(data_dict)
    # index=False bedeutet, dass der DataFrame ohne eine Indexnummer in die CSV-Datei geschrieben wird
    data_to_learn.to_csv("data/words_to_learn.csv", index=False)
    get_new_card()


def get_new_card():
    # warum muss new_card und flip_timer als global definiert werden, data_dict aber nicht?
    # weil new_card und flip_timer hier neu gesetzt werden, während data_dict hier nur gelesen wird!
    global new_card, flip_timer

    # wenn noch ein Timer läuft, wird dieser jetzt gestoppt
    window.after_cancel(flip_timer)

    new_card = random.choice(data_dict)
    # print(new_card)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=new_card["French"], fill="Black")
    canvas.itemconfig(card_background, image=card_front_img)

    # nach Klick auf new card muss Timer neu gestartet werden
    flip_timer = window.after(3000, func=show_translation)


def show_translation():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=new_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


# ---------------------------- LOAD DATA ------------------------------- #
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")
# print(data)

# ansonsten wäre der Index auch immer mit dabei, deshalb besser eine Liste(!) mit vielen(!) Dictionaries
data_dict = data.to_dict(orient="records")
# print(data_dict[1])
# print(data_dict[1]["French"])
# print(data_dict[1]["English"])

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flash Card App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
# hier wird der Timer das erste Mal gestartet
flip_timer = window.after(3000, func=show_translation)

# mit der Größe des einzubettenden Bildes
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
# immer relativ zum Canvas
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="Title", fill="black", font=(FONT_NAME, 40, "italic"))
card_word = canvas.create_text(400, 263, text="Word", fill="black", font=(FONT_NAME, 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

wrong_img = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=wrong_img, highlightthickness=0, command=get_new_card)
unknown_button.grid(row=1, column=0)

right_img = PhotoImage(file="images/right.png")
known_button = Button(image=right_img, highlightthickness=0, command=remove_card)
known_button.grid(row=1, column=1)

# ---------------------------- Run program ------------------------------- #
get_new_card()
window.mainloop()
