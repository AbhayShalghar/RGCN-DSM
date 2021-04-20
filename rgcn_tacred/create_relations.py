import pandas as pd
import time
import json
df = pd.read_csv('tacred_dataset.txt', delimiter = "\t", names=["Entity1","Relation","Entity2"])

a = []
entity1 = set(df["Entity1"])
#print(len(df['Entity1']))
#print(entity1)

#print(len(entity1))

relation = set(df["Relation"])
print(relation, len(relation))
#print(len(df['Relation']))
#print(len(relation))

entity2 = set(df["Entity2"])
#print(entity2)

k = []
lis = []
j=0
with open('tacred_dataset.txt', 'r') as f:
    for line in f:
        dic = {}
        k = line.strip().split('\t',3)
        dic['Entity1'] = k[0]
        dic['Relation'] = k[1]
        dic['Entity2'] = k[2]
        lis.append((k[0],k[1],k[2]))

#print(lis)
out_file = open("relations.json", "w") 
json.dump(lis, out_file, indent = 4, sort_keys = False)
    
out_file.close()   