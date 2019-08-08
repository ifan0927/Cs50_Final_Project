import requests
from bs4 import BeautifulSoup

def abstract(key):
    url = "http://lawdata.com.tw/tw/detail.aspx?no="
    resp = requests.get(url + str(key) + "&listkey=")
    soup = BeautifulSoup(resp.text,'html.parser')
    try:
        tables = soup.find('table', id='abstract')
    except AttributeError:
        return 
    try:
        for i in tables.find_all(id='SearchItem'):
            if len(i.text) > 100:
                return i.text
    except AttributeError:
        return
    
        
    
