import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("640x480")

app.title("Max Payne FSM Editor v0.1.0")


def openMPLDBFile():
    print("button pressed")


button = ctk.CTkButton(master=app, text="Open Max Payne 1 LDB (Game Level) File", command=openMPLDBFile)
button.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

app.mainloop()
