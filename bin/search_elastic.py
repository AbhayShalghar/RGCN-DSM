from elasticsearch import Elasticsearch
from ssl import create_default_context
import json

es_context = create_default_context(cafile="e0dc3caf-a1f2-11e9-b619-02c049fdd00c")
es = Elasticsearch(['https://1bf6b928-7dd1-405f-b615-af9304dd5f8d.a618efcd6c3341158fb843970f0d7edd.databases.appdomain.cloud:31379'], http_auth=('admin', 'BanishCOVID19'), scheme="https", port=31379, ssl_context=es_context)

def get_elastic_results(text1,text2):
    search_param = {
        'query': {
            'match': {
                'text': text1 and text2
                #"operator" : "and"
                
            }
        }
    }
    
    res = es.search(index="wikipeople-rgcn", body=search_param)
    #res = es.get(index="wikipeople-rgcn", id=20)
    return res


with open('/Users/abhayms//Documents/ontology-learning-master/bin/relations.json','r') as f:
    lines = json.load(f)
i=0
for line in lines:
    results = get_elastic_results(line[0],line[2])
    print(results['hits'])
    break

#for hit in results['hits']['hits']:
#    output = {}
#    score = hit["_score"]
#    qid = "%(qid)s" % hit["_source"]
#    text = "%(text)s" % hit["_source"]
#    type = "%(type)s" % hit["_source"]
#    print("###### Start ######")
#    print(score)
#    #print(text)
#    print(type)
#    print(qid)
#    print("###### End ######")
#