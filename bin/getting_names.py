import json
import requests
import bs4
from datetime import datetime

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)


with open('/Users/abhayms//Documents/ontology-learning-master/bin/relations.json','r') as q:
    lines = json.load(q)

j=[]
for line in lines:
    if "Q" in line[0]:
        j.append(line[0])
    if "Q" in line[2]:
        j.append(line[2])

z = list(set(j))
print(len(z))

def get_name_from_qid(qid):
    try:
        URL = 'https://www.wikidata.org/wiki/'+str(item)
        html = requests.get(URL) 
        b = bs4.BeautifulSoup(html.text, 'lxml')
        h1 = b.find("h1")
        wiki_title = h1.contents[0].text.split("\n")
        return wiki_title[1]
    except:
        return ""

for item in z:
    dic = {}
    k = get_name_from_qid(item)
    dic[item] = k
    with open("names.json", "a+") as outfile:  
        json.dump(dic, outfile)
        outfile.write('\n')

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)
    
      

