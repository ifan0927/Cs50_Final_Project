import json
import requests
import datetime

def search(name): 
    # get the post server in the website
    Url = "http://61.63.46.134:9000/ip-solr/ds2journalitem/document/_search"

    # set the Data send to the server
    payloadData ={"size":500,"from":0,"query":{"bool":{"should":[{"query_string":{"query":"name"}},{"has_child":{"type":"paragraph","score_mode":"sum","query":{"query_string":{"query":"name"}}}}]}},"sort":[{"sDatePublishOrder":{"order":"desc"}}],"highlight":{"tags_schema":"styled","encoder":"html","fragment_size":"9999","fields":{"*":{}}}}

    payloadData['query']['bool']['should'][0]['query_string']['query'] = name
    payloadData['query']['bool']['should'][1]['has_child']['query']['query_string']['query'] = name

    payloadHeader = {
    'Host':'http://61.63.46.134:9000/ip-solr/ds2journalitem/document/_search',
    'Content-Type': 'application/json',
    }

    timeOut = 25

    res = requests.post(Url, json=payloadData, headers=payloadHeader, timeout=timeOut,allow_redirects=True)

    result = "search.txt"

    f = open(f"{result}","w", encoding ="utf-8")
    f.write(f"tes text = {res.text}")

    return json.loads(res.text)