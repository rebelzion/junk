"""
# TODO @vronin: add sidebar to choose between different layouts
# TODO @vronin: add a button to save the layout photo
"""

import tkinter as tk
from tkinter import filedialog
from tkinter.messagebox import askyesnocancel
import logging
import argparse


# Global variables
FORMAT = "[%(levelname)s][%(filename)s:%(lineno)s - %(funcName)20s()] %(message)s"
APP_NAME = "Grimage"

logging.basicConfig(level=logging.INFO, format=FORMAT)


def create_root():
    root = tk.Tk()
    root.title(f'{APP_NAME} - a Image Layout Editor')

    # get the screen dimension
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    logging.info(f"Window screen dimensions({screen_width=}, {screen_height=})")

    window_width = screen_width // 2
    window_height = screen_height // 2

    root.geometry(f'{window_width}x{window_height}+{screen_width // 4}+{screen_height // 4}')

    return root

def UploadAction(event=None):
    filenames = filedialog.askopenfilenames(parent=root, title='Upload image(s)')
    logging.debug(f'UploadAction selected {filenames=}')

def close_main():
    res = askyesnocancel(title=f"Quit {APP_NAME}", message="Are you sure?")
    if res:
        root.destroy()

def key_pressed(event):
    key = event.char
    logging.debug(f"key_pressed: {key=}")
    if key.lower() == 'q':
        close_main()

def get_args():
    parser = argparse.ArgumentParser(f"Argument Parser for {APP_NAME}")
    parser.add_argument('--debug', action='store_true', help='Sets debug mode.')

    args = parser.parse_args()
    return args


if __name__ == '__main__':

    args = get_args()
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    root = create_root()

    upload_button = tk.Button(root, text='Upload Image(s)', command=UploadAction)
    upload_button.pack()
    upload_button.place(relx=0.5, rely=0.5, anchor='center')


    root.bind('<Key>', key_pressed)
    root.mainloop()
