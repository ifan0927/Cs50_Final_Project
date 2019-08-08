import jieba
import mysql.connector

lawdb = mysql.connector.connect(
        host="localhost",
        user = "root",
        password = "q7a4z1258",
        database = "law",
    )

db = lawdb.cursor()

sql = """SELECT short FROM law.work WHERE id = 1"""
db.execute(sql)
short = db.fetchone()
lawdb.commit()

result = list(jieba.lcut(short[0], cut_all=False))
print(result)


lawdb.close()