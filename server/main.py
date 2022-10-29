from typing import Union, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector 
import hashlib

HOST = "127.0.0.1" 
SERVER_PORT = 65432 
FORMAT = 'utf-8'
import socket 

app = FastAPI()

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    port='3306',
    database='chat_app_db'
)
cursor= db.cursor()

class User(BaseModel):
    # id: Optional[int] = None
    username: str
    password: str

@app.get("/")
def hello():
    return {"Hello"}

@app.post("/user/login")
def login(item: User):
    hashpass = hashlib.md5(item.password.encode(FORMAT)).hexdigest()
    cursor.execute("SELECT * FROM account WHERE username='%s' AND password='%s'" % (item.username, hashpass))
    accounts = cursor.fetchone()
    if accounts:
        return accounts
    else:
        raise HTTPException(status_code=500, detail="Login failed")

@app.post("/user/register")
def register(item: User):
    try:
        accepted = check_client_register(item.username)
        if accepted:
            hashpass = hashlib.md5(item.password.encode(FORMAT)).hexdigest()
            cursor.execute("INSERT INTO `account`(username, password) VALUES('%s', '%s')" % (item.username, hashpass))
            db.commit()
            return {"Create account successfully"}
    except:
        raise HTTPException(status_code=500, detail="Username already exists")

def check_client_register(username):
    if(username == 'admin'):
        return False
    else:
        cursor.execute("SELECT * FROM `account` WHERE username='{}'".format(username))
        data = cursor.fetchone()
        if(data):
            return False
        else: 
            return True

@app.get('/user/all')
def get_all_user():
    try:
        cursor.execute("select * from Account")
        data = cursor.fetchall()
        return data
    except:
        raise HTTPException(status_code=500, detail="Failed")

def open_socket(): 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((HOST, SERVER_PORT))
    s.listen()
    conn, addr = s.accept()      