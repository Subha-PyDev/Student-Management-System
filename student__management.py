import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Database Setup
def init_db():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            course TEXT NOT NULL,
            marks INTEGER
        )
    """)
    conn.commit()
    conn.close()

# Function to Add Student
def add_student():
    name = name_entry.get()
    age = age_entry.get()
    course = course_entry.get()
    marks = marks_entry.get()

    if name and age and course and marks:
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, age, course, marks) VALUES (?, ?, ?, ?)", 
                       (name, age, course, marks))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Student added successfully!")
        view_students()
        clear_entries()
    else:
        messagebox.showwarning("Warning", "All fields are required!")

# Function to View Students
def view_students():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()

    student_table.delete(*student_table.get_children())
    for row in rows:
        student_table.insert("", tk.END, values=row)

# Function to Update Student
def update_student():
    selected_item = student_table.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a student to update!")
        return

    student_id = student_table.item(selected_item)["values"][0]
    name = name_entry.get()
    age = age_entry.get()
    course = course_entry.get()
    marks = marks_entry.get()

    if name and age and course and marks:
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE students SET name=?, age=?, course=?, marks=? WHERE id=?", 
                       (name, age, course, marks, student_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Student updated successfully!")
        view_students()
        clear_entries()
    else:
        messagebox.showwarning("Warning", "All fields are required!")

# Function to Delete Student
def delete_student():
    selected_item = student_table.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a student to delete!")
        return

    student_id = student_table.item(selected_item)["values"][0]
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Student deleted successfully!")
    view_students()

# Function to Search Student
def search_student():
    search_term = search_entry.get()
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE name LIKE ?", ('%' + search_term + '%',))
    rows = cursor.fetchall()
    conn.close()

    student_table.delete(*student_table.get_children())
    for row in rows:
        student_table.insert("", tk.END, values=row)

# Function to Clear Input Fields
def clear_entries():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)
    marks_entry.delete(0, tk.END)

# Initialize Database
init_db()

# GUI Setup
root = tk.Tk()
root.title("Student Management System")
root.geometry("700x500")
root.configure(bg="#f2f2f2")

# Labels & Entry Fields
tk.Label(root, text="Name", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
name_entry = tk.Entry(root, width=20, font=("Arial", 12))
name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Age", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
age_entry = tk.Entry(root, width=20, font=("Arial", 12))
age_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Course", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5)
course_entry = tk.Entry(root, width=20, font=("Arial", 12))
course_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Marks", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5)
marks_entry = tk.Entry(root, width=20, font=("Arial", 12))
marks_entry.grid(row=3, column=1, padx=10, pady=5)

# Buttons
tk.Button(root, text="Add Student", font=("Arial", 12), bg="#4CAF50", fg="white", command=add_student).grid(row=4, column=0, padx=10, pady=5)
tk.Button(root, text="Update Student", font=("Arial", 12), bg="#2196F3", fg="white", command=update_student).grid(row=4, column=1, padx=10, pady=5)
tk.Button(root, text="Delete Student", font=("Arial", 12), bg="#f44336", fg="white", command=delete_student).grid(row=4, column=2, padx=10, pady=5)
tk.Button(root, text="View All", font=("Arial", 12), bg="#FFC107", fg="black", command=view_students).grid(row=4, column=3, padx=10, pady=5)

# Search Bar
tk.Label(root, text="Search by Name:", font=("Arial", 12)).grid(row=5, column=0, padx=10, pady=5)
search_entry = tk.Entry(root, width=20, font=("Arial", 12))
search_entry.grid(row=5, column=1, padx=10, pady=5)
tk.Button(root, text="Search", font=("Arial", 12), bg="#9C27B0", fg="white", command=search_student).grid(row=5, column=2, padx=10, pady=5)

# Student Table
columns = ("ID", "Name", "Age", "Course", "Marks")
student_table = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    student_table.heading(col, text=col)
    student_table.column(col, width=100)

student_table.grid(row=6, column=0, columnspan=4, padx=10, pady=10)

# Start GUI
view_students()  # Load existing students
root.mainloop()