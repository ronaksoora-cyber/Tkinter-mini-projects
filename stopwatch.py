from tkinter import *
from tkinter import ttk, messagebox
import time
import threading

root = Tk()
root.title("Stopwatch")
root.geometry("680x500")
root.minsize(300,500)
root.maxsize(900,800)
root.configure(bg="#1E293B")
root.resizable(True, True)
root.minsize(460, 580)

# Colors
BG      = "#1E293B"
CARD    = "#0F172A"
BORDER  = "#334155"
BLUE    = "#3B82F6"
RED     = "#EF4444"
ORANGE  = "#F97316"
GRAY    = "#475569"
WHITE   = "#F1F5F9"
MUTED   = "#94A3B8"
GREEN   = "#22C55E"
ACCENT  = "#38BDF8"
PURPLE  = "#A855F7"

#  State
sw_running  = False
sw_elapsed  = 0.0
sw_start    = 0.0
laps        = []

timer_running = False
timer_elapsed = 0
timer_thread  = None


#  HEADER

hdr = Frame(root, bg=BG)
hdr.pack(fill=X, padx=20, pady=(16,0))

Label(hdr, text="DESKTOP", font=("Segoe UI", 12, "bold"),
    bg=BG, fg=WHITE).pack(side=LEFT)
Label(hdr, text=" STOPWATCH ", font=("Segoe UI", 12, "bold"),
    bg=BG, fg=ACCENT).pack(side=LEFT)
Label(hdr, text="APP", font=("Segoe UI", 12, "bold"),
    bg=BG, fg=WHITE).pack(side=LEFT)

Label(root, text="Modern  •  Clean  •  Functional",
    font=("Segoe UI", 9), bg=BG, fg=MUTED).pack(pady=(2,10))


#  MAIN CARD

card = Frame(root, bg=CARD, bd=0)
card.pack(fill=BOTH, expand=True, padx=16, pady=(0,16))

# content area
content_area = Frame(card, bg=CARD)
content_area.pack(fill=BOTH, expand=True)


#  HELPER — round button

def mk_btn(parent, text, bg, cmd, w=12, h=1):
    return Button(parent, text=text,
                font=("Segoe UI", 11, "bold"),
                bg=bg, fg=WHITE,
                activebackground=WHITE,
                activeforeground=bg,
                relief="flat", bd=0,
                width=w, height=h,
                cursor="hand2",
                command=cmd)


#  PAGE 1 — STOPWATCH

sw_page = Frame(content_area, bg=CARD)

time_var = StringVar(value="00:00:00")
ms_var   = StringVar(value=".00")

# big clock
clock_row = Frame(sw_page, bg=CARD)
clock_row.pack(pady=(28,4))
Label(clock_row, textvariable=time_var,
    font=("Segoe UI", 56, "bold"),
    bg=CARD, fg=WHITE).pack(side=LEFT)
Label(clock_row, textvariable=ms_var,
    font=("Segoe UI", 28, "bold"),
    bg=CARD, fg=ACCENT).pack(side=LEFT, anchor=S, pady=(0,10))

# sw buttons

sw_btn_row = Frame(sw_page, bg=CARD)
sw_btn_row.pack(pady=12)

def sw_tick():
    while sw_running:
        elapsed = time.time() - sw_start
        h  = int(elapsed // 3600)
        m  = int((elapsed % 3600) // 60)
        s  = int(elapsed % 60)
        ms = int((elapsed * 100) % 100)
        time_var.set(f"{h:02d}:{m:02d}:{s:02d}")
        ms_var.set(f".{ms:02d}")
        time.sleep(0.01)

def sw_start_fn():
    global sw_running, sw_start, sw_elapsed
    if not sw_running:
        sw_running = True
        sw_start = time.time() - sw_elapsed
        threading.Thread(target=sw_tick, daemon=True).start()

def sw_stop_fn():
    global sw_running, sw_elapsed
    if sw_running:
        sw_elapsed = time.time() - sw_start
        sw_running = False

def sw_reset_fn():
    global sw_running, sw_elapsed
    sw_running = False
    sw_elapsed = 0.0
    time_var.set("00:00:00")
    ms_var.set(".00")
    laps.clear()
    render_laps()

def sw_lap_fn():
    if sw_running:
        e = time.time() - sw_start
        h = int(e // 3600)
        m = int((e % 3600) // 60)
        s = int(e % 60)
        ms= int((e * 100) % 100)
        laps.append(f"{h:02d}:{m:02d}:{s:02d}.{ms:02d}")
        render_laps()

mk_btn(sw_btn_row, "▶  Start", BLUE,    sw_start_fn).pack(side=LEFT, padx=5)
mk_btn(sw_btn_row, "⏹  Stop",  RED,     sw_stop_fn).pack(side=LEFT, padx=5)
mk_btn(sw_btn_row, "↺  Reset", GRAY,    sw_reset_fn).pack(side=LEFT, padx=5)

# lap button
mk_btn(sw_page, "+ Lap", BORDER, sw_lap_fn, w=10, h=1).pack(pady=(0,8))

# separator
Frame(sw_page, bg=BORDER, height=1).pack(fill=X, padx=20, pady=4)

# lap rows
lap_container = Frame(sw_page, bg=CARD)
lap_container.pack(fill=BOTH, expand=True, padx=20)

def delete_lap(i):
    laps.pop(i)
    render_laps()

def render_laps():
    for w in lap_container.winfo_children():
        w.destroy()
    for i, lap in enumerate(reversed(laps)):
        real_i = len(laps)-1-i
        row = Frame(lap_container, bg=CARD)
        row.pack(fill=X, pady=3)
        Label(row, text=f"Lap {real_i+1}",
            font=("Segoe UI", 11), bg=CARD, fg=MUTED,
            width=7, anchor=W).pack(side=LEFT)
        Label(row, text=lap,
            font=("Segoe UI", 11, "bold"),
            bg=CARD, fg=WHITE).pack(side=LEFT, expand=True)
        Button(row, text="🗑", font=("Segoe UI", 10),
            bg=CARD, fg=MUTED,
            activebackground=RED, activeforeground=WHITE,
            relief="flat", bd=0, cursor="hand2",
            command=lambda i=real_i: delete_lap(i)).pack(side=RIGHT)


#  PAGE 2 — TIMER

timer_page = Frame(content_area, bg=CARD)

Label(timer_page, text="Countdown Timer",
    font=("Segoe UI", 15, "bold"),
    bg=CARD, fg=WHITE).pack(pady=(28,8))

timer_var = StringVar(value="00:10:00")
Label(timer_page, textvariable=timer_var,
    font=("Segoe UI", 54, "bold"),
    bg=CARD, fg=WHITE).pack()

# spinboxes

spin_row = Frame(timer_page, bg=CARD)
spin_row.pack(pady=12)

def mk_spin(parent, label, maxv):
    f = Frame(parent, bg=CARD)
    f.pack(side=LEFT, padx=12)
    Label(f, text=label, font=("Segoe UI", 9),
        bg=CARD, fg=MUTED).pack()
    sp = Spinbox(f, from_=0, to=maxv, width=4,
                font=("Segoe UI", 13, "bold"),
                bg=BORDER, fg=WHITE,
                buttonbackground=GRAY,
                relief="flat", justify=CENTER,
                format="%02.0f")
    sp.pack()
    return sp

sp_h = mk_spin(spin_row, "HH", 23)
sp_m = mk_spin(spin_row, "MM", 59)
sp_s = mk_spin(spin_row, "SS", 59)

# set default 10 min

sp_m.delete(0, END); sp_m.insert(0, "10")

t_status = Label(timer_page, text="",
                font=("Segoe UI", 11), bg=CARD, fg=GREEN)
t_status.pack(pady=4)

def timer_tick():
    global timer_elapsed, timer_running
    while timer_running and timer_elapsed > 0:
        time.sleep(1)
        timer_elapsed -= 1
        h = timer_elapsed//3600
        m = (timer_elapsed%3600)//60
        s = timer_elapsed%60
        timer_var.set(f"{h:02d}:{m:02d}:{s:02d}")
    if timer_running and timer_elapsed == 0:
        t_status.config(text="✅ Time's up!", fg=GREEN)
        timer_running = False

def timer_start():
    global timer_running, timer_elapsed
    if not timer_running:
        try:
            h = int(sp_h.get()); m = int(sp_m.get()); s = int(sp_s.get())
            timer_elapsed = h*3600 + m*60 + s
            if timer_elapsed > 0:
                timer_running = True
                t_status.config(text="⏳ Running...", fg=ACCENT)
                threading.Thread(target=timer_tick, daemon=True).start()
        except: pass

def timer_pause():
    global timer_running
    timer_running = False
    t_status.config(text="⏸ Paused", fg=MUTED)

def timer_reset():
    global timer_running, timer_elapsed
    timer_running = False
    timer_elapsed = 0
    timer_var.set("00:00:00")
    t_status.config(text="")

tb_row = Frame(timer_page, bg=CARD)
tb_row.pack(pady=10)
mk_btn(tb_row, "▶  Start", BLUE,   timer_start).pack(side=LEFT, padx=5)
mk_btn(tb_row, "⏸  Pause", ORANGE, timer_pause).pack(side=LEFT, padx=5)
mk_btn(tb_row, "↺  Reset", GRAY,   timer_reset).pack(side=LEFT, padx=5)


#  PAGE 3 — ALARM

alarm_page = Frame(content_area, bg=CARD)

Label(alarm_page, text="Set Alarm",
    font=("Segoe UI", 15, "bold"),
    bg=CARD, fg=WHITE).pack(pady=(28,16))

# time input row

alarm_time_row = Frame(alarm_page, bg=CARD)
alarm_time_row.pack()

alarm_h = mk_spin(alarm_time_row, "HH", 23)
alarm_m = mk_spin(alarm_time_row, "MM", 59)

# AM/PM
ampm_var = StringVar(value="AM")
ampm_frame = Frame(alarm_time_row, bg=CARD)
ampm_frame.pack(side=LEFT, padx=12)
Label(ampm_frame, text="AM/PM", font=("Segoe UI", 9),
    bg=CARD, fg=MUTED).pack()
OptionMenu(ampm_frame, ampm_var, "AM", "PM").pack()

# repeat
Label(alarm_page, text="Repeat",
    font=("Segoe UI", 11), bg=CARD, fg=MUTED).pack(pady=(16,4))
repeat_var = StringVar(value="Daily")
repeat_menu = OptionMenu(alarm_page, repeat_var,
                        "Once", "Daily", "Weekdays", "Weekends")
repeat_menu.config(bg=BORDER, fg=WHITE, relief="flat",
                font=("Segoe UI", 11), width=16)
repeat_menu.pack()

alarm_status = Label(alarm_page, text="",
                    font=("Segoe UI", 11), bg=CARD, fg=GREEN)
alarm_status.pack(pady=8)

def set_alarm():
    try:
        h = int(alarm_h.get())
        m = int(alarm_m.get())
        ap = ampm_var.get()
        rp = repeat_var.get()
        alarm_status.config(
            text=f"✅ Alarm set for {h:02d}:{m:02d} {ap} ({rp})",
            fg=GREEN)
    except:
        alarm_status.config(text="Invalid time!", fg=RED)

def clear_alarm():
    alarm_status.config(text="🔕 Alarm cleared", fg=MUTED)

ab_row = Frame(alarm_page, bg=CARD)
ab_row.pack(pady=8)
mk_btn(ab_row, "🔔  Set Alarm",   BLUE, set_alarm).pack(side=LEFT, padx=5)
mk_btn(ab_row, "🔕  Clear",       GRAY, clear_alarm).pack(side=LEFT, padx=5)


#  PAGE 4 — LAP LIST

laplist_page = Frame(content_area, bg=CARD)

Label(laplist_page, text="All Laps",
    font=("Segoe UI", 15, "bold"),
    bg=CARD, fg=WHITE).pack(pady=(28,10))

lap_lb = Listbox(laplist_page,
                font=("Segoe UI", 12),
                bg=CARD, fg=WHITE,
                selectbackground=BLUE,
                relief="flat", bd=0,
                highlightthickness=0,
                activestyle="none")
lap_lb.pack(fill=BOTH, expand=True, padx=24, pady=4)

def refresh_laplist():
    lap_lb.delete(0, END)
    if not laps:
        lap_lb.insert(END, "  No laps recorded yet")
    for i, lap in enumerate(laps):
        lap_lb.insert(END, f"  Lap {i+1}          {lap}")

mk_btn(laplist_page, "🔄 Refresh", BLUE,refresh_laplist, w=14).pack(pady=10)


#  PAGE 5 — SETTINGS

settings_page = Frame(content_area, bg=CARD)

Label(settings_page, text="Settings",
    font=("Segoe UI", 15, "bold"),
    bg=CARD, fg=WHITE).pack(pady=(28,20))

# dark mode toggle

dark_var = BooleanVar(value=True)

def make_setting_row(parent, label, widget_fn):
    row = Frame(parent, bg="#1a2744", bd=0)
    row.pack(fill=X, padx=24, pady=6)
    Label(row, text=label, font=("Segoe UI", 12),
        bg="#1a2744", fg=WHITE,
        anchor=W).pack(side=LEFT, padx=14, pady=12)
    widget_fn(row).pack(side=RIGHT, padx=14, pady=12)

def dark_toggle(parent):
    cb = Checkbutton(parent, variable=dark_var,
                    bg="#1a2744", activebackground="#1a2744",
                    selectcolor=BLUE,
                    relief="flat", cursor="hand2")
    return cb

make_setting_row(settings_page, "🌙  Dark Mode", dark_toggle)

# theme colors

Label(settings_page, text="Theme Color",
    font=("Segoe UI", 11), bg=CARD, fg=MUTED).pack(pady=(14,6))

color_row = Frame(settings_page, bg=CARD)
color_row.pack()

themes = [BLUE, PURPLE, GREEN, RED, ORANGE, ACCENT]
for c in themes:
    b = Button(color_row, bg=c, width=3, height=1,
            relief="flat", cursor="hand2",
            activebackground=WHITE)
    b.pack(side=LEFT, padx=5)

Label(settings_page, text="v1.0  •  Tkinter Mini Projects",
    font=("Segoe UI", 9), bg=CARD, fg=BORDER).pack(pady=(30,0))


#  BOTTOM TAB BAR — 5 tabs

Frame(card, bg=BORDER, height=1).pack(fill=X)

tab_bar = Frame(card, bg=CARD)
tab_bar.pack(fill=X, side=BOTTOM)

pages    = [sw_page, timer_page, alarm_page, laplist_page, settings_page]
tab_data = [
    ("⏱", "Stopwatch"),
    ("⏳", "Timer"),
    ("🔔", "Alarm"),
    ("☰", "Lap List"),
    ("⚙", "Settings"),
]
tab_btns   = []
underlines = []

def switch_tab(idx):
    for p in pages:
        p.pack_forget()
    pages[idx].pack(fill=BOTH, expand=True)
    if idx == 3:
        refresh_laplist()
    for i, (b, ul) in enumerate(zip(tab_btns, underlines)):
        if i == idx:
            b.config(fg=ACCENT)
            ul.config(bg=ACCENT)
        else:
            b.config(fg=MUTED)
            ul.config(bg=CARD)

for i, (icon, name) in enumerate(tab_data):
    tf = Frame(tab_bar, bg=CARD)
    tf.pack(side=LEFT, expand=True)
    b = Button(tf, text=f"{icon}\n{name}",
            font=("Segoe UI", 8),
            bg=CARD, fg=MUTED,
            activebackground=CARD,
            activeforeground=ACCENT,
            relief="flat", bd=0,
            padx=4, pady=8,
            cursor="hand2",
            command=lambda i=i: switch_tab(i))
    b.pack(fill=X)
    tab_btns.append(b)
    ul = Frame(tf, bg=CARD, height=2)
    ul.pack(fill=X)
    underlines.append(ul)

switch_tab(0)
root.mainloop()