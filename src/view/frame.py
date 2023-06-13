from tkinter import (
    ttk,
)

from utils.screen import get_window_position

# Create a new window


class Frame(ttk.Frame):

    def __init__(self, title: str, height: int, width: int, form_components: list[dict[str:str]]) -> None:
        super().__init__()
        self.height = height
        self.width = width

        # Create the window
        self.master.title(title)
        self.master.minsize(self.width, self.height)
        self.master.geometry(get_window_position(self.master.winfo_screenwidth(
        ), self.master.winfo_screenheight(), self.width, self.height))

        # Create the frame
        self.pack(fill='both', expand=False)

        # Create the form

        for component in form_components:
            self.create_component(component)

    def create_component(self, component: dict[str:str]) -> None:
        if component['type'] == 'label':
            ttk.Label(self, text=component['text']).grid(
                row=component['row'], column=component['column'])
        elif component['type'] == 'button':
            ttk.Button(self, text=component['text'], command=component['command']).grid(
                row=component['row'], column=component['column'])
        elif component['type'] == 'entry':
            ttk.Entry(self, textvariable=component['textvariable']).grid(
                row=component['row'], column=component['column'])
        elif component['type'] == 'combobox':
            ttk.Combobox(self, textvariable=component['textvariable'], values=component['values']).grid(
                row=component['row'], column=component['column'])
        elif component['type'] == 'checkbutton':
            ttk.Checkbutton(self, text=component['text'], variable=component['variable']).grid(
                row=component['row'], column=component['column'])
        elif component['type'] == 'radiobutton':
            ttk.Radiobutton(self, text=component['text'], variable=component['variable'], value=component['value']).grid(
                row=component['row'], column=component['column'])
        elif component['type'] == 'spinbox':
            ttk.Spinbox(self, textvariable=component['textvariable'], from_=component['from'], to=component['to']).grid(
                row=component['row'], column=component['column'])
        elif component['type'] == 'scale':
            ttk.Scale(self, variable=component['variable'], from_=component['from'], to=component['to']).grid(
                row=component['row'], column=component['column'])
        elif component['type'] == 'progressbar':
            ttk.Progressbar(self, variable=component['variable'], maximum=component['maximum']).grid(
                row=component['row'], column=component['column'])
        elif component['type'] == 'separator':
            ttk.Separator(self, orient=component['orient']).grid(
                row=component['row'], column=component['column'])
        elif component['type'] == 'sizegrip':
            ttk.Sizegrip(self).grid(
                row=component['row'], column=component['column'])
        elif component['type'] == 'treeview':
            ttk.Treeview(self, columns=component['columns']).grid(
                row=component['row'], column=component['column'])
        elif component['type'] == 'notebook':
            ttk.Notebook(self).grid(
                row=component['row'], column=component['column'])
        elif component['type'] == 'progress':
            ttk.Progressbar(self, orient=component['orient'], length=component['length'], mode=component['mode']).grid(
                row=component['row'], column=component['column'])
