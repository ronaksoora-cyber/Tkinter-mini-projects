from tkinter import *

root = Tk()

root.title("Resize Window")
root.geometry("400x200")

# ek function bna lete h jo window ka size change kare
def apply_size():
    try:
        w = int(width_entry.get())
        h = int(height_entry.get())
        root.geometry(f"{w}x{h}")
    except ValueError:
        print("Put the valid number")

#label or entry box width ke liye 
Label(root, text="Width:").pack(pady=5)
width_entry = Entry(root)
width_entry.pack(pady=5)

#label or entry box height ke liye
Label(root, text="Height:").pack(pady=5)
height_entry = Entry(root)
height_entry.pack(pady=5)

# button jo click karne par apply_size function call kare
Button(root, text="Apply", command=apply_size).pack(pady=10)

root.mainloop()