import pandas as pd
import time
import json
df = pd.read_csv('/Users/abhayms//Documents/ontology-learning-master/data/wikipeople/wikipeople_dataset.txt', delimiter = "\t", names=["Entity1","Relation","Entity2"])

a = []
entity1 = set(df["Entity1"])
#print(len(df['Entity1']))
for ene in entity1:
    if "Q" in ene:
        a.append(ene)

#print(len(entity1))

relation = set(df["Relation"])
#print(len(df['Relation']))
#print(len(relation))

entity2 = set(df["Entity2"])
#print(len(df['Entity2']))

for en in entity2:
    if "Q" in en:
        a.append(en)
print(len(set(a)))
#print(len(entity2))

""" k = []
lis = []
j=0
with open('/Users/abhayms//Documents/ontology-learning-master/data/wikipeople/wikipeople_dataset.txt', 'r') as f:
    for line in f:
        dic = {}
        k = line.strip().split('\t',3)
        dic['Entity1'] = k[0]
        dic['Relation'] = k[1]
        dic['Entity2'] = k[2]
        if ((k[1] == 'father') or (k[1] == 'mother') or (k[1] == 'child') or (k[1] == 'spouse') or (k[1] == 'sibling') or (k[1] == 'employer') or ('partner' in k[1]) or ('student' in k[1])):
            lis.append((k[0],k[1],k[2]))

#print(lis)
out_file = open("relations.json", "w") 
json.dump(lis, out_file, indent = 4, sort_keys = False)
    
out_file.close()     """   

