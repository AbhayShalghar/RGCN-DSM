import json
import codecs
from copy import deepcopy

dataset_list = []
count = 0

def process_file(input_file):
    global count
    with codecs.open(input_file, "r", "utf8") as f:
        docs = f.readlines()
        for doc in docs:
           data = json.loads(doc)
           for cluster_name, d in data.items():
              doc_map = {}
              doc_map["doc"] = cluster_name

              # first populating doc_map which we'll copy to what we write
              for k, v in d.items():
                 if k == "wikidata_qid":
                     doc_map["entity_label"] = v
                 if k == "wiki_url":
                     doc_map["wiki_url"] = v
                 if k == "title":
                     doc_map["title"] = v

              # now reading again to write doc structure
              for k, v in d.items():
                 if k == "title":
                     doc_map["title"] = v
                     title_map = deepcopy(doc_map)
                     title_map["doc_type"] = "title"
                     title_map["text"] = v
                     title_map["id"] = count
                     dataset_list.append(title_map)
                     count+=1
                 if k == "first_section":
                     intro_map = deepcopy(doc_map)
                     intro_map["doc_type"] = "first_section"
                     intro_map["text"] = v
                     intro_map["id"] = count
                     dataset_list.append(intro_map)
                     count+=1
                 # this is original text, we should compare content with this text
                 #if k == "text":
                 #    doc_map["text"] = v
                 if k == "infobox" and v is not None and len(v) > 0:
                     infobox = v
                     try:
                         for info_type, info in infobox.items():
                             infobox_map = deepcopy(doc_map)
                             infobox_map["doc_type"] = "infobox"
                             infobox_map["text"] = info
                             infobox_map["info_type"] = info_type
                             infobox_map["id"] = count
                             dataset_list.append(infobox_map)
                             count+=1
                     except Exception as e:
                         print(str(e))
                 if k == "links":
                     links = v
                     for link in links:
                         link_map = deepcopy(doc_map)
                         link_map["doc_type"] = "link"
                         link_map["text"] = link
                         link_map["id"] = count
                         dataset_list.append(link_map)
                         count+=1
                 if k == "section_by_title":
                    sections_list = v
                    for section in sections_list:
                        #******* section title *******
                        section_title = section["section"]
                        #******* section text begin *******
                        section_text = section["text"]
                        subsections = section["subsections"]
                        for subsection in subsections:
                            #******* subsection title *******
                            subsection_title = subsection["subsection"]
                            #******* subsection text begin *******
                            # paragraphs seems to just replicate the text here
                            subsection_text = subsection["text"]
                            #print(subsection_text)
                            #******** subsection text end ******
                            #******* subsection paragraphs begin *******
                            subsection_paragraphs = subsection_text.split("||")
                            for ssp in subsection_paragraphs:
                                ssp = ssp.strip()
                                if len(ssp) < 3:
                                    continue
                                if "Subsections (" in ssp:
                                    continue
                                if "Section: " in ssp:
                                    continue
                                ss_map = deepcopy(doc_map)
                                ss_map["section"] = section_title
                                ss_map["subsection"] = subsection_title
                                ss_map["doc_type"] = "subsection"
                                ss_map["text"] = ssp
                                ss_map["id"] = count
                                dataset_list.append(ss_map)
                                count+=1
                            #******** subsection paragraphs end ******
                        if len(subsections) < 1:
                            #******* section paragraphs begin *******
                            section_paragraphs = section_text.split("||")
                            for sp in section_paragraphs:
                                sp = sp.strip()
                                if len(sp) < 3:
                                    continue
                                if "Subsections (" in sp:
                                    continue
                                if "Section: " in sp:
                                    continue
                                s_map = deepcopy(doc_map)
                                s_map["section"] = section_title
                                s_map["doc_type"] = "section"
                                s_map["text"] = sp
                                s_map["id"] = count
                                dataset_list.append(s_map)
                                count+=1
                            #******* section paragraphs end *******
                        #******** section text end ******")
    
for i in range(10):
    file_name = "/Users/abhayms//Documents/ontology-learning-master/data/wikipeople/n-ary_train_qid_details.json." + str(i)
    process_file(file_name)

with codecs.open("/Users/abhayms//Documents/ontology-learning-master/data/wikipeople/tacred_dataset.json", "w", "utf8") as ofs:
    json.dump(dataset_list, ofs, indent=4) 
