from ast import expr
import tkinter as tk
from PIL import Image
from PIL import ImageTk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sys
import os

# ----- Directory Path -----
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    return os.path.join(base_path, relative_path)

bg_path = resource_path("assets/background.png")
icon_path = resource_path("assets/icon.ico")

"""----- Main Window -----"""

# ----- Main Window Set Up -----
window = tk.Tk()
window.title("Graph Generator")
window.configure(bg="lightgray")
window.geometry("920x765+470+50")
window.resizable(False, False)

# ----- Icon Set Up -----
window.iconbitmap(icon_path)

# ----- Background Set Up -----
bg_image = Image.open(bg_path)
bg_photo = ImageTk.PhotoImage(bg_image)

background_frame = tk.Label(window, image=bg_photo)
background_frame.place(x=0, y=0, relwidth=1, relheight=1)


"""----- Main Body -----"""

# ----- Navigation -----
Header_frame = tk.Frame(background_frame, bg="#0d1b2a")
Header_frame.place(relx=0.5, y=20, anchor="center")

Header = tk.Label(Header_frame, text="Graph Generator", font=("Arial", 28, "bold"), fg="yellow", bg="#0d1b2a")
Header.pack()

# ----- Controls -----
main_menu = tk.Frame(window, bg="#0d1b2a")
main_menu.place(relx=0.5, y=130, anchor="center")

# ---Display
Text = tk.Label(main_menu, text="Enter Expression of Function [such as: x**2 or np.sin(x) or np.arccos(x)]", font=("Arial", 13), fg="white", bg="#0d1b2a")
Text.grid(row=0, column=1, padx=10, pady=5)

display = tk.Entry(main_menu, font=("Arial", 15), width=60, justify="center", relief=tk.RIDGE, borderwidth=5, textvariable=tk.StringVar())
display.grid(row=1, column=1, padx=10, pady=5)


"""----- Graph Plot -----"""

# ----- Plot -----
plot_frame = tk.Frame(window, bg="#0d1b2a")
plot_frame.place(relx=0.5, y=500, anchor="center")

#plot to draw...
figure, axis = plt.subplots()
figure.patch.set_facecolor("#0d1b2a")

#empty plot to show...
axis.clear()
axis.set_xlabel("x", color="white")
axis.set_ylabel("y", color="white")
axis.tick_params(axis="both", colors="white")
axis.set_facecolor("#0f2f51")
axis.grid(True, color="white")

canvas = FigureCanvasTkAgg(figure, master=plot_frame)
canvas.get_tk_widget().pack(fill="both", expand=True)
canvas.draw()

#list to track...
plot_list = []
current_index = -1

#functions....
def generate():
    global current_index

    expr = display.get().lower()
    plot_list.append(expr)
    current_index = len(plot_list) - 1

    draw_graph(expr)

def draw_graph(expr):
    for widget in plot_frame.winfo_children():
        widget.destroy()
    
    if expr == "":
        return
    x = np.linspace(-10, 10, 400)
    try:
        y = eval(expr)
    except:
        return

    axis.clear()
    axis.plot(x, y, label="Function", color="cyan", linestyle="-")
    axis.set_title(f"y = {expr}", color="white")
    axis.set_xlabel("x", color="white")
    axis.set_ylabel("y", color="white")
    axis.tick_params(axis="both", colors="white")
    axis.set_facecolor("#0f2f51")
    axis.grid(True, color="white")
    axis.legend(labelcolor="#ffffff").get_frame().set_facecolor("#5f6b02")

    canvas = FigureCanvasTkAgg(figure, master=plot_frame)
    canvas.get_tk_widget().pack(fill="both", expand=True)
    canvas.draw()



def previous():
    global current_index

    if current_index > 0:
        current_index -= 1

        display.delete(0, tk.END)
        display.insert(0, plot_list[current_index])

        draw_graph(plot_list[current_index])

def next():
    global current_index

    if current_index < len(plot_list) - 1:
        current_index += 1

        display.delete(0, tk.END)
        display.insert(0, plot_list[current_index])

        draw_graph(plot_list[current_index])

def clear():
    display.delete(0, tk.END)

    for widget in plot_frame.winfo_children():
        widget.destroy()
    
    axis.clear()
    axis.set_xlabel("x", color="white")
    axis.set_ylabel("y", color="white")
    axis.tick_params(axis="both", colors="white")
    axis.set_facecolor("#0f2f51")
    axis.grid(True, color="white")

    canvas = FigureCanvasTkAgg(figure, master=plot_frame)
    canvas.get_tk_widget().pack(fill="both", expand=True)
    canvas.draw()


#---Button-1
gen_btn = tk.Button(main_menu, text="Generate", font=("Arial", 12), command=generate, fg="lightgreen")
gen_btn.grid(row=2, column=1, padx=10, pady=5)
#---Button-2
prev_btn = tk.Button(main_menu, text="Previous", font=("Arial", 12), command=previous, fg="lightcoral")
prev_btn.grid(row=2, column=0, padx=10, pady=5)
#---Button-3
next_btn = tk.Button(main_menu, text="Next", font=("Arial", 12), command=next, fg="lightcoral")
next_btn.grid(row=2, column=2, padx=10, pady=5)
#---Button-4
clear_btn = tk.Button(main_menu, text="Clear", font=("Arial", 12), command=clear, fg="red")
clear_btn.grid(row=3, column=1, padx=10, pady=5)


# plot_label = tk.Label(plot_frame, text="Graph", fg="white", bg="#0d1b2a")
# plot_label.pack()

# ..... To Run The Screen Constantly .....
window.mainloop()
