from tkinter import *
from tkinter import font as tkfont
import json
import os
from datetime import datetime

root = Tk()
root.title("Calculator")
root.geometry("380x550")
root.maxsize(600,900)
root.minsize(300,500)

root.configure(bg="#1a1a2e")
root.resizable(True, True)

# history file ka path
HISTORY_FILE = "calc_history.json"

# history load karo agar file exist karti h
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

# history save karo file mein
def save_to_history(expression, result):
    history = load_history()
    entry = {
        "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "expression": expression,
        "result": str(result)
    }
    history.append(entry)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

# DISPLAY
display_frame = Frame(root, bg="#1a1a2e")
display_frame.pack(fill=X, padx=20, pady=(20, 10))

# chota expression dikhane wala label
expr_label = Label(display_frame, text="",
                font=("Consolas", 13),
                bg="#1a1a2e", fg="#888", anchor="e")
expr_label.pack(fill=X)

# bada result dikhane wala label
result_label = Label(display_frame, text="0",
                    font=("Consolas", 42, "bold"),
                    bg="#1a1a2e", fg="white", anchor="e")
result_label.pack(fill=X)

# current expression store karne ke liye
current_expr = ""

# ======= FUNCTIONS =======
def press(value):
    global current_expr
    current_expr += str(value)
    result_label.config(text=current_expr)
    expr_label.config(text="")

def calculate():
    global current_expr
    try:
        expression = current_expr
        result = eval(current_expr)
        # agar result integer h toh .0 mat dikhao
        if result == int(result):
            result = int(result)
        save_to_history(expression, result)
        expr_label.config(text=expression + " =")
        result_label.config(text=str(result))
        current_expr = str(result)
    except:
        result_label.config(text="Error")
        current_expr = ""

def clear():
    global current_expr
    current_expr = ""
    result_label.config(text="0")
    expr_label.config(text="")

def backspace():
    global current_expr
    current_expr = current_expr[:-1]
    if current_expr == "":
        result_label.config(text="0")
    else:
        result_label.config(text=current_expr)

def toggle_sign():
    global current_expr
    try:
        val = eval(current_expr)
        current_expr = str(-val)
        result_label.config(text=current_expr)
    except:
        pass

def percentage():
    global current_expr
    try:
        val = eval(current_expr)
        current_expr = str(val / 100)
        result_label.config(text=current_expr)
    except:
        pass

# HISTORY WINDOW
def show_history():
    history = load_history()

    hist_win = Toplevel(root)
    hist_win.title("History")
    hist_win.geometry("400x500")
    hist_win.configure(bg="#1a1a2e")

    Label(hist_win, text="📋 Calculation History",
        font=("Consolas", 15, "bold"),
        bg="#1a1a2e", fg="white").pack(pady=10)

    # scrollable frame ke liye canvas
    canvas = Canvas(hist_win, bg="#1a1a2e", highlightthickness=0)
    scrollbar = Scrollbar(hist_win, orient="vertical",
                        command=canvas.yview)
    scroll_frame = Frame(canvas, bg="#1a1a2e")

    scroll_frame.bind("<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=10)
    scrollbar.pack(side="right", fill="y")

    if not history:
        Label(scroll_frame, text="Abhi koi history nahi h!",
            font=("Consolas", 12),
            bg="#1a1a2e", fg="#888").pack(pady=20)
    else:
# latest pehle dikhao
        for item in reversed(history):
            card = Frame(scroll_frame, bg="#16213e")
            card.pack(fill=X, pady=4, padx=5)

            Label(card, text=item["time"],
                font=("Consolas", 9),
                bg="#16213e", fg="#888").pack(
                anchor="w", padx=10, pady=(6, 0))

            Label(card,
                text=f"{item['expression']} = {item['result']}",
                font=("Consolas", 14, "bold"),
                bg="#16213e", fg="white").pack(
                anchor="w", padx=10, pady=(0, 6))

# clear history button
    def clear_history():
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
        hist_win.destroy()

    Button(hist_win, text="🗑 Clear History",
        font=("Consolas", 11),
        bg="#e94560", fg="white", relief="flat",
        command=clear_history).pack(pady=10)

# BUTTONS FRAME
btn_frame = Frame(root, bg="#1a1a2e")
btn_frame.pack(padx=15, pady=10, fill=BOTH, expand=True)

# columns aur rows ko stretch karne do
for i in range(4):
    btn_frame.columnconfigure(i, weight=1)
for i in range(6):
    btn_frame.rowconfigure(i, weight=1)

# button banana ka function
def make_btn(parent, text, row, col,
            bg="#16213e", fg="white",
            cmd=None, colspan=1):
    b = Button(parent, text=text,
            font=("Consolas", 16, "bold"),
            bg=bg, fg=fg,
            activebackground=fg,
            activeforeground=bg,
            relief="flat", bd=0,
            cursor="hand2",
            command=cmd)
    b.grid(row=row, column=col,
        columnspan=colspan,
        padx=4, pady=4,
        sticky="nsew")
    return b

# BUTTONS

# Row 0
make_btn(btn_frame, "H",   0, 0, bg="#0f3460", fg="#e94560", cmd=show_history)
make_btn(btn_frame, "+/-", 0, 1, bg="#0f3460", fg="white",   cmd=toggle_sign)
make_btn(btn_frame, "%",   0, 2, bg="#0f3460", fg="white",   cmd=percentage)
make_btn(btn_frame, "⌫",  0, 3, bg="#0f3460", fg="#e94560", cmd=backspace)

# Row 1
make_btn(btn_frame, "7", 1, 0, cmd=lambda: press("7"))
make_btn(btn_frame, "8", 1, 1, cmd=lambda: press("8"))
make_btn(btn_frame, "9", 1, 2, cmd=lambda: press("9"))
make_btn(btn_frame, "/", 1, 3, bg="#e94560", cmd=lambda: press("/"))

# Row 2
make_btn(btn_frame, "4", 2, 0, cmd=lambda: press("4"))
make_btn(btn_frame, "5", 2, 1, cmd=lambda: press("5"))
make_btn(btn_frame, "6", 2, 2, cmd=lambda: press("6"))
make_btn(btn_frame, "*", 2, 3, bg="#e94560", cmd=lambda: press("*"))

# Row 3
make_btn(btn_frame, "1", 3, 0, cmd=lambda: press("1"))
make_btn(btn_frame, "2", 3, 1, cmd=lambda: press("2"))
make_btn(btn_frame, "3", 3, 2, cmd=lambda: press("3"))
make_btn(btn_frame, "-", 3, 3, bg="#e94560", cmd=lambda: press("-"))

# Row 4
make_btn(btn_frame, "C", 4, 0, bg="#555",    cmd=clear)
make_btn(btn_frame, "0", 4, 1,               cmd=lambda: press("0"))
make_btn(btn_frame, ".", 4, 2,               cmd=lambda: press("."))
make_btn(btn_frame, "+", 4, 3, bg="#e94560", cmd=lambda: press("+"))

# Row 5 — = full width
make_btn(btn_frame, "=", 5, 0,
        bg="#e94560", fg="white",
        cmd=calculate, colspan=4)

root.mainloop()