#!/usr/bin/python3
from requests.exceptions import ConnectionError
import json
import wikipediaapi
import wptools

'''
Wiki can be used as a wrapper around the wptools library.
Its task is to fetch, filter, and format the requested data from a Wikipedia.

{
  title: str,
  aliases: list,
  label: str,
  description: str,
  first_section: str,
  text: str,
  infobox: dict,
  assessments: dict <dict>,
  links: list,
  labels: list,
  sections: list,
  categories:
}
'''
class wiki():

    def __init__(self, page_name):
        self.page_name = page_name
        try:
            self.wiki = wptools.page(page_name)
            self.wikiApi = wikipediaapi.Wikipedia("en")
            self.wikiApi = self.wikiApi.page(page_name)
        except ConnectionError as e:
            print("Not connected to the internet: %s" % e)
        get = self.wiki.get()
        get_more = self.wiki.get_more()
        self.data = {
                "title": get.data["title"],
                "aliases": get.data["aliases"],
                "label": get.data["label"],
                "description": get.data["description"],
                "first_section": self.wikiApi.summary,
                "text": self.wikiApi.text,
                "infobox": get.data["infobox"],
                "assessments": get.data["assessments"],
                "links": get.data["links"],
                "labels": self.dictValues(get.data["labels"]),
                "sections": self.sectionsDict(self.wikiApi.sections),
                "categories": [s.replace("Category:", '') for s in get_more.data["categories"]]
        }

    def sectionsDict(self, sections, level=0):
        sDict = {}
        for s in sections:
            sDict[s.title] = self.sectionsDict(s.sections, level + 1)
        return sDict

    def dictValues(self, d):
        valueList = []
        for key,value in d.items():
            valueList.append(value)
        return valueList


if __name__ == "__main__":
    wp = wiki("Kyrsten_Sinema")
    wp_json = json.dumps(wp.data)
    print(wp_json)

