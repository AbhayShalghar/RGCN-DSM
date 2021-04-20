import json
import pandas as pd
import threading

with open('/Users/abhayms//Documents/ontology-learning-master/data/wikipeople/tacred_dataset.json') as f:
    data = json.load(f)

with open('/Users/abhayms//Documents/ontology-learning-master/bin/relations.json') as g:
    data1 = json.load(g)

#for entity in data1:
def generation(entity):
    mg = {'name':entity,'title':0,'first_section':0,'infobox':0,'link':0,'subsection':0,'section':0}
    for section in data:
        count = 0
        text = str(section["text"])
        a, b = text.count(entity[0]), text.count(entity[2])
        if (a>0 and b>0):
            count = min(a,b)
        mg[section['doc_type']] = mg[section['doc_type']] + count

    with open('pair-vectors.txt', 'a+') as filehandle:
            filehandle.write('%s\n' % mg)

for i in range(0,len(data1),5):
    t1 = threading.Thread(target=generation,args=(data1[i],))
    t2 = threading.Thread(target=generation,args=(data1[i+1],))
    t3 = threading.Thread(target=generation,args=(data1[i+2],))
    t4 = threading.Thread(target=generation,args=(data1[i+3],))
    t5 = threading.Thread(target=generation,args=(data1[i+4],))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
