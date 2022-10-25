import tkinter as tk

window = tk.Tk()

window.title("ViTalk")
window.geometry("500x400")
window.resizable(width=False, height=False)

container = tk.Frame()

label_username = tk.Label(window, text="username")
entry_username = tk.Entry(window)
btn_login = tk.Button(text='Login')

label_username.pack()
entry_username.pack()
btn_login.pack()
container.pack()


window.mainloop()