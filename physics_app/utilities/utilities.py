import tkinter as tk
from ctypes import windll


def make_widget_transparent(widget: tk.Widget, colorkey: int = 0x00030201):
    hwnd = widget.winfo_id()
    wnd_exstyle = windll.user32.GetWindowLongA(hwnd, -20)  # GWL_EXSTYLE
    new_exstyle = wnd_exstyle | 0x00080000  # WS_EX_LAYERED
    windll.user32.SetWindowLongA(hwnd, -20, new_exstyle)  # GWL_EXSTYLE
    windll.user32.SetLayeredWindowAttributes(
        hwnd, colorkey, 255, 0x00000001
    )  # LWA_COLORKEY = 0x00000001
