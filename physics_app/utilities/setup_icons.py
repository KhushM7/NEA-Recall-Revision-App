from PIL import ImageTk
from pytablericons import TablerIcons, OutlineIcon
import customtkinter as ctk


def setup_info_icon():
    icon_info_size = 24
    load_icon_info = TablerIcons.load(
        OutlineIcon.INFO_CIRCLE, icon_info_size, color="#000", stroke_width=1.6
    )
    icon_info = ctk.CTkImage(light_image=load_icon_info)
    return icon_info, icon_info_size
