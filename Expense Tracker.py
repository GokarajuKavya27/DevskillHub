#!/usr/bin/env python
# coding: utf-8

# In[2]:


import sqlite3
import pandas as pd
import tkinter as tk
from tkinter import messagebox

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")

    
        self.conn = sqlite3.connect("exp.db")
        self.cursor = self.conn.cursor()

       
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                date TEXT NOT NULL
            )
        ''')
        self.conn.commit()

        # Create GUI components
        self.category_label = tk.Label(root, text="Category:")
        self.amount_label = tk.Label(root, text="Amount:")
        self.date_label = tk.Label(root, text="Date (YYYY-MM-DD):")

        self.category_entry = tk.Entry(root)
        self.amount_entry = tk.Entry(root)
        self.date_entry = tk.Entry(root)

        self.add_button = tk.Button(root, text="Add Expense", command=self.add_expense)
        self.update_button = tk.Button(root, text="Update Expense", command=self.update_expense)
        self.delete_button = tk.Button(root, text="Delete Expense", command=self.delete_expense)
        self.report_button = tk.Button(root, text="Generate Monthly Report", command=self.generate_report)

        # Grid layout
        self.category_label.grid(row=0, column=0, padx=10, pady=10)
        self.amount_label.grid(row=1, column=0, padx=10, pady=10)
        self.date_label.grid(row=2, column=0, padx=10, pady=10)

        self.category_entry.grid(row=0, column=1, padx=10, pady=10)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=10)
        self.date_entry.grid(row=2, column=1, padx=10, pady=10)

        self.add_button.grid(row=3, column=0, columnspan=2, pady=10)
        self.update_button.grid(row=4, column=0, columnspan=2, pady=10)
        self.delete_button.grid(row=5, column=0, columnspan=2, pady=10)
        self.report_button.grid(row=6, column=0, columnspan=2, pady=10)

    def add_expense(self):
        category = self.category_entry.get()
        amount = self.amount_entry.get()
        date = self.date_entry.get()

        if category and amount and date:
            try:
                amount = float(amount)
                self.cursor.execute("INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)",
                                    (category, amount, date))
                self.conn.commit()
                messagebox.showinfo("Success", "Expense added successfully.")
                self.clear_entries()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount.")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def update_expense(self):
        category = self.category_entry.get()
        amount = self.amount_entry.get()
        date = self.date_entry.get()

        if category and amount and date:
            try:
                amount = float(amount)
                self.cursor.execute("UPDATE expenses SET amount = ?, date = ? WHERE category = ?",
                                    (amount, date, category))
                self.conn.commit()
                messagebox.showinfo("Success", "Expense updated successfully.")
                self.clear_entries()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount.")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def delete_expense(self):
        category = self.category_entry.get()

        if category:
            self.cursor.execute("DELETE FROM expenses WHERE category = ?", (category,))
            self.conn.commit()
            messagebox.showinfo("Success", "Expense deleted successfully.")
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Please enter a category to delete.")

    def generate_report(self):
        self.cursor.execute("SELECT  date,category,SUM(amount) FROM expenses GROUP BY date")
        data = self.cursor.fetchall()

        if not data:
            messagebox.showinfo("Info", "No data available for generating a report.")
            return

        df = pd.DataFrame(data, columns=[' date','category','Total Amount'])
        report_text = df.to_string(index=False)

        messagebox.showinfo("Monthly Expense Report", report_text)

    def clear_entries(self):
        self.category_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()


# In[ ]:




