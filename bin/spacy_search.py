filename = "/Users/abhayms//Documents/ontology-learning-master/data/wikipeople/n-ary_train_qid_details.json.0"
f = open(filename, "r")
lines = f.readlines()
print(len(lines))


#for line in lines:
#    entities = get_entities_from_spacy(line)
#    for entity_element in entities:
#        location = entity_element.get("location")
#        entity = entity_element.get("label")
#        entity_location_map[entity][location] += 1