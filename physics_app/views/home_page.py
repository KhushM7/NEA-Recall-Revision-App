import tkinter as tk


class HomePage(tk.Frame):
    def __init__(self, master: tk.Frame, server_url: str):
        super().__init__(master)
        self.master = master
