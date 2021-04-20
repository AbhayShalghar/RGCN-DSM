from elasticsearch import Elasticsearch
from ssl import create_default_context
import json
import uuid
import nltk
import codecs
from datetime import datetime
import threading


now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

es = Elasticsearch()

def publish(input_file):
    f = codecs.open(input_file, "r", "utf8")
    lines = f.readlines()   #reading lines from the file
    f.close()
    for line in lines:
        line = line.strip()
        jd = json.loads(line)
        k = next(iter(jd))
        jd = jd[k]
        try:
            qid = jd["wikidata_qid"]
        except:
            continue
        try:
            doc = {}
            doc['qid'] = jd['wikidata_qid']
            #doc['wiki_url'] = jd['wiki_url']
            doc['title'] = jd['title']
            doc['text'] = jd['title']
            doc['type'] = "title"
            res = es.index(index="wikipeople-test", id= doc['qid'] + "_1", body=doc)
        except Exception as e:
            print("Error writing title")
            print(str(e))

        # text
        tokens = nltk.sent_tokenize(jd['text'])
        n = 0
        for t in tokens:
            try:
                doc = {}
                doc['qid'] = jd['wikidata_qid']
                doc['title'] = jd['title']
                doc['text'] = t
                # TODO: Do actual relation extraction
                doc['relation'] = "relation"
                doc['type'] = "text_sentence"
                res = es.index(index="wikipeople-test", id=doc['qid'] + "_text_" + str(n), body=doc)
                n = n + 1
            except Exception as e:
                print("Error writing text")
                print(str(e))
   
        # qid
        try:
            doc = {}
            doc['qid'] = jd['wikidata_qid']
            doc['title'] = jd['title']
            #doc['wiki_url'] = jd['wiki_url']
            doc['text'] = jd['first_section']
            doc['type'] = "first_section"
            res = es.index(index="wikipeople-test", id=doc['qid'] + "_3", body=doc)
        except Exception as e:
            print("Error writing first_section")
            print(str(e))
   
        # infobox
        try:
            if jd.get("infobox") is not None and len(jd.get("infobox")) > 0:
                y = 0
                for k, v in jd['infobox'].items():
                    doc = {}
                    doc['qid'] = jd['wikidata_qid']
                    doc['title'] = jd['title']
                    #doc['wiki_url'] = jd['wiki_url']
                    doc["text"] = k
                    doc['type'] = "infobox"
                    res = es.index(index="wikipeople-test", id=doc['qid'] +  "_info_" + str(y), body=doc)
                    y = y + 1
        except Exception as e:
            print("Error writing infobox")
            print(str(e))
            
        # sections
        section_by_title_list = jd['section_by_title']
        for section_by_title in section_by_title_list:
            if section_by_title.get("text") is not None:
                try:
                    doc = {}
                    doc['qid'] = jd['wikidata_qid']
                    doc['title'] = jd['title']
                    #doc['wiki_url'] = jd['wiki_url']
                    doc["text"] = section_by_title.get("text") 
                    doc['type'] = "section"
                    res = es.index(index="wikipeople-test", id=doc['qid'] + "_5", body=doc)
                except Exception as e:
                    print("Error writing section")
                    continue
            # subsections
            if section_by_title.get("subsections") is not None:
                subsections_list = section_by_title.get("subsections")
                if len(subsections_list) < 1:
                    continue
                    for subsection_map in subsections_list:
                        if subsection_map.get('text') is not None:
                            try:
                                doc = {}
                                doc['qid'] = jd['wikidata_qid']
                                doc['title'] = jd['title']
                                #doc['wiki_url'] = jd['wiki_url']
                                doc["text"] = subsection_map.get("text") 
                                doc['type'] = "subsection"
                                res = es.index(index="wikipeople-test", id=doc['qid'] + "_6", body=doc)
                            except Exception as e:
                                print("Error writing subsection")
                                continue

input_file_1 = "/Users/abhayms//Documents/ontology-learning-master/data/wikipeople/n-ary_train_qid_details.json.15"
input_file_2 = "/Users/abhayms//Documents/ontology-learning-master/data/wikipeople/n-ary_train_qid_details.json.16"
input_file_3 = "/Users/abhayms//Documents/ontology-learning-master/data/wikipeople/n-ary_train_qid_details.json.17"
input_file_4 = "/Users/abhayms//Documents/ontology-learning-master/data/wikipeople/n-ary_train_qid_details.json.18"
input_file_5 = "/Users/abhayms//Documents/ontology-learning-master/data/wikipeople/n-ary_train_qid_details.json.19"

t1 = threading.Thread(target=publish,args=(input_file_1,))
t2 = threading.Thread(target=publish,args=(input_file_2,))
t3 = threading.Thread(target=publish,args=(input_file_3,))
t4 = threading.Thread(target=publish,args=(input_file_4,))
t5 = threading.Thread(target=publish,args=(input_file_5,))
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
#publish(input_file)

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)
