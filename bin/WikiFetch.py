#!/usr/bin/python3
import json
from requests.exceptions import ConnectionError
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

    def __init__(self):
        try:
            self.wikipediaAPI = wikipediaapi.Wikipedia("en")
        except ConnectionError as error:
            print("Not connected to the internet: %s" % error)

    def get_data(self, page_name, wiki_url, wikidata_qid):
        self.wiki = wptools.page(page_name, silent=True)
        self.wikiApi = None
        try:
            self.wikiApi = self.wikipediaAPI.page(page_name)
        except Exception as e:
            print("Error gettig page from wikipediaAPI")
            print(str(e))

        get = None
        try:
            get = self.wiki.get()
        except Exception as e:
            print("Error getting content from wptools")
            print(str(e))
        #get_more = self.wiki.get_more()
        data = {}
        data["wikidata_qid"] = wikidata_qid
        data["wiki_url"] = wiki_url
        try:
            data["title"] = self.wikiApi.title
        except Exception as e:
            try:
                data["title"] = get.data["title"]
            except Exception as e:
                data["title"] = ""
        try:
            data["first_section"] = self.wikiApi.summary
        except Exception as e:
            data["first_section"] = ""
        try:
            data["text"] = self.wikiApi.text
        except Exception as e:
            data["text"] = ""
        try:
            data["infobox"] = get.data["infobox"]
        except Exception as e:
            data["infobox"] = ""
        try:
            data["links"] = get.data["links"]
        except Exception as e:
            data["links"] = ""
            data["links"] = self.wikiApi.links,
            #data["backlinks"] = get.data["backlinks"],
            #data["claims"] = get.data["claims"],
            #data["extext"] = get.data["extext"],
            #data["labels"] = self.dictValues(get.data["labels"]),
            #data["sections"] = self.sectionsDict(self.wikiApi.sections),
            #data["sections_orig"] = self.wikiApi.sections,
            #data["wikitext"] = get.data["wikitext"],
            #data["aliases] = get.data["aliases"],
            #data["label] = get.data["label"],
            #data["description] = get.data["description"],
            #data["assessments"] = get.data["assessments"],

        try:
            data["section_by_title"] = self.sectionByTitle(self.sectionsDict(self.wikiApi.sections))
        except Exception as e:
            data["section_by_title"] = ""
        #data["categories"] = self.wikiApi.categories
        #data["categories"] = [s.replace("Category:", '') for s in get_more.data["categories"]]
        return data

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

    def sectionByTitle(self, sections_dict):
        output_list = []
        for k, v in sections_dict.items():
            #print(k)
            #print(self.wikiApi.section_by_title(k))
            section = str(self.wikiApi.section_by_title(k))
            section = section.replace("\n","||")
            output = {}
            output["section"] = k
            output["text"] = section
            subsections = v
            subsections_list = []
            for k2, v2 in subsections.items():
                subsection = str(self.wikiApi.section_by_title(k2))
                subsection = subsection.replace("\n", "||")
                subsection_map = {}
                subsection_map["subsection"] = k2
                subsection_map["text"] = subsection
                subsections_list.append(subsection_map)
            output["subsections"] = subsections_list
            output_list.append(output)
        return output_list


if __name__ == "__main__":
    WP = wiki()
    data = WP.get_data("Kyrsten_Sinema", "", "")
    WP_JSON = json.dumps(data)
    print(WP_JSON)
