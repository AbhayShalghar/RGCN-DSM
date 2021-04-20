#%%
from datetime import datetime
import codecs
import json
import pandas as pd
import time
import sys
import traceback
from os import path
import WikipediaLib
import Person
import GoogleLib

now = datetime.now()
dt_string = now.strftime("%Y%m%d%H%M%S")

def verify_wiki_title(query_str, wiki_title):
    return True
    if len(wiki_title) < 6:
        return False
    ns = query_str.lower()
    wt = wiki_title.lower()
    if ns not in wt and wt not in ns:
        # if all words in title are present in the name, fine
        parts = wt.split(' ')
        for part in wt.split('-'):
            parts.append(part)
        for part in parts:
            if part not in ns:
                return False
    return True


def get_wiki_url_and_title(query_str):
    wiki_url = ""
    wiki_title = ""
    query = query_str + " wikipedia"
    wiki_url = GoogleLib.get_wiki_url_from_google(query)
    if len(wiki_url) > 5:
        wiki_title = WikipediaLib.get_wiki_title_from_wiki_url(wiki_url)
    if not Person.isPerson(wiki_title):
        return "",""

    wiki_title_from_url = WikipediaLib.get_title_from_wiki_url_hack(wiki_url)
    flag = Person.isPerson(wiki_title_from_url)
    if flag == False:
        return "",""

    #print(wiki_title)
    return wiki_url, wiki_title


# you can remove the cache files, it was done for another use-case
# this populates 3 intermediate files. entity_names may not be relevant
# wiki_title and wiki_url you can retain
def get_wiki_text(data_dir, input_file, output_file):
    wiki_not_found_cache_file = data_dir + "/wiki_not_found_cache.json"
    wiki_pages_cache_file = data_dir + "/wiki_pages_cache.json"
    wiki_pages_cache = {}
    wiki_not_found_cache = {}
    
    if path.exists(wiki_pages_cache_file):
        f = codecs.open(wiki_pages_cache_file, "r", "utf8")
        wiki_pages_cache = json.load(f)
        f.close()
        
    if path.exists(wiki_not_found_cache_file):
        f = codecs.open(wiki_not_found_cache_file, "r", "utf8")
        wiki_not_found_cache = json.load(f)
        f.close()

    entity_names_file = data_dir + "/entity_names.json"
    entity_names_file = entity_names_file.replace(" ", "_")
    wiki_titles_file = data_dir + "/wiki_titles.json"
    wiki_titles_file = wiki_titles_file.replace(" ", "_")
    wiki_url_file = data_dir + "/wiki_urls.json"
    wiki_url_file = wiki_url_file.replace(" ", "_")
    
    if path.exists(entity_names_file):
        f = codecs.open(entity_names_file, "r", "utf8")
        entity_names_map = json.load(f)
        f.close()
    else:
        entity_names_map = {}

    if path.exists(wiki_titles_file):
        f = codecs.open(wiki_titles_file, "r", "utf8")
        wiki_titles_map = json.load(f)
        f.close()
    else:
        wiki_titles_map = {}
    
    # no need to find wiki_urls if already present
    if path.exists(wiki_url_file):
        f = codecs.open(wiki_url_file, "r", "utf8")
        wiki_url_map = json.load(f)
        f.close()
    else:
        wiki_url_map = {}
    
    # no need to get wiki text if already present
    if path.exists(output_file):
        f = codecs.open(output_file, "r", "utf8")
        json_data = json.load(f)
        f.close()
    else:
        json_data = {}
    
    # this is where we need to read the tweets file
    f = codecs.open(input_file, "r", "utf8")
    input_json = json.load(f)
    f.close()
    
    count = 1
    for tweet in input_json:
        ##############################################
        # need to populate the query_str as required #
        ##############################################
        query_str = ""
        try:
            if wiki_url_map.get(query_str) is not None and len(wiki_url_map[query_str]) > 5:
                wiki_url = wiki_url_map[query_str]
                if wiki_titles_map.get(query_str) is not None and len(wiki_titles_map[query_str]) > 5:
                    wiki_title = wiki_titles_map[query_str]
                else:
                    wiki_title = WikipediaLib.get_wiki_title_from_wiki_url(wiki_url)
            else:
                wiki_url, wiki_title = get_wiki_url_and_title(query_str)
                if len(wiki_title) < 6:
                    wiki_titles_map[query_str] = ""
                    continue
                if len(wiki_url) < 6:
                    wiki_url_map[query_str] = ""
                    continue
                #print(query)
                #print(wiki_url)

                flag = verify_wiki_title(query_str, wiki_title)
                if flag == False:
                    if wiki_url_map.get(query_str) is not None:
                        print("Incorrect wiki article. Ignoring.", query_str.encode('utf-8'), " not in ", wiki_title.encode('utf-8'))
                        del wiki_url_map[query_str]
                    if json_data.get(wiki_url) is not None:
                        json_element = json_data.get(wiki_url)
                        query_str = json_element["name"]
                        wiki_title = json_element["wiki_title"]
                        if query_str not in wiki_title:
                            del json_data[wiki_url]
                            print("Incorrect wiki article. Deleting wiki_text for this wiki_url too:", wiki_url.encode('utf-8'))
    
                    # eventually merge this wiki_title with wiki_url_map
                    if wiki_titles_map.get(query_str) is not None:
                        temp_title = wiki_titles_map[query_str]
                        if len(temp_title) > 1:
                            wiki_url, wiki_title = get_wiki_url_and_title(temp_title)
    
            if len(wiki_title) < 6:
                wiki_titles_map[query_str] = ""
                continue
            wiki_titles_map[query_str] = wiki_title

            if len(wiki_url) < 6:
                wiki_url_map[query_str] = ""
                continue
            wiki_url_map[query_str] = wiki_url

            if json_data.get(wiki_url) is not None:
                #print("wiki text for url already exists.", wiki_url) 
                # temporary code begin
                wiki_content = json_data.get(wiki_url)
                if wiki_pages_cache.get(wiki_title) is None:
                    wiki_pages_cache[wiki_title] = wiki_content
                # temporary code end
                continue
    
            if wiki_pages_cache.get(wiki_title) is not None:
                wiki_content = wiki_pages_cache.get(wiki_title)
            else:   
                if wiki_not_found_cache.get(wiki_title) is not None:
                     continue
                wiki_content = WikipediaLib.get_wiki_content(wiki_title)
                if wiki_content is None or wiki_content.get('wiki_url') is None:
                    wiki_not_found_cache[wiki_title] = 1
                    continue
                wiki_pages_cache[wiki_title] = wiki_content

                flag = Person.isPersonWikiContent(wiki_title, wiki_content)
                if flag == False:
                    continue

            wiki_url = wiki_content['wiki_url']
            wiki_outlinks = wiki_content['outlinks']
            wiki_categories = wiki_content['categories']
            wiki_images = wiki_content['images']
            wiki_text = wiki_content['wiki_text']

            json_element = {}
            json_element["name"] = query_str
            json_element["wiki_url"] = wiki_url
            json_element["wiki_title"] = wiki_title
            json_element["wiki_outlinks"] = wiki_outlinks
            json_element["wiki_categories"] = wiki_categories
            json_element["wiki_images"] = wiki_images
            json_element['wiki_text'] = json.dumps(wiki_text)
            json_data[wiki_url] = json_element
            time.sleep(2)
            count += 1
            #if count > 10:
            #    break
        except Exception as e:
            error = str(e)
            print(error.encode('utf-8'))
            tb = traceback.format_exc()
            print(tb.encode('utf-8'))
            continue
    
    #%%
    with codecs.open(output_file, "w", "utf8") as f:
        json.dump(json_data, f, indent=4, sort_keys=True)

    with codecs.open(entity_names_file, "w", "utf8") as f:
        json.dump(entity_names_map, f, indent=4, sort_keys=True)

    wiki_url_list = list(wiki_url_map.keys())
    for query_str in wiki_url_list:
        if entity_names_map.get(query_str) is None:
            del wiki_url_map[query_str]

    for query_str in list(entity_names_map.keys()):
        if wiki_url_map.get(query_str) is None:
            wiki_url_map[query_str] = ""
    
    with codecs.open(wiki_url_file, "w", "utf8") as f:
        json.dump(wiki_url_map, f, indent=4, sort_keys=True)

    wiki_titles_list = list(wiki_titles_map.keys())
    for query_str in wiki_titles_list:
        if entity_names_map.get(query_str) is None:
            del wiki_titles_map[query_str]
    
    for query_str in list(entity_names_map.keys()):
        if wiki_titles_map.get(query_str) is None:
            wiki_titles_map[query_str] = ""

    with codecs.open(wiki_titles_file, "w", "utf8") as f:
        json.dump(wiki_titles_map, f, indent=4, sort_keys=True)

    with codecs.open(wiki_not_found_cache_file, "w", "utf8") as f:
        json.dump(wiki_not_found_cache, f, indent=4, sort_keys=True)
    
    with codecs.open(wiki_pages_cache_file, "w", "utf8") as f:
        json.dump(wiki_pages_cache, f, indent=4, sort_keys=True)

# main program starts here
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: " + sys.argv[0] + " <data_dir> <input_file> <output_file>")
        sys.exit(0)
    
    data_dir = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    get_wiki_text(data_dir, input_file, output_file)
