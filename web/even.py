import mysql.connector

lawdb = mysql.connector.connect(
        host="localhost",
        user = "root",
        password = "q7a4z1258",
        database = "law",
    )

db = lawdb.cursor()

sql = """SELECT publish from cons"""

db.execute(sql)
temp = db.fetchall()
count = 0

for i in temp:
    count = count + len(str(i))


print(count/len(temp))

lawdb.close()
