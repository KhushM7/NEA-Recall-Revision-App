import customtkinter

app = customtkinter.CTk()

app.columnconfigure(0, weight=1)

notebook = customtkinter.CTkTabview(app)
notebook.add("Tab1")
notebook.add("Tab2")
notebook.grid(padx=10, pady=10)
notebook._segmented_button.grid(sticky="W")

app.mainloop()
