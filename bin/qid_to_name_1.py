import json
from datetime import datetime
import requests
from requests import utils

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

with open('/Users/abhayms//Documents/ontology-learning-master/bin/relations.json','r') as f:
    lines = json.load(f)

j=[]
for line in lines:
    if "Q" in line[0]:
        j.append(line[0])
    if "Q" in line[2]:
        j.append(line[2])

z = list(set(j))
print(len(z))

def get_wikipedia_url_from_wikidata_id(wikidata_id, lang=None, debug=False):
    import requests
    from requests import utils

    url = (
        'https://www.wikidata.org/w/api.php'
        '?action=wbgetentities'
        '&props=sitelinks/urls'
        f'&ids={wikidata_id}'
        '&format=json')
    try:
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
    except:
        pass
    
i=0
g=0
for k in z:
    #print(k)
    g = g+1
    b = get_wikipedia_url_from_wikidata_id(k)
    dic = {}
    if b:
        dic[k] = b[next(iter(b))]
        print(g)
        i=i+1
        with open("links_1.json", "a+") as outfile:  
            json.dump(dic, outfile)
            outfile.write('\n')

print(i)

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)