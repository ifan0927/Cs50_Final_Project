import json ,jieba ,requests
import requests
import datetime

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

    timeOut = 25

    res = requests.post(Url, json=payloadData, headers=payloadHeader, timeout=timeOut,allow_redirects=True)
    r_dict = json.loads(res.text)
    publish = []
    for i in range(len(r_dict['hits']['hits'])):
        publish.append(r_dict['hits']['hits'][i]['_source']['sJournalItem1'])

    # return the publish 
    return publish

def compare(publish_1, publish_2, operate):
    if str(operate) == "&":
        result = []

        for n in publish_1:
            for m in publish_2:
                if n == m:
                    result.append(n)
                    break
        
        return result
        

    elif str(operate) == "+":

        result = []
        for i in publish_1:
            result.append(i)
        for i in publish_2:
            result.append(i)
        
        return result
