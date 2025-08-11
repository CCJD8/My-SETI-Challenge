# Budget tracker and push it to GitHub
# To do: 
# - add compound interest every day
# - host the database csv on raspberry pi

import pandas as pd
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


def edit_balance(*args):
    """Edit the current balance according to the amount withdrawn."""
    try:
        withdrawal = float(withdraw_entry.get())
        balance = float(current_balance.get())
        current_balance.set(balance-withdrawal)
    except Exception:  # General Exception used to catch all exceptions apart from keyboard interrupts
        error_message()


def save_balance(*args):
    """Save the current balance to the CSV with pandas."""
    balance = float(current_balance.get())
    database.iloc[0,0] = balance
    database.to_csv(database_path, index=False)
    messagebox.showinfo("Saved", "New balance saved and confirmed")


def error_message():
    """Display a default error message."""
    messagebox.showerror("Error", "Something went wrong...")



# Load in details from CSV with pandas
database_path = "C:\\Users\\Connor\\Documents\\Nebuchadnezzar\\Learning\\Python\\database.csv"
database = pd.read_csv(database_path)
balance = database.iloc[0,0]

# Create main window with tkinter
root = tk.Tk()
root.title("Bank Account")

# Style the main window
style = ttk.Style()
style.theme_use("clam")
style.configure("my_style", font="helvetica 24", foreground="blue")

# Create a frame in the parent widget[the root main window]
# Position a widget[the mainframe frame] in the parent widget[the root main 
# window] in a grid.
mainframe = ttk.Frame(root, padding=(3,3,12,12), borderwidth=40, relief='groove')
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))

# Configure column and row index of the grid
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Add entry object in grid for withdrawals
withdraw_amount = tk.StringVar()
withdraw_entry = ttk.Entry(mainframe, width=10, textvariable=withdraw_amount)
withdraw_entry.grid(column=1, row=2)

# Add withdrawal submit button
button_withdraw = ttk.Button(mainframe, text="Withdraw", command=edit_balance)
button_withdraw.grid(column=2, row=2)

# Add balance display
current_balance = tk.StringVar(value=balance)
ttk.Label(mainframe, textvariable=current_balance).grid(column=5, row=3)

# Add confirm and save button
button_save = ttk.Button(mainframe, text="Confirm", command=save_balance)
button_save.grid(column=6, row=6)

# Create padding. Loop through all widgets which are children of the mainframe
# parent, then add padding to each
for child in mainframe.winfo_children():
    child.grid_configure(padx=30, pady=30)

# Bind the return/enter key to run the function display_balance. This passes 
# an event argument to the function which we set to None since we don't 
# require it
root.bind("<Return>", edit_balance)

root.mainloop()