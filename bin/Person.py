import codecs
import re

patterns = [r',', r' born ', r' of ', r' and ', r'List ', r':', r'Election', r'Representatives', r'Committee', r'Europe', r'United States', r'Congress', r'Army', r'Member', r' for ', r'Cabinet', r'Ministry', r'Minister', r' the ', r'The ', r'Constituency', r'Party', r'of india', r'of Australia', r'of New Zealand', r'of Israel', r'of Singapore', r'of Canada', r'Assembly', r'Film', r'Morcha', r'School', r'\bthe\b', r'League', r'Team', r'University', r'Government', r'Secretary', r'Speaker', r'Proposition', r'Legislature', r'Senate', r'Parliament', r'Greens', r'Authority', r'Disambiguation', r'Council', r'Number', r'College', r'\bTV ', r' Medal\b', r'\bWar\b', r'\bGuards\b', r'\bTax\b', r'Comics',r'Wikipedia', r'Template', r'Category', r'Dictionary', r'Economic', r'Trade', r'History', r'International', r'District', r'Leader', r' Act']
regex_pattern = '|'.join(patterns)

more_patterns = "Australian| News|Police|Marriage|Federation|Terrorist|Province|Military|Wagga|South Australia|Corporation|Commission| Line| Day |Electoral|Publishing|Gazette|Energy|Scholar|Officer|Votes|Newspaper|Office|Alliance|Veterans|Daily|Ceremony|Air Force|Naval |Fruit| Golf|Political|Family|National|Company|Magazine|Conservative|Student|American|Baptist|Social|Website|Hospital|Officer|Executive| Base|Science|Shooting|Beach|Administration|Industry|Amendment|Journal|Crisis|Banking|Court |Attorney|Railway|Rail |Adolf Hitler|Organization|Agenda|Center|County|Church| Press|Queen |Technology|Federal|Association| & |Foundation|Bureau|Media|America|Climate|Union|Supreme|River|Weekly|Irish|State|Program|Fund|Conference|Reservation|People|Pacific|Broadcasting|Left|Democrat|Republican|Bombing|County|Sheriff|United|Zealand|North|Royal|Group|Relations|Institute|East |West |Bank|First|General|World|Service|Language|City|Court|Indian|Centre|Football|Israel|Society|Operation|Health|Club|Corps|Central|Academy|Washington|Trust|Political|Nations|London|Pakistan|movement|Radio|massacre|Street|Civil|Research|Board|Award|Kingdom|attack|Navy|Business|Singapore|Northern|Station|Nuclear|Network|Island|Development|America|Chinese|Animal|Command|Financial|Liberal|Intelligence|English|Project|Rights|Southern|Republic|Country|Campaign|German|Ltd|Security|system|Toronto|Special|Russian|Museum|Life|Capital|Management|Independent|Station|Degree|Report|Review|Library|Labour|England|Airport|Cancer|Memorial|California|Socialism|Department|Freedom|Division|Defence|Cross|BBC|Conflict|Science|Insurance|Castle|Protection|Lieutenant|Youth|Unit|Same-sex|Regiment|Marine |Nation|Environmental|Coalition|Municipal|Revolution|New |News | Australia| F.C.| Times| Festival| Institution| LLC| Treaty| Limited| Cup|Tribunal|Administrative|Extremism|Terror|Scheme| Post| House| Marathon|British|Port "

regex_pattern += '|' + more_patterns
compiled_regex_pattern = re.compile(regex_pattern)

name_list = ['de','van','da','e','el','bin','al','ad','i','den','du','le','ul','ur','ud', 'von', 'dos']


number_pattern = "[0-9]+"
compiled_number_pattern = re.compile(number_pattern)

def isPerson(first_hop_orig):
    first_hop = first_hop_orig.lower()
    # we don't want non-people wiki titles as entities
    if ('politician)' in first_hop or 'er)' in first_hop) and 'born ' not in first_hop and 'died ' not in first_hop:
        return True

    parts = first_hop_orig.split("(")

    # need the portion before the paranthesis, if any
    parts_str = parts[0]
    parts = parts_str.split(",")
    parts_str = parts[0]

    parts_str = parts_str.strip()

    parts = parts_str.split(" ") 
    if len(parts) <= 1 and '-' not in parts_str:
        #print("length:", len(parts))
        return False
    for part in parts:
        try:
            first_letter = part[0]
            if first_letter.islower():
                if len(part) > 3 and '-' not in part and '%' not in part:
                    #print(part, "longer than 3")
                    return False
                if part not in name_list:
                    #print(part, "not in name list")
                    return False
                #mentions = re.search(compiled_name_pattern, parts_str)
                #if mentions is None:
                #    return False
        except Exception as e:
            print(str(e))
   
    mentions = re.search(compiled_regex_pattern, parts_str)
    if mentions is not None:
        #print(mentions)
        return False

    mentions = re.search(compiled_number_pattern, parts_str)
    if mentions is not None and '%' not in parts_str:
        #print(mentions)
        return False

    return True

positive_patterns = "births|deaths|people|politicians|actors|civil servants"
compiled_positive_pattern = re.compile(positive_patterns, re.IGNORECASE)

# must use negative patterns after positive patterns
negative_patterns = "establishments|companies|plays|works|hosptial|building|established|brands|television series|films|towns|cities|History of"
compiled_negative_pattern = re.compile(negative_patterns, re.IGNORECASE)
def isPersonWikiContent(wiki_title, wiki_content):
    categories = wiki_content['categories']
    for category in categories:
        category = category.lower()
        mentions = re.search(compiled_positive_pattern, category)
        if mentions is not None:
            return True 
        mentions = re.search(compiled_negative_pattern, category)
        if mentions is not None:
            return False

    return True

