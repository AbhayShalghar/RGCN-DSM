#%%
import json
import sys
from datetime import datetime
import codecs
import pywikibot
from os import path

# NEED TO SET THE FOLLOWING ENV VARIABLES
# export LC_ALL=en_US.UTF-8
# export LANG=en_US.UTF-8
# export PYWIKIBOT_NO_USER_CONFIG=1

now = datetime.now()
dt_string = now.strftime("%Y%m%d%H%M%S")

site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()

wikidata_properties = {}
f = codecs.open("../input/wikidata_properties.txt", "r", "utf8")
lines = f.readlines()
for line in lines:
    parts = line.split("|")
    pid = parts[0]
    label = parts[2]
    wikidata_properties[pid] = label
f.close()

#wikidata_entity_item_map_file = data_dir + "/wikidata_entity_item_map_file.json"
#if path.exists(wikidata_entity_item_map_file):
#    f = codecs.open(wikidata_entity_item_map_file, "r", "utf8")
#    wikidata_entity_item_map = json.load(f)
#    f.close()
#else:
#    wikidata_entity_item_map = {}
wikidata_entity_item_map = {}

wikidata_entity_properties_map_file = data_dir + "/wikidata_entity_properties_map_file.json"
if path.exists(wikidata_entity_properties_map_file):
    f = codecs.open(wikidata_entity_properties_map_file, "r", "utf8")
    wikidata_entity_properties_map = json.load(f)
    f.close()
else:
    wikidata_entity_properties_map = {}

wikidata_entity_label_map_file = data_dir + "/wikidata_entity_label_map_file.json"
if path.exists(wikidata_entity_label_map_file):
    f = codecs.open(wikidata_entity_label_map_file, "r", "utf8")
    wikidata_entity_label_map = json.load(f)
    f.close()
else:
    wikidata_entity_label_map = {}

wikidata_entity_desc_map_file = data_dir + "/wikidata_entity_desc_map_file.json"
if path.exists(wikidata_entity_desc_map_file):
    f = codecs.open(wikidata_entity_desc_map_file, "r", "utf8")
    wikidata_entity_desc_map = json.load(f)
    f.close()
else:
    wikidata_entity_desc_map = {}

def get_entity_label_desc(entity):
    global wikidata_entity_item_map
    global wikidata_entity_label_map
    global wikidata_entity_desc_map
    entity_label = None
    entity_desc = None

    flag = False
    if wikidata_entity_label_map.get(entity) is not None:
        entity_label = wikidata_entity_label_map.get(entity)
    else:
        flag = True
    if wikidata_entity_desc_map.get(entity) is not None:
        entity_desc = wikidata_entity_desc_map.get(entity)
    else:
        flag = True

    if flag == False:
        return entity_label, entity_desc

    if wikidata_entity_item_map.get(entity) is not None:
        item_dict = wikidata_entity_item_map[entity]
    else:
        item = pywikibot.ItemPage(repo, entity)
        item_dict = item.get()
        wikidata_entity_item_map[entity] = item_dict
    try:
        if item_dict.get('labels') is not None:
            labels = item_dict['labels']
            if labels.get('en') is not None:
                entity_label = labels['en']
                wikidata_entity_label_map[entity] = entity_label
        if item_dict.get('descriptions') is not None:
            labels = item_dict['descriptions']
            if labels.get('en') is not None:
                entity_desc = labels['en']
                wikidata_entity_desc_map[entity] = entity_desc
    except Exception as e:
        print(str(e))
    return entity_label, entity_desc
        

def get_wikidata_properties(qid):
    if wikidata_entity_properties_map.get(qid) is not None:
        properties_list = wikidata_entity_properties_map[qid]
        return properties_list

    properties_list = []
    try:
        if wikidata_entity_item_map.get(qid) is not None:
            item_dict = wikidata_entity_item_map[qid]
        else:
            item = pywikibot.ItemPage(repo, qid)
            item_dict = item.get()
            wikidata_entity_item_map[qid] = item_dict

        clm_dict = item_dict["claims"]
        for pid, clm_list in clm_dict.items():
            for clm in clm_list:
                try:
                    #print("pid:", pid)
                    #print(prop_desc)
                    clm_json = clm.toJSON()
                    #print(clm_json)
                    if clm_json.get('mainsnak') is None:
                        continue
                    mainsnak = clm_json.get('mainsnak')
                    if mainsnak.get('property') is None:
                        continue
                    if mainsnak.get('datatype') is None:
                        continue
                    data_type = mainsnak.get('datatype')
                    if data_type == 'external-id':
                        external_id = mainsnak['datavalue']['value']
                        properties_list.append((pid, external_id))
                    elif data_type == 'url':
                        url = mainsnak['datavalue']['value']
                        properties_list.append((pid, url))
                    elif data_type == 'wikibase-item':
                        property_qid = mainsnak['datavalue']['value']['numeric-id'] 
                        property_qid = "qid:Q" + str(property_qid)
                        properties_list.append((pid, property_qid))
                    else:
                        continue
                except Exception as e:
                    print(str(e))
        wikidata_entity_properties_map[qid] = properties_list
    except Exception as e:
        print(str(e))

    return properties_list

#f = codecs.open(wikidata_entity_item_map_file, "w", "utf8")
#json.dump(wikidata_entity_item_map, f, indent=4)
#f.close()

f = codecs.open(wikidata_entity_properties_map_file, "w", "utf8")
json.dump(wikidata_entity_properties_map, f, indent=4)
f.close()

f = codecs.open(wikidata_entity_label_map_file, "w", "utf8")
json.dump(wikidata_entity_label_map, f, indent=4)
f.close()

f = codecs.open(wikidata_entity_desc_map_file, "w", "utf8")
json.dump(wikidata_entity_desc_map, f, indent=4)
f.close()

#clm_dict = item_dict["claims"]
#clm_list = clm_dict["P69"]

#for clm in clm_list:
#    clm_trgt = clm.getTarget()
#    print(clm_trgt)
