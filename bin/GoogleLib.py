"""Example of Python client calling Knowledge Graph Search API."""
import json
import urllib.parse
import urllib.request
from googleapiclient.discovery import build

my_api_key = "AIzaSyDv0xz6bnl-pFzcmn3-NmlNT662HQmTgos"
my_cse_id = "014907431480918052286:l-h94audtze"

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    if res.get('items') is None:
        return []
    return res['items']

def get_wiki_url_from_google(query):

    results= google_search(query,my_api_key,my_cse_id,num=10)

    # firstly it has to be from wikipedia
    for result in results:
        if 'en.wikipedia.org' not in result['link']:
            continue
        return result["link"]
    print("No wiki url found from google.")
    return ""


#api_key = open('.api_key').read()
if __name__ == "__main__":
    query = 'Boris Johnson'
    service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
    params = {
        'query': query,
        'limit': 10,
        'indent': True,
        'key': my_api_key,
    }
    url = service_url + '?' + urllib.parse.urlencode(params)
    response = json.loads(urllib.request.urlopen(url).read())
    for element in response['itemListElement']:
      print(element)
      break

