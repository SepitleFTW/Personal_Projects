import tkinter as tk
from tkinter import messagebox
import sqlite3
import pyotp

# Initialize the database
def init_db():
    conn = sqlite3.connect('password_manager.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, otp_secret TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS passwords (id INTEGER PRIMARY KEY, user_id INTEGER, service TEXT, username TEXT, password TEXT)''')
    conn.commit()
    conn.close()

# GUI Application class
class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")

        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        self.label = tk.Label(self.frame, text="Welcome to Password Manager")
        self.label.grid(row=0, column=0, columnspan=2)

        self.login_button = tk.Button(self.frame, text="Login", command=self.show_login)
        self.login_button.grid(row=1, column=0)

        self.register_button = tk.Button(self.frame, text="Register", command=self.show_register)
        self.register_button.grid(row=1, column=1)

    def show_login(self):
        LoginWindow(self.root)

    def show_register(self):
        RegisterWindow(self.root)

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(root)
        self.window.title("Login")

        self.frame = tk.Frame(self.window)
        self.frame.pack(pady=10)

        self.username_label = tk.Label(self.frame, text="Username:")
        self.username_label.grid(row=0, column=0)
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.grid(row=0, column=1)

        self.password_label = tk.Label(self.frame, text="Password:")
        self.password_label.grid(row=1, column=0)
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.grid(row=1, column=1)

        self.login_button = tk.Button(self.frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Authenticate user
        conn = sqlite3.connect('password_manager.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, otp_secret FROM users WHERE username=? AND password=?', (username, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            user_id, otp_secret = result
            otp = pyotp.TOTP(otp_secret)
            otp_code = otp.now()
            messagebox.showinfo("2FA Code", f"Your 2FA code is: {otp_code}")
            self.window.destroy()
            PasswordManager(user_id, self.root)
        else:
            messagebox.showerror("Error", "Invalid credentials")

class RegisterWindow:
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(root)
        self.window.title("Register")

        self.frame = tk.Frame(self.window)
        self.frame.pack(pady=10)

        self.username_label = tk.Label(self.frame, text="Username:")
        self.username_label.grid(row=0, column=0)
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.grid(row=0, column=1)

        self.password_label = tk.Label(self.frame, text="Password:")
        self.password_label.grid(row=1, column=0)
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.grid(row=1, column=1)

        self.register_button = tk.Button(self.frame, text="Register", command=self.register)
        self.register_button.grid(row=2, column=0, columnspan=2)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        otp_secret = pyotp.random_base32()

        # Register user
        conn = sqlite3.connect('password_manager.db')
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password, otp_secret) VALUES (?, ?, ?)', (username, password, otp_secret))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful")
            self.window.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        conn.close()

class PasswordManager:
    def __init__(self, user_id, root):
        self.user_id = user_id
        self.root = root
        self.window = tk.Toplevel(root)
        self.window.title("Password Manager")

        self.frame = tk.Frame(self.window)
        self.frame.pack(pady=10)

        self.service_label = tk.Label(self.frame, text="Service:")
        self.service_label.grid(row=0, column=0)
        self.service_entry = tk.Entry(self.frame)
        self.service_entry.grid(row=0, column=1)

        self.username_label = tk.Label(self.frame, text="Username:")
        self.username_label.grid(row=1, column=0)
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.grid(row=1, column=1)

        self.password_label = tk.Label(self.frame, text="Password:")
        self.password_label.grid(row=2, column=0)
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.grid(row=2, column=1)

        self.add_button = tk.Button(self.frame, text="Add", command=self.add_password)
        self.add_button.grid(row=3, column=0, columnspan=2)

        self.password_list = tk.Listbox(self.frame)
        self.password_list.grid(row=4, column=0, columnspan=2)

        self.load_passwords()

    def add_password(self):
        service = self.service_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = sqlite3.connect('password_manager.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO passwords (user_id, service, username, password) VALUES (?, ?, ?, ?)', (self.user_id, service, username, password))
        conn.commit()
        conn.close()

        self.service_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.load_passwords()

    def load_passwords(self):
        self.password_list.delete(0, tk.END)
        conn = sqlite3.connect('password_manager.db')
        cursor = conn.cursor()
        cursor.execute('SELECT service, username, password FROM passwords WHERE user_id=?', (self.user_id,))
        passwords = cursor.fetchall()
        conn.close()

        for pwd in passwords:
            self.password_list.insert(tk.END, f"Service: {pwd[0]}, Username: {pwd[1]}, Password: {pwd[2]}")

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()
