import pyodbc

conx = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=LAPTOP-4NB1E5PG\SQLEXPRESS; Database=LTM_CHAT_APP; UID=sa; PWD=12345678;')

cursor = conx.cursor()

for row in cursor.execute("select * from Account where username = 'a'"):
    print(row.username)
    print(row[0])
    print(row)

cursor.execute("select * from Account")

data = cursor.fetchall()

print(data)

# username='tuanle'
# password='12345'

# cursor.execute("insert Account values (?,?)", username, password)
# conx.commit()
conx.close()