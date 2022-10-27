from typing import Union, Optional
from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector 
import hashlib

FORMAT = 'utf-8'

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
    id: Optional[int] = None
    username: str
    password: str

@app.get("/")
def hello():
    return {"Hello"}

@app.get("/user/login")
def login():
    cursor.execute("select * from account")
    accounts = cursor.fetchall()
    return accounts

@app.post("/user/register")
def register(item: User):
    hashpass = hashlib.md5(item.password.encode(FORMAT)).hexdigest()
    cursor.execute("INSERT INTO `account`(username, password) VALUES('%s', '%s')" % (item.username, hashpass))
    db.commit()
    return {"Create account successfully"}