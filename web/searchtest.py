from scrap1 import search
from abstract import abstract
import csv
import time

def main():
    
    name = str(input("what you want to search?"))

    r_dict = search(name)
    publish = []
    keyword = []
    herf_id = []

    for i in range(len(r_dict['hits']['hits'])):
        publish.append(r_dict['hits']['hits'][i]['_source']['sJournalItem1'])
        keyword.append(r_dict['hits']['hits'][i]['_source']['sKeyword'])
        herf_id.append(r_dict['hits']['hits'][i]['_source']['iJournalItem'])

    print(publish)

            
if __name__ == "__main__":
    main()