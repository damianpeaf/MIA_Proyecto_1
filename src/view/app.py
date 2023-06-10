from tkinter import (
    filedialog,
    Menu,
    Frame,
    messagebox,
    Text,
    Tk,
    ttk,
)

from utils.screen import get_window_position

# Create a new window


class App(ttk.Frame):

    # Size of the window
    APP_WIDTH: int = 1400
    APP_HEIGHT: int = 700

    def __init__(self) -> None:
        super().__init__()

        # Create the window
        self.master.title("Proyecto 1 - Grupo 6")
        self.master.geometry(get_window_position(self.master.winfo_screenwidth(
        ), self.master.winfo_screenheight(), self.APP_WIDTH, self.APP_HEIGHT))

    def create_widgets(self) -> None:
        pass
