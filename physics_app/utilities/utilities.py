import customtkinter as ctk
from PIL import Image, ImageTk
from typing import Tuple


def configure_grid(frame: ctk.CTkFrame, rows: int, columns: int) -> None:
    """Configures grid layout for a given frame.
    :rtype: object
    """
    for i in range(rows):
        frame.grid_rowconfigure(i, weight=1)
    for i in range(columns):
        frame.grid_columnconfigure(i, weight=1)


def resize_and_update_image(
    image: Image.Image,
    canvas: ctk.CTkCanvas,
    canvas_size: Tuple[int, int],
    scale_factor: float = 1.5,
) -> None:
    """
    Resize an image to fit within the canvas size while maintaining aspect ratio,
    and update the canvas with the resized image.

    :param image: The original PIL Image to resize.
    :param canvas: The canvas widget to display the image.
    :param canvas_size: The size (width, height) of the canvas.
    :param scale_factor: Factor to scale down the width of the image.
    """
    width, height = canvas_size
    new_width = int(width / scale_factor)
    new_height = int((image.height / image.width) * new_width)

    if new_height > height:
        new_height = height
        new_width = int(new_height / (image.height / image.width))

    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    image_tk = ImageTk.PhotoImage(resized_image)

    # Clear the canvas and update with the resized image
    canvas.delete("all")
    canvas.create_image(width // 2, height // 2, image=image_tk, anchor="center")

    # Keep a reference to avoid garbage collection
    canvas.image_tk = image_tk
