#%% This program collects wikipedia articles for wikidata qids using multiple threads
import threading 
import codecs
import WikipediaLib
from WikiFetch import wiki
import json
from wikidata.client import Client


#%%
qid = "Q275863"
def get_wikipedia_url(qid):
    url = WikipediaLib.get_wikipedia_url_from_wikidata_id(qid)
    print(url)
    return url
#url = get_wikipedia_url(qid)

#%%
def get_wikipedia_title(url):
    title = WikipediaLib.get_title_from_wiki_url_hack(url)
    print(title)
    return title
#title = get_wikipedia_title(url)

#%%
def fetch_wiki(title):
    try:
        wp = wiki(title)
        wp_json = json.dumps(wp.data)
        return wp.data
    except:
        return {}
#wp_data = fetch_wiki(title)
#print(wp_data)

#%%
def thread_task(input_file, output_file): 
    """ 
    task for thread 
    calls increment function 100000 times. 
    """
    #wikipedia_urls = get_wikipedia_url_from_wikidata_id(qid)
    print(input_file)
    f = codecs.open(input_file, "r", "utf8")
    lines = f.readlines()
    f.close()
    #print(len(lines))
    wp = wiki()
    for qid in lines:
        qid = qid.strip()
        wp_key = qid
        wp_value = {}
        try:
            try:
                url = WikipediaLib.get_wikipedia_url_from_wikidata_id(qid)
            except:
                url = ""
            try:
                title = WikipediaLib.get_title_from_wiki_url_hack(url)
            except:
                try:
                    title = WikipediaLib.get_wiki_title_from_wiki_url(url)
                except:
                    title = ""
            if len(title) > 0:
                wp_value = wp.get_data(title, url, qid)
        except Exception as e:
            print(str(e))

        try:
            wp_data = {}
            wp_data[wp_key] = wp_value
            wp_json = json.dumps(wp_data)
            ofs = codecs.open(output_file, "a+", "utf8")
            ofs.write(wp_json)
            ofs.write("\n")
            ofs.flush()
            ofs.close()
        except Exception as e:
            print(str(e))


  
#%%
client = Client()
#entity = client.get('Q20145', load=True)
#print(entity)
#print(entity.description)

# takes a wikipeople file as input
# note the portion where we only use presumed qids of people and not all entities
def get_wikidata_qids(relations_file, input_file, output_file):
    #%%
    f = open(input_file, "r")
    lines = f.readlines()
    f.close()
    
    pf = open(relations_file, "r")
    plines = pf.readlines()
    pf.close()
    relations_map = {}
    for pline in plines:
        parts = pline.split("\t")
        if len(parts) < 2:
            continue
        pid = parts[0]
        if relations_map.get(pid) is None:
            relations_map[pid] = parts[1]
        
    #%%
    qid_map = {}
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
                    if i != 0 and relations_map.get(pid) is None:
                        continue
                    if qid_map.get(qid) is None:
                        qid_map[qid] = ""
                    i += 1
                except Exception as e:
                    print(str(e))
                    continue
        except Exception as e2:
            print(str(e2))
            continue
    output_list = list(qid_map.keys())
    output_list.sort()

    ofs1 = open(output_file, "w")
    for qid in output_list:
        ofs1.write(qid + "\n")
    ofs1.close()

def divide_in_chunks(lines, parts_len, input_file, num_threads):
    j = 0
    for i in range(0, len(lines), parts_len):  
        write_lines = lines[i:i + parts_len]
        temp_file = input_file + "." + str(j)
        f = codecs.open(temp_file, "w", "utf8")
        for write_line in write_lines:
            f.write(write_line)
        f.close()
        j+=1
    if j > num_threads:
        print("error")

def main_task(num_threads, input_file, output_file): 
    threads = []
    # creating threads 
    f = open(input_file,"r")
    lines = f.readlines()
    f.close()
    num_lines = len(lines)
    parts_len = int(num_lines / num_threads)
    if parts_len < 1:
        parts_len = 1
    print("qids per file:")
    print(parts_len)
    divide_in_chunks(lines, parts_len, input_file, num_threads)

    for i in range(0, num_threads):
        t = threading.Thread(target=thread_task, args=(input_file + "." + str(i), output_file + "." + str(i),))
        threads.append(t)
  
    # start threads 
    for t in threads:
        t.start()

    # wait until threads finish their job 
    for t in threads:
        t.join()

#%%
relations_file = "./data/wikipeople/wiki_people_relations.txt"
input_file = "./data/wikipeople/n-ary_train.json"
qids_file = "./data/wikipeople/n-ary_train_qids.txt" 
output_file = "./data/wikipeople/n-ary_train_qid_details.json"
#get_wikidata_qids(relations_file, input_file, qids_file)
main_task(10, qids_file, output_file)
