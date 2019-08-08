from scrap1 import search
from abstract import abstract
import csv
import mysql.connector

def main():
    lawdb = mysql.connector.connect(
        host="localhost",
        user = "root",
        password = "q7a4z1258",
        database = "law",
    )

    db = lawdb.cursor()

    with open ('list.csv', newline='',encoding = 'utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            r_dict = search(row[0])
            publish = []

            for i in range(len(r_dict['hits']['hits'])):
                publish.append(r_dict['hits']['hits'][i]['_source']['sJournalItem1'])
                
                sql = """INSERT INTO other (publish) VALUE (%s)""" 
                record = (str(publish[i]),)

                db.execute(sql,record)
                lawdb.commit()
    
    lawdb.close()
                

            
if __name__ == "__main__":
    main()