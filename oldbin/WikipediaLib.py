import wikipedia
import requests
import bs4
import wikipedia
import GoogleLib

def get_wikidata_url_from_wiki_url(wiki_url):
    try:
        html = requests.get(wiki_url)
        b = bs4.BeautifulSoup(html.text, 'lxml')
        h1 = b.find(id="t-wikibase")
        wikibase_item = h1.contents[0]
        wiki_data_url = wikibase_item['href']
    except:
        return ""
    return wiki_data_url

def get_wiki_title_from_wiki_url(wiki_url):
    #print(result["link"])
    html = requests.get(wiki_url)
    b = bs4.BeautifulSoup(html.text, 'lxml')
    h1 = b.find("h1")
    wiki_title = h1.contents[0]
    return wiki_title

def get_title_from_wiki_url_hack(wiki_url):
    if len(wiki_url) < 6:
        return ""
    wiki_title_from_url  = wiki_url.replace("https://en.wikipedia.org/wiki/","")
    wiki_title_from_url = wiki_title_from_url.strip("/")
    wiki_title_from_url = wiki_title_from_url.replace("_"," ")
    return wiki_title_from_url

def wiki_url_matches_title(wiki_url, wiki_title):
    if len(wiki_url) < 6:
        return False
    wiki_title_from_url  = wiki_url.replace("https://en.wikipedia.org/wiki/","")
    wiki_title_from_url = wiki_title_from_url.strip("/")
    wiki_title_from_url = wiki_title_from_url.replace("_"," ")
    if wiki_title == wiki_title_from_url:
        return True

    fetch_wiki_title = get_wiki_title_from_wiki_url(wiki_url)
    if fetch_wiki_title == wiki_title:
        return True 

    return False

def get_wiki_content(wiki_title):
    try:
        if len(wiki_title) < 5:
            return None
        wiki_title_query = "Key (" + wiki_title + ")"
        p = wikipedia.page(title=wiki_title_query,pageid=None,auto_suggest=True,redirect=True,preload=False)
        if wiki_title != p.title:
            return None
        wiki_content = {}
        wiki_content['wiki_url'] = p.url
        wiki_content['outlinks'] = p.links
        wiki_content['categories'] = p.categories
        output_image_urls = []
        try:
            images_urls = p.images
            names = wiki_title.split(" ")
            output_image_urls = []
            for image_url in images_urls:
                flag = False
                for name in names:
                    if len(name) > 4 and name in image_url:
                        flag = True
                        break
                if flag == True:
                    output_image_urls.append(image_url)
                    break
        except:
            output_image_urls = []
        wiki_content['images'] = output_image_urls
        wiki_content['wiki_text'] = p.content
        return wiki_content
    except Exception as e:
        print(str(e))
        print("Error getting wiki content for:", wiki_title.encode('utf-8'))
    return None
