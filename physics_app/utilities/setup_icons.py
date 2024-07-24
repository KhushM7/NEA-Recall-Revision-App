from pytablericons import TablerIcons, OutlineIcon
import customtkinter as ctk


def setup_info_icon():
    icon_info_size = 24
    load_icon_info = TablerIcons.load(
        OutlineIcon.INFO_CIRCLE, icon_info_size, color="#000", stroke_width=2
    )
    icon_info = ctk.CTkImage(light_image=load_icon_info)
    return icon_info, icon_info_size


def setup_error_icon():
    icon_error_size = 24
    load_icon_error = TablerIcons.load(
        OutlineIcon.EXCLAMATION_CIRCLE,
        icon_error_size,
        color="#d74141",
        stroke_width=2,
    )
    icon_error = ctk.CTkImage(light_image=load_icon_error)
    return icon_error, icon_error_size


def setup_close_icon():
    close_icon_size = 24
    load_close_icon = TablerIcons.load(
        OutlineIcon.X, close_icon_size, color="#000000", stroke_width=2
    )
    close_icon = ctk.CTkImage(light_image=load_close_icon)
    return close_icon, close_icon_size
