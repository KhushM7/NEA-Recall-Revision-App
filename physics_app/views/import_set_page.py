import os
from tkinter import messagebox
import xlwings as xw
import customtkinter as ctk

from physics_app.utilities.server_utilities.flashcard_handler import FlashcardHandler


class ImportSetPage(ctk.CTkToplevel):
    def __init__(self, parent, user_id):
        super().__init__(parent)
        self.flashcard_handler = FlashcardHandler(server_url="http://127.0.0.1:5000")
        self.user_id = user_id
        self.title("Import Flashcard Set")
        self.geometry("500x600")
        self.grab_set()  # Prevents interaction with parent window
        self.transient(parent)  # Links it to the parent window

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.label_title = ctk.CTkLabel(
            self, text="Import Flashcard Set", font=("Arial", 16)
        )
        self.label_title.grid(row=0, column=0, pady=(10, 20), sticky="n")

        self.label_instructions = ctk.CTkLabel(
            self,
            text=(
                "Please upload an Excel file with the following format:\n"
                "- The first column is the front of the card\n"
                "- The second column is the back of the card\n"
                "Ensure no blank rows and no additional columns are present."
            ),
            wraplength=400,
            justify="left",
        )
        self.label_instructions.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="w")

        self.button_choose_file = ctk.CTkButton(
            self, text="Choose File", command=self.choose_file
        )
        self.button_choose_file.grid(row=2, column=0, padx=20, pady=(10, 20))

        self.label_set_name = ctk.CTkLabel(self, text="Set Name:")
        self.label_set_name.grid(row=3, column=0, padx=20, sticky="w")

        self.entry_set_name = ctk.CTkEntry(self, placeholder_text="Enter set name here")
        self.entry_set_name.grid(row=4, column=0, padx=20, pady=(5, 15), sticky="ew")

        self.label_file_contents = ctk.CTkLabel(self, text="File Contents:")
        self.label_file_contents.grid(row=5, column=0, padx=20, sticky="w")

        self.textbox_file_contents = ctk.CTkTextbox(self, width=400, height=200)
        self.textbox_file_contents.grid(
            row=6, column=0, padx=20, pady=(5, 15), sticky="ew"
        )

        self.button_save = ctk.CTkButton(self, text="Save", command=self.save_set)
        self.button_save.grid(row=7, column=0, padx=20, pady=(15, 20))

        self.selected_file = None

    def choose_file(self):
        filetypes = [("Excel files", "*.xlsx *.xls")]
        filepath = ctk.filedialog.askopenfilename(
            title="Open File", filetypes=filetypes
        )

        if filepath:
            self.selected_file = filepath
            file_name = os.path.splitext(os.path.basename(filepath))[0]
            self.entry_set_name.insert("end", file_name)
            try:
                # Read the Excel file using xlwings
                with xw.App(visible=False) as app:
                    wb = app.books.open(filepath)
                    sheet = wb.sheets[0]
                    data = sheet.used_range.value

                # Validate format: should have exactly 2 columns
                if any(len(row) != 2 for row in data):
                    raise ValueError(
                        "Invalid format: File must have exactly two columns."
                    )

                # Clear the textbox and display contents
                self.textbox_file_contents.delete("1.0", "end")
                for row in data:
                    front, back = row
                    self.textbox_file_contents.insert(
                        "end", f"Front: {front}\nBack: {back}\n---\n"
                    )

            except Exception as e:
                messagebox.showerror("File Error", f"Error reading file: {e}")
                self.textbox_file_contents.delete("1.0", "end")
                self.textbox_file_contents.insert(
                    "1.0", "Error: Unable to display file contents."
                )
        else:
            messagebox.showwarning("No File Selected", "Please select a file.")

    def save_set(self):
        set_name = self.entry_set_name.get()
        if not set_name:
            messagebox.showerror("Set Name Missing", "Please enter a set name.")
            return

        file_contents = self.textbox_file_contents.get("1.0", "end").strip()
        if not file_contents:
            messagebox.showerror(
                "No Content", "The file contents are empty. Please check and try again."
            )
            return

        flashcards = []
        try:
            # Parse the contents of the textbox
            for block in file_contents.split("---\n"):
                lines = block.strip().split("\n")
                if len(lines) >= 2:
                    front = lines[0].replace("Front: ", "", 1).strip()
                    back = lines[1].replace("Back: ", "", 1).strip()
                    flashcards.append(
                        {"set_name": set_name, "front": front, "back": back}
                    )

            # Save each flashcard
            for card in flashcards:
                self.flashcard_handler.create_flashcard(self.user_id, card)

            messagebox.showinfo(
                "Save Successful", f"Flashcards for set '{set_name}' have been saved."
            )
            self.destroy()  # Close the window

        except Exception as e:
            messagebox.showerror("Save Error", f"Error saving flashcards: {e}")
