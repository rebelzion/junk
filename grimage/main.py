import tkinter as tk

window = tk.Tk()
window.title('Grimage - a Image Layout Editor')

# get the screen dimension
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
print(screen_width, screen_height)

window_width = screen_width // 2
window_height = screen_height // 2

window.geometry(f'{window_width}x{window_height}+{screen_width // 4}+{screen_height // 4}')

"""
# TODO @vronin: add upload photo and drag and drop
# TODO @vronin: add sidebar to choose between different layouts
# TODO @vronin: add a button to save the layout photo
"""


window.mainloop()
