import tkinter as tk
import socket 
import hashlib
import mysql.connector 

HOST = '127.0.0.1'
SERVER_POST = 65432
FORMAT = 'utf-8'
LOGIN = 'login'
FAIL = 'fail'
SUCCESS = 'success'

class StartPage(tk.Frame):
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)

        label_title = tk.Label(self, text="LOG IN")
        label_user = tk.Label(self, text="Username")
        label_password = tk.Label(self, text="Password")

        self.label_notice = tk.Label(self, text="", bg="bisque2")
        self.entry_user = tk.Entry(self, width=20, bg="light yellow")
        self.entry_password = tk.Entry(self, width=20, bg="light yellow")

        button_log = tk.Button(self, text='LOG IN', command=lambda: appController.logIn(self, client))
        button_log.configure(width=10)

        button_register = tk.Button(self, text='REGISTER', command=lambda: appController.showPage(RegisterPage))
        button_register.configure(width=10)

        label_title.pack()
        label_user.pack()
        self.entry_user.pack()
        label_password.pack()
        self.entry_password.pack()
        self.label_notice.pack()

        button_log.pack()
        button_register.pack()

class RegisterPage(tk.Frame):
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)

        label_title = tk.Label(self, text="LOG IN")
        label_user = tk.Label(self, text="Username")
        label_password = tk.Label(self, text="Password")
        label_cf_password = tk.Label(self, text="Confirm Password")

        self.label_notice = tk.Label(self, text="", bg="bisque2")
        self.entry_user = tk.Entry(self, width=40, bg="light yellow")
        self.entry_password = tk.Entry(self, width=40, bg="light yellow")
        self.entry_cf_password = tk.Entry(self, width=40, bg="light yellow")

        button_submit = tk.Button(self, text='REGISTER', command=lambda: appController.register(self))
        button_submit.configure(width=10)

        button_back = tk.Button(self, text='BACK', command=lambda: appController.showPage(StartPage))
        button_back.configure(width=10)

        label_title.pack()
        label_user.pack()
        self.entry_user.pack()
        label_password.pack()
        self.entry_password.pack()
        label_cf_password.pack()
        self.entry_cf_password.pack()
        self.label_notice.pack()

        button_submit.pack()
        button_back.pack()

class HomePage(tk.Frame):
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)

        label_title = tk.Label(self, text="HOME PAGE")

        self.label_notice = tk.Label(self, text="", bg="bisque2")
        btn_logout = tk.Button(self, text="LOG OUT", command=lambda: appController.showPage(StartPage))

        label_title.pack()
        btn_logout.pack()

class RoomPage(tk.Frame):
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)

        label_title = tk.Label(self, text="HOME PAGE")
        label_room = tk.Label(self, text="Join room")
        label_add_room = tk.Label(self, text="Create room")
        label_pin_room = tk.Label(self, text="PIN")

        self.label_notice = tk.Label(self, text="", bg="bisque2")
        self.entry_id_room = tk.Entry(self, width=40, bg="light yellow")
        self.entry_name_room = tk.Entry(self, width=40, bg="light yellow")
        self.entry_pin_room = tk.Entry(self, width=40, bg="light yellow")

        button_join_room = tk.Button(self, text='JOIN')
        button_join_room.configure(width=10)
        button_add_room = tk.Button(self, text='CREATE ROOM')
        button_add_room.configure(width=10)
        btn_logout = tk.Button(self, text="LOG OUT", command=lambda: appController.showPage(StartPage))

        label_title.pack()
        label_room.pack()
        self.entry_id_room.pack()
        label_add_room.pack()
        self.entry_name_room.pack()
        label_pin_room.pack()
        self.entry_pin_room.pack()
        self.label_notice.pack()

        button_join_room.pack()
        button_add_room.pack()
        btn_logout.pack()

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title("ViTalk")
        self.geometry("500x300")
        self.resizable(width=False, height=False)

        container = tk.Frame()
        container.configure(bg='red')

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage,RegisterPage, HomePage):
            frame = F(container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[F] = frame

        self.frames[StartPage].tkraise()
    
    def showPage(self, FrameClass):
        self.frames[FrameClass].tkraise()

    def logIn(self, curFrame, sck: socket):
        try:
            username = curFrame.entry_user.get()
            pswd = curFrame.entry_password.get()
            if username == "" or pswd=="":
                curFrame.label_notice["text"] = "Fields cannot be empty"
                return 
            # Send option
            option = LOGIN
            sck.sendall(option.encode(FORMAT))
            # Send account info
            sck.sendall(username.encode(FORMAT))
            # sck.recv(1024)
            
            sck.sendall(pswd.encode(FORMAT))
            # sck.recv(1024)
            # Recv login message
            msg = sck.recv(1024).decode(FORMAT)
            if(msg == SUCCESS):
                self.showPage(HomePage)
            else: 
                curFrame.label_notice['text'] = 'Invalid password'
                return
        except:
            print("Error: Server is not responding")

    def register(self, curFrame):
        try:
            username = curFrame.entry_user.get()
            password = curFrame.entry_password.get()
            cf_password = curFrame.entry_cf_password.get()
            if username == "" or password=="" or cf_password == "":
                curFrame.label_notice["text"] = "Fields cannot be empty"
                return 

            if password != cf_password:
                curFrame.label_notice["text"] = 'Password and confirm password is not match'
                return

            accepted = self.check_client_register(username)
            hashpass = hashlib.md5(password.encode(FORMAT)).hexdigest()
            if accepted:
                cursor.execute("INSERT INTO `account`(username, password) VALUES('%s', '%s')" % (username, hashpass))
                db.commit()
                curFrame.label_notice["text"] = "Create account successfully"
            else:
                curFrame.label_notice["text"] = "Username already exists"
        except:
            print('Error')

    def check_client_register(self, username):
        if(username == 'admin'):
            return False
        else:
            cursor.execute("SELECT * FROM `account` WHERE username='{}'".format(username))
            data = cursor.fetchall()
            if(data):
                return False
            else: 
                return True

    def check_room(self, roomName):
        cursor.execute("SELECT * FROM `account` WHERE username='{}'".format(roomName))
        data = cursor.fetchall()
        if(data):
            return False
        else: 
            return True

# ---------------MAIN----------------
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    port='3306',
    database='chat_app_db'
)
cursor = db.cursor()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect( (HOST, SERVER_POST) )
print('CLIENT SIDE')

app = App()
app.mainloop()