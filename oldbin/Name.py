
def get_name_from_wiki_title(wiki_title):
    # if the wiki title has a comma, it's not very useful
    if "," in wiki_title:
        parts = wiki_title.split(",")
        name = parts[0]
        if len(name) > 3:
            return name
    # getting name from wiki_title
    parts = wiki_title.split("(")
    name = parts[0]
    name = name.strip()
    return name
