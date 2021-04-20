import json
import bs4
import requests


def get_wiki_title_from_wiki_url(wiki_url):
    #print(result["link"])
    html = requests.get(wiki_url)
    b = bs4.BeautifulSoup(html.text, 'lxml')
    h1 = b.find("h1")
    wiki_title = h1.contents[0]
    return wiki_title

with open('/Users/abhayms//Documents/ontology-learning-master/bin/relations.json','r') as q:
    lines = json.load(q)

with open('/Users/abhayms//Documents/ontology-learning-master/bin/links.json','r') as f:
    lines1 = json.load(f)

d=[]
for lin in lines1:
    for k in lin:
        d.append(k)

for r in lines1:
    for line in lines:
        if "Q" in line[0]:
            if line[0] in d:
                try:
                    line[0] = get_wiki_title_from_wiki_url(r[line[0]])
                    print(line[0])
                except:
                    pass
        if "Q" in line[2]:
            if line[2] in d:
                try:
                    line[2] = get_wiki_title_from_wiki_url(r[line[2]])
                    print(line[2])
                except:
                    pass


