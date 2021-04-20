#%%
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

def populate_elastic_from_file(input_file,title):
    global es
    f = codecs.open(input_file, "r", "utf8")
    lines = f.readlines()
    f.close()
    
    # TODO: What we are doing here?
    es.indices.delete(index='wikipeople-rgcn', ignore=[400, 404])
    
    es_id = 0
    for line in lines:
        line = line.strip()
        json_data = json.loads(line)
    
        for qid, jd in json_data.items():
            data = []
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
                z = jd['title'].count(title)
                #print('title '+str(z))
                data.append(title)
                data.append(jd['title'])
                data.append(z)
                res = es.index(index="wikipeople-rgcn", id=es_id, body=doc)
            except Exception as e:
                print("Error writing text")
                print(str(e))
                
            #res1=es.get(index='wikipeople-rgcn',doc_type="title",id=es_id)
            #print(len(res1))
            z=0
            k=0
            # text
            try:
                #es_id += 1
                doc = {}
                doc['qid'] = jd['wikidata_qid']
                doc['title'] = jd['title']
                #doc['wiki_url'] = jd['wiki_url']
                doc['text'] = jd['text']
                doc['type'] = "text"
                z = jd['text'].count(title)
                #print('text '+str(z))
                data.append(z)
                res = es.index(index="wikipeople-test", id=es_id, body=doc)
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
                z = jd['first_section'].count(title)
                #print('first_section '+str(z))
                data.append(z)
                res = es.index(index="wikipeople-test", id=es_id, body=doc)
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
                        z = jd['infobox'][k].count(title)
                        a = a+z
                        res = es.index(index="wikipeople-test", id=es_id, body=doc)
                    #print('infobox '+str(a))
                    data.append(a)
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
                        z = section_by_title.get("text").count(title)
                        b=b+z
                        res = es.index(index="wikipeople-test", id=es_id, body=doc)
                    except Exception as e:
                        print("Error writing section")
                        continue
#                # subsections
                if section_by_title.get("subsections") is not None:
                    subsections_list = section_by_title.get("subsections")
                    #print(len(subsections_list))
                    #z = section_by_title.get("subsections").count(jd['title'])
                    #print(z)
                    #b = b+z
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
                                    z = subsection_map.get("text").count(title)
                                    b = b+z
                                    res = es.index(index="wikipeople-test", id=es_id, body=doc)
                                except Exception as e:
                                    print("Error writing subsection")
                                    continue
            #print('section '+str(b))
            data.append(b)
        sum=0
        for i in range(2,len(data)):
            sum = sum + data[i]
        #print(sum)
        if sum > 0:
            print(data)
            with open('listfile_1.txt', 'a+') as filehandle:
                filehandle.write('%s\n' % data)
            # forgot to include categories during extraction
            # TODO - add categories to the index
    
            #if es_id > 10:
            #    break
            
# this program is not threaded, but input files were created that way
#num_threads = 1
#for i in range(0, num_threads):

i=1   
input_file = "/Users/abhayms//Documents/ontology-learning-master/data/wikipeople/n-ary_train_qid_details.json." + str(i)
#populate_elastic_from_file(input_file,"Mahatma Gandhi")
if __name__ == "__main__":
    t1 = multiprocessing.Process(target=populate_elastic_from_file,args=(input_file,"Mahatma Gandhi",))
    t2 = multiprocessing.Process(target=populate_elastic_from_file,args=(input_file,"Narendra Modi",))
    t3 = multiprocessing.Process(target=populate_elastic_from_file,args=(input_file,"Jawaharlal Nehru",))
    t4 = multiprocessing.Process(target=populate_elastic_from_file,args=(input_file,"Indira Gandhi",))
    t5 = multiprocessing.Process(target=populate_elastic_from_file,args=(input_file,"Barack Obama",))

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



