#%%
from wikidata.client import Client
import json
import codecs
import WikipediaLib

#%%
# global variables
qids_labels_map = {}
client = Client()

#%%
def load_qids_labels_file(qids_labels_file):
    global qids_labels_map
    f = codecs.open(qids_labels_file, "r", "utf8")
    qids_labels_map = json.load(f)
    f.close()

#entity = client.get('Q20145', load=True)
#print(entity)
#print(entity.description)
def get_qid_label(qid):
    global qids_labels_map
    if qids_labels_map.get(qid) is not None:
        return qids_labels_map.get(qid)
    try:
        url = WikipediaLib.get_wikipedia_url_from_wikidata_id(qid)
        title = WikipediaLib.get_title_from_wiki_url_hack(url)
        qids_labels_map[qid] = title
        return title
    except:
        try:
            entity = client.get(qid, load=False)
            qids_labels_map[qid] = entity.label
            return entity.label
        except:
            return ""

#%%
def populate_map_from_file(input_file):
    pf = open(input_file, "r")
    plines = pf.readlines()
    pf.close()
    output_map = {}
    for pline in plines:
        parts = pline.split("\t")
        if len(parts) < 2:
            continue
        pid = parts[0]
        if output_map.get(pid) is None:
            output_map[pid] = parts[1]
    return output_map
 
#%%    
# takes a wikipeople file as input
# note the portion where we only use presumed qids of people and not all entities
def create_wikipeople_dataset(relations_file, attributes_file, input_file, output_file):
    #%%
    f = open(input_file, "r")
    lines = f.readlines()
    f.close()
    
    relations_map = populate_map_from_file(relations_file)
    attributes_map = populate_map_from_file(attributes_file)

    #%%
    dedup_map = {}
    for line in lines:
        try:
            #print(line)
            json_line = json.loads(str(line))
            output_element = {}
            output_str = ""
            i = 0
            for k, v in json_line.items():
                try:
                    if len(k) < 2:
                        continue
                    parts = k.split("_")
                    if len(parts) < 2:
                        continue
                    pid = parts[0]
                    qid = v
                    if i == 0:
                        source = get_qid_label(qid)
                        if len(source) < 1:
                            source = qid
                        predicate = ""
                        if relations_map.get(pid) is not None:
                            predicate = relations_map.get(pid)
                        elif attributes_map.get(pid) is not None:
                            predicate = attributes_map.get(pid)
                        else:
                            print("Error: invalid pid:", pid)
                        predicate = predicate.replace(" ", "_")
                    elif i == 1:
                        object = get_qid_label(qid)
                        if len(object) < 1:
                            object = qid
                        ofs1 = codecs.open(output_file, "a+", "utf8")
                        key = source + "\t" + predicate + "\t" + object
                        if dedup_map.get(key) is None:
                            dedup_map[key] = ""
                            ofs1.write(key + "\n")
                            ofs1.flush()
                        ofs1.close()
                    i += 1
                except Exception as e:
                    print(str(e))
                    continue
        except Exception as e2:
            print(str(e2))
            continue



#%%
relations_file = "./data/wikipeople/wiki_people_relations.txt"
attributes_file = "./data/wikipeople/wiki_people_attributes.txt"
input_file = "./data/wikipeople/n-ary_train.json"
output_file = "./data/wikipeople/wikipeople_dataset.txt"
qids_labels_file = "./data/wikipeople/wikidata_qids_labels.json"
load_qids_labels_file(qids_labels_file)
create_wikipeople_dataset(relations_file, attributes_file, input_file, output_file)
ofs = codecs.open(qids_labels_file, "w", "utf8")
json.dump(qids_labels_map, ofs)
ofs.close()

if __name__ == "__main__":
    relations_file = "./data/wikipeople/wiki_people_relations.txt"
    attributes_file = "./data/wikipeople/wiki_people_attributes.txt"
    input_file = "./data/wikipeople/n-ary_train.json"
    output_file = "./data/wikipeople/wikipeople_dataset.txt" 
    qids_labels_file = "./data/wikipeople/wikidata_qids_labels.json"
    load_qids_labels_file(qids_labels_file)
    create_wikipeople_dataset(relations_file, attributes_file, input_file, output_file)
    ofs = codecs.open(qids_labels_file, "w", "utf8")
    json.dump(qids_labels_map, ofs)
    ofs.close()
