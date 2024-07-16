import tkinter as tk


class PhysicsApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")
        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        self.message = "Hi there, everyone!"
        print(self.message)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Physics App")
    root.state("zoomed")

    app = PhysicsApp(master=root)
    app.pack(expand=True, fill="both")

    root.mainloop()
