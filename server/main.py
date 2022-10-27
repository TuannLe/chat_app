from typing import Union
from fastapi import FastAPI, Depends
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
# import mysql.connector 
import hashlib

FORMAT = 'utf-8'

app = FastAPI()

models.Base.metadata.create_all(engine)

# db = mysql.connector.connect(
#     host='localhost',
#     user='root',
#     password='',
#     port='3306',
#     database='chat_app_db'
# )
# cursor= db.cursor()

@app.get("/")
def hello():
    return {"Hello"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/user/login")
def login(request: schemas.User, db : Session = Depends(get_db)) :
    # cursor.execute("select * from account")
    # accounts = cursor.fetchall()
    # return accounts
    return db


# @app.post("/user/register")
# def register(username: str, password: str):
    # hashpass = hashlib.md5(password.encode(FORMAT)).hexdigest()
    # cursor.execute("INSERT INTO `account`(username, password) VALUES('%s', '%s')" % (username, password))
    # db.commit()
    # return {"Create account successfully"}