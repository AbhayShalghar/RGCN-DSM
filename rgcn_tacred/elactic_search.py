from elasticsearch import Elasticsearch
from ssl import create_default_context
import json
from datetime import datetime
import requests
from requests import utils

""" with open('/Users/abhayms//Documents/ontology-learning-master/bin/names.json','r') as h:
    names = json.load(h)

d=[]
c=[]
for name in names:
    for k,v in name.items():
        d.append(k)
        c.append(v)

print(d[0])
print(c[0]) """

es = Elasticsearch()


def get_elastic_results_exact(text1,text2):
    search_param = {
                'query': {
                    'query_string': {
                        #"query": "(Jiajing Emperor) AND (Zhu Houcong)", 
                        "query": "(\""+text1+"\")"+" AND "+"(\""+text2+"\")",
                        "fields": ["text"],
                    }
                }
            }
    res = es.search(index="tacred-test", body=search_param)
    return res

def get_elastic_results_partial(text1,text2):
    search_param = {
                'query': {
                    'query_string': {
                        #"query": "(Jiajing Emperor) AND (Zhu Houcong)", 
                        "query": "("+text1+")"+" AND "+"("+text2+")",
                        "fields": ["text"],
                    }
                }
            }
    res = es.search(index="tacred-test", body=search_param)
    return res

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

with open('relations.json','r') as f:
    lines = json.load(f)
i=0
j=0
k=0
for line in lines:
    k = k+1
    try:
        #print(line[0],line[2])
        results = get_elastic_results_exact(line[0],line[2])
        x = results['hits']['hits']
        if(results['hits']['total']['value'])>0:
            i = i+1
        else:
            results = get_elastic_results_partial(line[0], line[2])
            x = results['hits']['hits']
            j = j+1
        dic = {'entity1':line[0], 'entity2': line[2], 'title':0, 'infobox':0, 'first_section':0, 'section':0, 'text_sentence':0}
        for item in x:
            #print(item)
            dic[item['_source']['type']] = dic[item['_source']['type']] + 1
        with open("vectors_exact_partial.json", "a+") as outfile:  
            json.dump(dic, outfile)
            outfile.write('\n')
    except:
        pass


print(i,j,k)
now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)



#print(res['hits']['total']['value'])
""" dic = {'text_sentence':0, 'infobox':0, 'title':0, 'section':0, 'first_section':0}
x = res['hits']['hits']
print(res['hits']['total']['value'])
for item in x:
    #print(item['_source']['text'])
    #print("\t")
    #print(item['_source']['type'])
    dic[item['_source']['type']] = dic[item['_source']['type']] + 1
    #vector using doctype 
print(dic) """