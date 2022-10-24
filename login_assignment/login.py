import tkinter as tk
import tkinter.messagebox as mb
import mysql.connector
import re
from tkinter import ttk
""" connecting to the database using 'connect()'  method
## it takes 3 required parameters 'host', 'user', 'password' """
"""In the above code snippet reader should change user and password to his username and password to connect to MySQL Database Server.  
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -Login.py-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --  """

""" Connecting to the database## importing 'mysql.connector'  
##for connection to mysql database """
db_connection = mysql.connector.connect(host="localhost", user="root", password="mysql#2022")
# creating database_cursor to perform SQL operation
db_cursor = db_connection.cursor(buffered=True)
# Using Toplevel widget to create a new window named RegisterWindow to register a new user
class RegisterWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.original_frame = parent
        self.geometry("600x450+485+162")
        self.title("Register")
        self.configure(background="#ff80ff")
        self.lblRegister = tk.Label(self, text="Register", font=("Helvetica", 16), bg="yellow", fg="blue")
        self.lblUId = tk.Label(self, text="Enter UserId:", font=("Helvetica", 10), bg="blue", fg="yellow")
        self.lblPwd = tk.Label(self, text="Enter Password:", font=("Helvetica", 10), bg="blue", fg="yellow")
        self.txtUId = tk.Entry(self)
        self.txtPwd = tk.Entry(self)
        self.btn_register = tk.Button(self, text="Register", font=("Helvetica", 11), bg="yellow", fg="blue",
                                      command=self.registering)
        self.btn_cancel = tk.Button(self, text="<-Back", font=("Helvetica", 11), bg="yellow", fg="blue",
                                    command=self.onClose)
        self.lblRegister.place(relx=0.467, rely=0.111, height=21, width=100)
        self.lblUId.place(relx=0.355, rely=0.333, height=21, width=78)
        self.lblPwd.place(relx=0.319, rely=0.4, height=21, width=100)
        self.txtUId.place(relx=0.490, rely=0.333, height=20, relwidth=0.223)
        self.txtPwd.place(relx=0.490, rely=0.4, height=20, relwidth=0.223)
        self.btn_register.place(relx=0.500, rely=0.660, height=24, width=63)
        self.btn_cancel.place(relx=0.605, rely=0.660, height=24, width=54)

    def registering(self):
        if not db_connection.is_connected():
            db_connection.connect()
            # executing cursor with execute method and pass SQL query
            db_cursor.execute("CREATE DATABASE IF NOT EXISTS User")  # Create a Database
            db_cursor.execute("use User")  # Interact with Database# creating required tables
            db_cursor.execute(
                "Create table if not exists USER(uid VARCHAR(30) NOT NULL PRIMARY KEY,password VARCHAR(30))")
            db_connection.commit()
        uid = self.txtUId.get()  # Retrieving entered user id
        pwd = self.txtPwd.get()  # Retrieving entered password
        if uid == "":
            mb.showinfo('Information', "Please Enter User Id")
            self.txtUId.focus_set()
            return
        if pwd == "":
            mb.showinfo('Information', "Please Enter Password")
            self.txtPwd.focus_set()
            return
        pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.match(pat, uid):
            mb.showinfo('Information', "Enter Valid Email")
            self.txtUId.focus_set()
            return
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{5,16}$"
        if not re.match(reg, pwd):
            mb.showinfo('Information', "Enter Valid Password")
            self.txtPwd.focus_set()
            return
        # Inserting record into table of  database
        db_cursor.execute("use User")  # Interact with  Database
        print(uid, pwd)
        query = "INSERT INTO user(uid,password) VALUES (%s,%s)"
        val = (uid, pwd)
        try:
            # implement sql Sentence
            db_cursor.execute(query, val)
            mb.showinfo('Information', "Data inserted Successfully")  # Submit to database for execution
            db_connection.commit()
        except:
            mb.showinfo('Information', "Data insertion failed!!!")  # Rollback in case there is any error
            db_connection.rollback()  # Close database connection
            db_connection.close()

    def onClose(self):
        self.destroy()
        self.original_frame.show()


class LoginApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("600x450+351+174")
        self.configure(bg="#ff8040")
        self.lblHeading = tk.Label(self, text="Login", font=("Helvetica", 16), bg="yellow", fg="blue")
        self.lbluname = tk.Label(self, text="Enter UserName:", font=("Helvetica", 10), bg="blue", fg="yellow")
        self.lblpsswd = tk.Label(self, text="Enter Password:", font=("Helvetica", 10), bg="blue", fg="yellow")
        self.txtuname = tk.Entry(self, width=60)
        self.txtpasswd = tk.Entry(self, width=60, show="*")
        self.btn_login = tk.Button(self, text="Login", font=("Helvetica", 11), bg="yellow", fg="blue",
                                   command=self.login)
        self.btn_clear = tk.Button(self, text="Clear", font=("Helvetica", 11), bg="yellow", fg="blue",
                                   command=self.clear_form)
        self.btn_forgot_pwd = tk.Button(self, text="Forgot Password", font=("Helvetica", 11), bg="yellow", fg="blue",
                                        command=self.forgot_password)
        self.btn_register = tk.Button(self, text="NewUser!Register", font=("Helvetica", 11), bg="yellow", fg="blue",
                                      command=self.open_registration_window)
        self.btn_exit = tk.Button(self, text="Exit", font=("Helvetica", 16), bg="yellow", fg="blue", command=self.exit)
        self.lblHeading.place(relx=0.35, rely=0.089, height=41, width=174)
        self.lbluname.place(relx=0.235, rely=0.289, height=21, width=106)
        self.lblpsswd.place(relx=0.242, rely=0.378, height=21, width=102)
        self.txtuname.place(relx=0.417, rely=0.289, height=20, relwidth=0.273)
        self.txtpasswd.place(relx=0.417, rely=0.378, height=20, relwidth=0.273)
        self.btn_login.place(relx=0.45, rely=0.489, height=24, width=52)
        self.btn_clear.place(relx=0.54, rely=0.489, height=24, width=72)
        self.btn_register.place(relx=0.695, rely=0.489, height=24, width=175)
        self.btn_forgot_pwd.place(relx=0.55, rely=0.6, height=24, width=175)
        self.btn_exit.place(relx=0.75, rely=0.911, height=24, width=61)

    def open_registration_window(self):
        self.withdraw()
        window = RegisterWindow(self)
        window.grab_set()

    def open_login_success_window(self):
        self.withdraw()
        window = Login_Success_Window(self)
        window.grab_set()

    def show(self):
        self.update()
        self.deiconify()

    def login(self):
        if not db_connection.is_connected():
            db_connection.connect()  # executing cursor with execute method and pass SQL query
            db_cursor.execute("CREATE DATABASE IF NOT EXISTS User")  # Create a Database
            db_cursor.execute("use User")  # Interact with  Database# creating required tables
            db_cursor.execute(
                "create table if not exists USER(uid VARCHAR(30) NOT NULL PRIMARY KEY,password VARCHAR(30))")
            db_connection.commit()
        try:
            username = str(self.txtuname.get())  # Retrieving entered username
            passwd = str(self.txtpasswd.get())  # Retrieving entered password
            if username == "":
                mb.showinfo('Information', "Please Enter Username")
                self.txtuname.focus_set()
                return
            if passwd == "":
                mb.showinfo('Information', "Please Enter Password")
                self.txtpasswd.focus_set()
                return
            print(username)
            print(passwd)
            query = "SELECT * FROM User WHERE uid = '" + username + "' AND password = '" + passwd + "'"
            print(query)  # implement sql Sentence
            db_cursor.execute(query)
            rowcount = db_cursor.rowcount
            print(rowcount)
            if db_cursor.rowcount == 1:
                mb.showinfo('Information', "Login Successfully")
            else:
                mb.showinfo('Information', "Login failed,Invalid Username or Password.Try again!!!")
        except:  # Closing Connection
            db_connection.disconnect()

    def clear_form(self):
        self.txtuname.delete(0, tk.END)
        self.txtpasswd.delete(0, tk.END)
        self.txtuname.focus_set()

    def forgot_password(self):
        if not db_connection.is_connected():
            db_connection.connect()
        try:
            username = str(self.txtuname.get())  # Retrieving entered username
            if username == "":
                mb.showinfo('Information', "Please Enter Username")
                self.txtuname.focus_set()
                return
            query = "select password from user.user where uid='" + username + "'"
            db_cursor.execute(query)
            password = db_cursor.fetchone()
            rowcount = db_cursor.rowcount
            if db_cursor.rowcount == 1:
                mb.showinfo('Information', "Password Found ")
                win = tk.Tk()
                win.geometry("750x250")
                Cdd=tk.Label(win, text=password, font=('Century 15 bold')).pack(pady=20)
                button = ttk.Button(win, text="Your Password", command=Cdd)
                button.pack()
                win.mainloop()
            else:
                mb.showinfo("Information", "No such username")

        except:
            mb.showinfo('Information', "Username not found")
            db_connection.rollback()  # Close database connection
            db_connection.close()

    def exit(self):
        MsgBox = mb.askquestion('Exit Application', 'Are you sure you want to exit the application', icon='warning')
        if MsgBox == 'yes':
            self.destroy()


if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
