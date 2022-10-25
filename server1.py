import socket 
import threading 
import hashlib
# import pyodbc
import mysql.connector 

# Socket
HOST = "127.0.0.1" 
SERVER_PORT = 65432 
FORMAT = "utf8"

# Database config
# SERVER = 'LAPTOP-4NB1E5PG\SQLEXPRESS'
# DATABASE = 'LTM_CHAT_APP'
# UID = 'sa'
# PWD = '12345678'

# Option
FAIL = 'fail'
SUCCESS = 'success'
LOGIN = 'login'
END = 'x'

def recvList(conn):
    list = []

    item = conn.recv(1024).decode(FORMAT)

    while (item != "end"):
        
        list.append(item)
        #response
        conn.sendall(item.encode(FORMAT))
        item = conn.recv(1024).decode(FORMAT)
    
    return list

def serverLogin(conn):
    print('Login starting...')
    username= conn.recv(1024).decode(FORMAT)
    conn.sendall(username.encode(FORMAT)) 
    pswd = conn.recv(1024).decode(FORMAT)
    conn.sendall(pswd.encode(FORMAT))  
    hashpass = hashlib.md5(pswd.encode(FORMAT)).hexdigest()
    
    cursor.execute("SELECT * FROM account WHERE username='%s' AND password='%s'" % (username, hashpass))
    data = cursor.fetchall()
    msg='okk'
    if(data):
        msg = SUCCESS
        print(msg)
    else:
        msg = FAIL
        print(msg)
    conn.sendall(msg.encode(FORMAT))

def handleClient(conn: socket, addr):
    print("conn:",conn.getsockname())
    option = conn.recv(1024).decode(FORMAT)
    while (option != END):
        if (option == LOGIN):
            serverLogin(conn)     
    
    print("client" , addr, "finished")
    print(conn.getsockname(), "closed")
    conn.close()

#--------------------MAIN-------------
# conx = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=' + SERVER  +'; Database=' + DATABASE + '; UID='+UID + '; PWD='+PWD)
# cursor = conx.cursor()
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    port='3306',
    database='chat_app_db'
)
cursor = db.cursor()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind((HOST, SERVER_PORT))
s.listen()

print("SERVER SIDE")
print("server:", HOST, SERVER_PORT)
print("Waiting for Client")

nClient = 0
while (nClient < 5):
    try:
        conn, addr = s.accept()
        
        thr = threading.Thread(target=handleClient, args=(conn,addr))
        thr.daemon = False
        thr.start()
    except:
        print("Error")
    nClient += 1


print("End")
input()
s.close()
# conx.close()