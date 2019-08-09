import json ,jieba ,requests
import requests
import datetime
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras import backend
import jieba
import pandas as pd


def textsearch(name):
    # get the post server in the website
    Url = "http://61.63.46.134:9000/ip-solr/ds2journalitem/document/_search"

    # set the Data send to the server
    payloadData ={"size":100,"from":0,"query":{"bool":{"should":[{"query_string":{"query":"name"}},{"has_child":{"type":"paragraph","score_mode":"sum","query":{"query_string":{"query":"name"}}}}]}},"sort":[{"sDatePublishOrder":{"order":"desc"}}],"highlight":{"tags_schema":"styled","encoder":"html","fragment_size":"9999","fields":{"*":{}}}}

    payloadData['query']['bool']['should'][0]['query_string']['query'] = name
    payloadData['query']['bool']['should'][1]['has_child']['query']['query_string']['query'] = name

    payloadHeader = {
    'Host':'http://61.63.46.134:9000/ip-solr/ds2journalitem/document/_search',
    'Content-Type': 'application/json',
    }

    timeOut = 20

    res = requests.post(Url, json=payloadData, headers=payloadHeader, timeout=timeOut,allow_redirects=True)
    r_dict = json.loads(res.text)
    publish = []
    name = []
    link = []
    url = "http://lawdata.com.tw/tw/detail.aspx?no="
    for i in range(len(r_dict['hits']['hits'])):
        publish.append(r_dict['hits']['hits'][i]['_source']['sJournalItem1'])
        name.append(r_dict['hits']['hits'][i]['_source']['sAuthorName'])
        full_url = str(url) + str(r_dict['hits']['hits'][i]['_source']['iJournalItem'])+ "&listkey="
        link.append(full_url)

    # return the publish 
    return publish ,name ,link

def compare(publish_1, publish_2, author_1, author_2, link_1, link_2, operate):
    publish = []
    author = []
    link =[]
    
    if str(operate) == "&":
        for n in range(len(publish_1)):
            for m in range(len(publish_2)):
                if n == m:
                    publish.append(publish_1[n])
                    author.append(author_1[n])
                    link.append(link_1[n])
                    break
        
        return publish, author, link
        

    elif str(operate) == "+":
        for i in range(len(publish_1)):
            publish.append(publish_1[i])
            author.append(author_1[i])
            link.append(link_1[i])
        for i in range(len(publish_2)):
            publish.append(publish_2[i])
            author.append(author_2[i])
            link.append(link_2[i])
        
        return publish, author, link


def preprocess(text):
    # load the preset dict for jieba
    jieba.load_userdict("ml/jieba_dict/user_dict.txt")

    # turn the input to pd dataframe:
    test_data = pd.DataFrame(text, columns=['short'])
    
    # using jieba to cut the word
    cut = lambda x : list(jieba.cut(x))
    test_data['word'] = test_data['short'].apply(cut)

    # make the tokenizer 
    data_tokenizer = Tokenizer()
    data_tokenizer.fit_on_texts(test_data['word'])

    # covert the word to seqence of number
    test_data_ids = data_tokenizer.texts_to_sequences(test_data['word'])

    # uniform the length of the data
    test_data_padded_seqs = pad_sequences(test_data_ids, maxlen=20)

    return test_data_padded_seqs


def predict(data):
    model = load_model('ml/pretrain.h5')
    ans = model.predict(data)

    n = ans.tolist()
    forecast = []

    for i in n:
        temp = i
        if temp[0] > temp[1] and temp[0] > temp[2]:
            forecast.append("民法")
        elif temp[1] > temp[0] and temp[1] > temp[2]:
            forecast.append("刑法")
        elif temp[2] > temp[0] and temp[2] > temp[1] :
            forecast.append("其他")
    
    backend.clear_session()

    return forecast
