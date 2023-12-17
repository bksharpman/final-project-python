# todo_app.py
import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To do app")

        # Connect to SQLite database
        self.conn = sqlite3.connect("todo_db.db")
        self.create_table()

        self.task_entry = tk.Entry(root, width=40)
        self.task_entry.pack(pady=10)

        self.date_label = tk.Label(root, text="Date:")
        self.date_label.pack()

        self.date_entry = tk.Entry(root, width=40)
        self.date_entry.pack(pady=10)
        self.date_entry.insert(0, self.get_current_date())

        self.add_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.pack()

        self.task_listbox = tk.Listbox(root, width=50, height=10)
        self.task_listbox.pack(pady=10)

        self.complete_button = tk.Button(root, text="End", command=self.complete_task)
        self.complete_button.pack()

        self.delete_button = tk.Button(root, text="Delete", command=self.delete_task)
        self.delete_button.pack()

        self.priority_label = tk.Label(root, text="Priority:")
        self.priority_label.pack()

        self.priority_var = tk.StringVar()
        self.priority_var.set("Red")
        self.priority_radio_red = tk.Radiobutton(root, text="Red", variable=self.priority_var, value="Red", command=self.update_task_listbox)
        self.priority_radio_yellow = tk.Radiobutton(root, text="Yellow", variable=self.priority_var, value="Yellow", command=self.update_task_listbox)
        self.priority_radio_green = tk.Radiobutton(root, text="Green", variable=self.priority_var, value="Green", command=self.update_task_listbox)
        self.priority_radio_red.pack()
        self.priority_radio_yellow.pack()
        self.priority_radio_green.pack()

        self.menu = tk.Menu(root)
        self.root.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Save", command=self.save_tasks)
        self.file_menu.add_command(label="Upload", command=self.load_tasks)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)

        self.about_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="About", menu=self.about_menu)
        self.about_menu.add_command(label="Info", command=self.show_about_info)

        # Update task listbox initially
        self.update_task_listbox()

    def create_table(self):
        # Create a table if not exists
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    date TEXT,
                    priority TEXT
                )
            ''')

    def add_task(self):
        task = self.task_entry.get()
        date = self.date_entry.get() or self.get_current_date()
        priority = self.priority_var.get()

        if task:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute('''
                    INSERT INTO tasks (task, date, priority)
                    VALUES (?, ?, ?)
                ''', (task, date, priority))

            self.update_task_listbox()
            self.task_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, self.get_current_date())

    def update_task_listbox(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT * FROM tasks ORDER BY priority
            ''')
            tasks = cursor.fetchall()

        self.task_listbox.delete(0, tk.END)
        for task_data in tasks:
            task = task_data[1]
            priority = task_data[3]
            self.task_listbox.insert(tk.END, f"({priority}) {task}")

    def complete_task(self):
        selected_priority = self.priority_var.get()
        selected_task_index = self.task_listbox.curselection()

        if selected_task_index:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute('''
                    DELETE FROM tasks WHERE id=?
                ''', (selected_task_index[0] + 1,))  # SQLite uses 1-based index

            self.update_task_listbox()

    def delete_task(self):
        selected_priority = self.priority_var.get()
        selected_task_index = self.task_listbox.curselection()

        if selected_task_index:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute('''
                    DELETE FROM tasks WHERE id=?
                ''', (selected_task_index[0] + 1,))  # SQLite uses 1-based index

            self.update_task_listbox()

    def save_tasks(self):
        # Saving tasks is not required for SQLite as it's persistent
        messagebox.showinfo("Saved", "To do list saved")

    def load_tasks(self):
        # Loading tasks is not required for SQLite as it's persistent
        messagebox.showinfo("Uploaded", "To do list uploaded")

    def show_about_info(self):
        about_text = "To do app\n\n"
        about_text += "This app helps prioritize your tasks\n"
        about_text += "Tasks are divided by 3 colors\n\n"
        about_text += "• Red list - very important tasks\n"
        about_text += "• Yellow list - about important tasks\n"
        about_text += "• Green list - not very important tasks\n\n"
        about_text += "Select the color of the task using the buttons. If you do not specify the date,\n"
        about_text += "then the current date will be used automatically.\n"
        about_text += "You can Save and Upload the tasks list\n\n"
        about_text += "Authors: Bokeikhan, Edige \n"
        about_text += "Date: " + datetime.now().strftime("%d.%m.%Y")

        messagebox.showinfo("About", about_text)

    def get_current_date(self):
        return datetime.now().strftime("%Y-%m-%d")

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
