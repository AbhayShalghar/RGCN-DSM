#%%
from wikidata.client import Client
import json

#%%
client = Client()
entity = client.get('Q20145', load=True)
print(entity)
print(entity.description)

#%%
f = open("./data/wikipeople/n-ary_test.json", "r")
lines = f.readlines()
f.close()

#%%
ofs1 = open("./data/wikipeople/n-ary_test_details.json", "w")
ofs2 = open("./data/wikipeople/n-ary_test_details.txt", "w")
output_list = []
for line in lines:
    #print(line)
    json_line = json.loads(str(line))
    output_element = {}
    output_str = ""
    for k, v in json_line.items():
        if len(k) < 2:
            continue
        parts = k.split("_")
        if len(parts) < 2:
            continue
        pid = parts[0]
        qid = v
        entity = client.get(qid, load=True)
        #print(entity)
        #print(entity.description)
        output_element[k] = v
        output_str += v + "\t"
        output_element[k + "_label"] = entity.label
        output_str += str(entity.label) + "\t"
        output_element[k + "_desc"] = entity.description
        output_str += str(entity.description) + "\t" 
    property = client.get(pid, load=True)
    #print(property)
    #print(property.description)
    output_element["pid"] = pid
    output_str += pid + "\t"
    output_element["pid_label"] = property.label
    output_str += str(property.label) + "\t"
    output_element["pid_desc"] = property.description
    output_str += str(property.description) + "\n"
    output_list.append(output_element)
    ofs2.write(output_str)
json.dump(output_list, ofs1)

#%%
property = client.get('P166', load=True)
print(property)

#%%
f = open("./data/wikipeople/properties.txt", "r")
lines = f.readlines()
f.close()
f = open("./data/wikipeople/properties_details.txt", "r")
props = f.readlines()
f.close()
prop_map = {}
for prop in props:
    prop = prop.strip()
    prop_map[prop] = ""
of = open("./data/wikipeople/properties_details.txt", "a+")
for pid in lines:
    pid = pid.strip()
    if prop_map.get(pid) is not None:
        continue
    try:
        property = client.get(pid, load=True)
        output_str = pid + "\t"
        output_str += str(property.label) + "\t"
        output_str += str(property.description) + "\n"
        of.write(output_str)
        of.flush()
    except:
        continue
of.close()
