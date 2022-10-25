import mysql.connector 

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    port='3306',
    database='chat_app_db'
)

cursor= db.cursor()
cursor.execute("select * from account")

accounts = cursor.fetchall()
print(accounts)