import json
from datetime import datetime

import pandas as pd
import time
df = pd.read_csv('/Users/abhayms//Documents/ontology-learning-master/data/wikipeople/wikipeople_dataset.txt', delimiter = "\t", names=["Entity1","Relation","Entity2"])

a = []

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

entity1 = set(df["Entity1"])
#print(len(df['Entity1']))
for ene in entity1:
    if "Q" in ene:
        a.append(ene)

entity2 = set(df["Entity2"])

for en in entity2:
    if "Q" in en:
        a.append(en)
print(len(set(a)))
z = list(set(a))


def get_wikipedia_url_from_wikidata_id(wikidata_id, lang=None, debug=False):
        import requests
        from requests import utils

        url = (
        'https://www.wikidata.org/w/api.php'
        '?action=wbgetentities'
        '&props=sitelinks/urls'
        f'&ids={wikidata_id}'
        '&format=json')

        json_response = requests.get(url).json()
    
        if debug: print(wikidata_id, url, json_response) 

        entities = json_response.get('entities')    
        if entities:
            entity = entities.get(wikidata_id)
            if entity:
                sitelinks = entity.get('sitelinks')
                if sitelinks:
                    if lang:
                        # filter only the specified language
                        sitelink = sitelinks.get(f'{lang}wiki')
                        if sitelink:
                            wiki_url = sitelink.get('url')
                            if wiki_url:
                                return requests.utils.unquote(wiki_url)
                    else:
                        # return all of the urls
                        wiki_urls = {}
                        for key, sitelink in sitelinks.items():
                            wiki_url = sitelink.get('url')
                            if wiki_url:
                                wiki_urls[key] = requests.utils.unquote(wiki_url)
                        return wiki_urls
            return {}


print(get_wikipedia_url_from_wikidata_id("Q1733560"))   
print("\n\n") 
print(get_wikipedia_url_from_wikidata_id("Q233926"))    
print("\n\n") 
print(get_wikipedia_url_from_wikidata_id("Q1699533"))    


""" with open('/Users/abhayms//Documents/ontology-learning-master/bin/relations.json','r') as f:
    lines = json.load(f)
i=0
g=0
for k in z:
    #print(k)
    g = g+1
    b = get_wikipedia_url_from_wikidata_id(k)
    if b:
        print(k)
        print(b)
        print(g)
        i=i+1

print(i)

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time) """