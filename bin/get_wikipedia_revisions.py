#%%
#!/usr/bin/python3

"""
    get_pages_revisions.py

    MediaWiki API Demos
    Demo of `Revisions` module: Get revision data with content for pages
    with titles [[API]] and [[Main Page]]

    MIT License
"""

import requests
import codecs

title = "Narendra Modi"
S = requests.Session()

URL = "https://en.wikipedia.org/w/api.php"

PARAMS = {
    "action": "query",
    "prop": "revisions",
    "titles": title,
    "rvprop": "timestamp|user|comment|content",
    "rvslots": "main",
    "formatversion": "2",
    "format": "json"
}

R = S.get(url=URL, params=PARAMS)
DATA = R.json()

PAGES = DATA["query"]["pages"]

results_map = {}
results_map[title] = []
for page in PAGES:
    #print(page)
    print(type(page["revisions"]))
    for revision in page["revisions"]:
        for k, v in revision.items():
            if k == "slots":
                for x, y in v.items():
                    print(y['content'])
    #results_map[title].append(page["revisions"])
#of = codecs.open("./data/wikipeople_page_revisions.json", "w", "utf8")
#json.dump(results_map, of)
#of.close()


#%%
