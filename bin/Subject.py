#%%
import re
annotations_map = {
    "Jewish" : "Judaism",
    "rabbi" :  "Judaism",
    "Jews" :  "Judaism",
    "Hindu" : "Hinduism",
    "Catholic" : "Christianity",
    "Muslim" : "Islam",
    "Shia_" :  "Islam",
    "Islam" :  "Islam",
    "Sunni_" :  "Islam",
    "Jains" : "Jainism",
    "Ahmadi" :  "Islam",
    "atheist" : "Atheist",
    "agnostic" : "Agnostic",
    "Mormon" :  "Christianity",
    "Yazidi" : "Yazidi",
    "Buddhist" : "Buddhist",
    "Judaism" :  "Judaism",
    "Presbyterian" :  "Christianity",
    "Zoroastrian" : "Zoroastrian", 
    "Mennonite" :  "Christianity",
    "Lutheran" :  "Christianity",
    "Episcopal" :  "Christianity",
    "Church" :  "Christianity",
    "Jehovah" :  "Christianity",
    "Protestant" :  "Christianity",
    "Pentecostal" :  "Christianity",
    "Confucianism" : "Other",
    "Quakers" : "Other",
    "Evangelical" :  "Christianity",
    "Wahhabi" :  "Islam",
    "Māori_religion" : "Other",
    "Scientology_officials" : "Other",
    "Christian" :  "Christianity",
    "Bishops" :  "Christianity",
    "Baptist" :  "Christianity",
    "Methodism" :  "Christianity",
    "Methodists" :  "Christianity",
    "religious" : "Other",
    "Sikhs" : "Sikhism",
    "Anglican" :  "Christianity",
    "Chaplains" : "Christianity",
    "_female" : "Female",
    "women" :  "Female",
    "Female" :  "Female",
    "Male" : "Male",
    "_male" : "Male",
    "actresses" : "Female",
    "Actresses" : "Female",
    "mistresses" : "Female",
    "Transgender" : "Other",
    "ladies" : "Female",
    "gents" : "Male",
    "men" :   "Male",
    "Intersex_": "Other",
    "Gay_" : "Gay",
    "_players" : "Sports",
    "Volleyball" : "Sports",
    "swimmers" : "Sports",
    "rowers" : "Sports",
    "skating" : "Sports",
    "sport" : "Sports",
    "Soccer" : "Sports",
    "football" : "Sports",
    "runners" : "Sports",
    "boxers" : "Sports",
    "athletes" : "Sports",
    "Lacrosse" : "Sports",
    "boxers" : "Sports",
    "rugby" : "Sports",
    "cricketer" : "Sports",
    "basketball" : "Sports",
    "baseball" : "Sports",
    "tennis" : "Sports",
    "chess" : "Sports",
    "golf" : "Sports",
    "_players" : "Sports",
    "Olympic" : "Sports",
    "Sportspeople" : "Sports"
}

#%%
text = "Category:Nova_High_School_alumni"
patterns = {
    "ignore" : "(History_of|Participants_|_uncertain|_family|_unknown|Articles|_missing|Living_people)",
    "duration" : "(\d\d\d\d_births|\d\d\d\d_deaths|(\d\d(st|nd|rd|th)-century))",
    "deathCause": "Deaths_from_",
    "party" : "([^\"]*)(political_party)|Democrats|Republicans",
    "location" : "(People_from_)([^\"]*)",
    "religion" : "Jewish|rabbi|Jews|Hindu|Catholic|Muslim|Shia_|Islam|Sunni_|Jains|Ahmadi|atheist|agnostic|Mormon|Yazidi|Buddhist|Judaism|Presbyterian|Zoroastrian|Mennonite|Lutheran|Episcopal|Church|Jehovah|Protestant|Pentecostal|Confucianism|Quakers|Evangelical|Wahhabi|Māori_religion|Scientology_officials|Christian|Bishops|Baptist|Methodism|Methodists|religious|Sikhs|Anglican|Chaplains",
    "almaMater" : "([^\"]*)(_alumni)|(Alumni_of_)([^\"]*)|(People_educated_from_)([^\"]*)",
    "sexualOrientation" : "Gay_|LGBT|Lesbian",
    "nationality" : "Norwegian|Hungarian|Spanish|Greek|Moroccan|Israeli|Ghanaian|Finnish|New_Zealand|Czech|Nepalese|Kazakhstani|German|Soviet|Italian|Algerian|Pakistani|Japanese|Belizean|South_Korean|Uruguayan|Colombian|Egyptian|Moldovan|Romanian|Austrian|South_African|Russian|Mexican|Filipino|Argentine|Peruvian|Tunisian|Portuguese|Vanuatuan|Brazilian|North_Korean|Lithuanian|Ukrainian|Sri_Lankan|Belgian|citizens|emigrants|Jordanian|American|Malaysian|Polish|Scottish|Guatemalan|French|British|Slovak|Australian|Swedish|Irish|Turkish|Iranian|English|Croatian|Serbian|Dutch|Danish|Bulgarian|Yugoslav|Somali|Canadian|Icelandic|Indian|Vietnamese",
    "award" : "winners|award|prize|medalists|recipients",
    "profession" : "farmers|poets|historians|music_directors|mathematicians|inventors|novelists|_players|curators|entertainers|film_producers|photographers|presenters|Marines|commentators|announcers|executives|Opticians|economists|referees|ministers|educators|workers|researchers|designers|Police|artists|writers|painters|directors|actors|physicians|priests|television_producers|activists|Performers|Permanent_Secretaries|biologists|Secretaries|Councillors|scholars|drivers|generals|Academics|_MLAs|Ambassadors|chairmen|Philosophers|civil_servants|playwrights|choreographers|dancers|actresses|engineers|chemists|doctors|teachers|lawyers|singers|critics|businesspeople|psychologists|scientists|journalists|architects|judges|composers|broadcasters|faculty|musicians|Soldiers|Navy|Military|Generals|Governors|Princes_|Sheriffs|Presidents|Prime_Ministers|Politicians|_MPs|Mayor|Senator|Volleyball|swimmers|rowers|skating|sport|Soccer|football|runners|boxers|athletes|Lacrosse|boxers|rugby|cricketer|basketball|baseball|tennis|chess|golf|_players|Olympic|Sportspeople",
    "gender" : "_female|women|Female|Male|_male|actresses|mistresses|Transgender|ladies|gents|men|Intersex_",
    "language" : "language|Korean|Welsh|Flemish|Malayalam|Persian|Hindi|tamil"
}

#%%
def get_attributes(text):
    global annotations_map
    if "Category:" in text:
        text = text.split(":")[1]
    #%%
    attributes = []
    for relation, pattern_str in patterns.items():
        if "ignore" in relation:
            continue
        pattern = re.compile(pattern_str, re.IGNORECASE)
        output = re.search(pattern, text)
        annotation = ""
        try:
            if output is not None:
                if output.group is not None:
                    annotation = output.group(0)
                    if "location" in relation and "People_from_" in annotation:
                        annotation = output.group(2)
                    if "almaMater" in relation and "_alumni" in annotation:
                        annotation = output.group(1) 
                    if "almaMater" in relation and "Alumni_of_" in annotation:
                        annotation = output.group(2)
                    if "almaMater" in relation and "People_educated_from_" in annotation:
                        annotation = output.group(2)
                    if "party" in relation and "politici" in annotation:
                        annotation = output.group(1)
                else:
                    print(output)
                # for some values we have manually annotations
                if annotations_map.get(annotation) is not None:
                    annotation = annotations_map[annotation]
                attributes.append((relation, annotation))
        except:
            continue
    return attributes


#%%
text = "Ratz_politicians"
print(get_attributes(text))
