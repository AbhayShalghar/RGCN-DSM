import json
import pandas as pd
from collections import Counter

with open('/Users/abhayms//Documents/ontology-learning-master/data/wikipeople/tacred_dataset.json') as f:
    data = json.load(f)

print(type(data))
df1 = pd.read_csv('/Users/abhayms//Documents/ontology-learning-master/data/wikipeople/wikipeople_dataset.txt', delimiter = "\t", names=["Entity1","Relation","Entity2"])
entity1 = set(df1['Entity1'])
entity1 = list(entity1)

for entity in entity1:
    mg = {'name':entity,'title':0,'first_section':0,'infobox':0,'link':0,'subsection':0,'section':0}
    for section in data:
        #print(section)
        text = str(section["text"])
        count = text.count(str(entity))
        mg[section['doc_type']] = mg[section['doc_type']] + count
       
    print(mg)
    with open('vectors.txt', 'a+') as filehandle:
            filehandle.write('%s\n' % mg)
    
