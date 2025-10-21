import tkinter as tk

def press(key):
    entry_var.set(entry_var.get() + str(key))

def equal():
    try:
        expr = entry_var.get()
        if expr.strip() == "":
            return
        result = str(eval(expr))
        entry_var.set(result)
    except:
        entry_var.set("Error")

def clear():
    entry_var.set("")

root = tk.Tk()
root.title("Simple Calculator")
root.geometry("320x450")
root.resizable(True, True)

entry_var = tk.StringVar()

entry = tk.Entry(root, textvariable=entry_var, font=('Helvetica', 24), bd=5, relief=tk.RIDGE, justify='right')
entry.grid(row=0, column=0, columnspan=4, pady=20, padx=10, ipadx=5, ipady=10)

buttons = [
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['0', '.', '=', '+'],
]

for i, row in enumerate(buttons, start=1):
    for j, button in enumerate(row):
        color = 'orange' if button in ['/', '*', '-', '+', '='] else 'lightgray'
        fg_color = 'white' if color == 'orange' else 'black'
        action = equal if button == '=' else lambda key=button: press(key)
        b = tk.Button(root, text=button, font=('Helvetica', 20), bg=color, fg=fg_color, command=action, bd=1, relief=tk.RAISED)
        b.grid(row=i, column=j, sticky='nsew', padx=5, pady=5, ipadx=5, ipady=15)

clear_button = tk.Button(root, text='C', font=('Helvetica', 20), bg='red', fg='white', command=clear)
clear_button.grid(row=5, column=0, columnspan=4, sticky='nsew', padx=5, pady=10, ipady=15)

for i in range(5):
    root.grid_rowconfigure(i, weight=1)
for j in range(4):
    root.grid_columnconfigure(j, weight=1)

root.mainloop()
