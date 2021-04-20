import json
from datetime import datetime
import requests
from requests import utils

with open('/Users/abhayms//Documents/ontology-learning-master/bin/names.json','r') as h:
    names = json.load(h)

with open('/Users/abhayms//Documents/ontology-learning-master/bin/relations.json','r') as f:
    lines = json.load(f)

