from datetime import datetime
from elasticsearch import Elasticsearch
import codecs
import json
from ssl import create_default_context
import threading
import multiprocessing

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

es = Elasticsearch()

es_context = create_default_context(cafile="/Users/abhayms//Documents/ontology-learning-master/bin/e0dc3caf-a1f2-11e9-b619-02c049fdd00c")
es = Elasticsearch(['https://1bf6b928-7dd1-405f-b615-af9304dd5f8d.a618efcd6c3341158fb843970f0d7edd.databases.appdomain.cloud:31379'], http_auth=('admin', 'BanishCOVID19'), scheme="https", port=31379, ssl_context=es_context)

def populate_elastic_from_file(input_file):
    global es
    f = codecs.open(input_file, "r", "utf8")
    lines = f.readlines()   #reading lines from the file
    f.close()
    #print(type(lines))   type of lines is list
    
    # TODO: What we are doing here?
    #es.indices.delete(index='wikipeople-rgcn', ignore=[400, 404])   #removes document from the index
    
    es_id = 0
    for line in lines:
        line = line.strip()
        json_data = json.loads(line)
        #print(type(json_data))    type is dict
    
        for qid, jd in json_data.items():
            if jd.get("wikidata_qid") is None:
                continue
            # title
            try:
                es_id += 1
                doc = {}
                doc['qid'] = jd['wikidata_qid']
                #doc['wiki_url'] = jd['wiki_url']
                doc['title'] = jd['title']
                doc['text'] = jd['title']
                doc['type'] = "title"
                res = es.index(index="wikipeople-rgcn", id=es_id, body=doc)
            except Exception as e:
                print("Error writing text")
                print(str(e))
                
            #res1=es.get(index='wikipeople-rgcn',doc_type="title",id=es_id)
            #print(len(res1))
            # text
            try:
                #es_id += 1
                doc = {}
                doc['qid'] = jd['wikidata_qid']
                doc['title'] = jd['title']
                #doc['wiki_url'] = jd['wiki_url']
                doc['text'] = jd['text']
                doc['type'] = "text"
                res = es.index(index="wikipeople-rgcn", id=es_id, body=doc)
            except Exception as e:
                print("Errori writing text")
                print(str(e))
                
            
    
            # qid
            try:
                es_id += 1
                doc = {}
                doc['qid'] = jd['wikidata_qid']
                doc['title'] = jd['title']
                #doc['wiki_url'] = jd['wiki_url']
                doc['text'] = jd['first_section']
                doc['type'] = "first_section"
                res = es.index(index="wikipeople-rgcn", id=es_id, body=doc)
            except Exception as e:
                print("Error writing first_section")
                print(str(e))
            
            # infobox
            try:
                if jd.get("infobox") is not None and len(jd.get("infobox")) > 0:
                    a=0
                    for k, v in jd['infobox'].items():
                        es_id += 1
                        doc = {}
                        doc['qid'] = jd['wikidata_qid']
                        doc['title'] = jd['title']
                        #doc['wiki_url'] = jd['wiki_url']
                        doc["text"] = k
                        doc['type'] = "infobox"
                        res = es.index(index="wikipeople-rgcn", id=es_id, body=doc)
            except Exception as e:
                print("Error writing infobox")
                print(str(e))
                continue
            
            
             #sections
            if jd.get('section_by_title') is None:
                continue
            section_by_title_list = jd['section_by_title']
            b=0
            for section_by_title in section_by_title_list:
                if section_by_title.get("text") is not None:
                    try:
                        es_id += 1
                        doc = {}
                        doc['qid'] = jd['wikidata_qid']
                        doc['title'] = jd['title']
                        #doc['wiki_url'] = jd['wiki_url']
                        doc["text"] = section_by_title.get("text") 
                        doc['type'] = "section"
                        res = es.index(index="wikipeople-rgcn", id=es_id, body=doc)
                    except Exception as e:
                        print("Error writing section")
                        continue
#                # subsections
                if section_by_title.get("subsections") is not None:
                    subsections_list = section_by_title.get("subsections")
                    if len(subsections_list) > 0:
                        for subsection_map in subsections_list:
                            if subsection_map.get('text') is not None:
                                try:
                                    es_id += 1
                                    doc = {}
                                    doc['qid'] = jd['wikidata_qid']
                                    doc['title'] = jd['title']
                                    #doc['wiki_url'] = jd['wiki_url']
                                    doc["text"] = subsection_map.get("text")
                                    doc['type'] = "subsection"
                                    res = es.index(index="wikipeople-rgcn", id=es_id, body=doc)
                                except Exception as e:
                                    print("Error writing subsection")
                                    continue
        """sum=0
        for i in range(2,len(data)):
            sum = sum + data[i]
        #print(sum)
        if sum > 0:
            print(data)
            with open('listfile.txt', 'a+') as filehandle:
                filehandle.write('%s\n' % data) """
            # forgot to include categories during extraction
            # TODO - add categories to the index
    
            #if es_id > 10:
            #    break
            
# this program is not threaded, but input files were created that way
#num_threads = 1
#for i in range(0, num_threads):

for i in range(10):
    print(i) 
    input_file = "/Users/abhayms//Documents/ontology-learning-master/data/wikipeople/n-ary_train_qid_details.json." + str(i)
    populate_elastic_from_file(input_file)

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

#threads = []
#for _ in range(10):
 #   t = threading.Thread(target=populate_elastic_from_file,args=(input_file,"Mahatma Gandhi",))
  #  t.start()
   # threads.append(t)

#for thread in threads:
 #   thread.join()



