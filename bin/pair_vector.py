import torch as th

relation_map = {
"relative" : "relative",
"type_of_kinship" : "relative",
"student_of" : "related",
"employer" : "employer",
"godparent" : "relative",
"partner_in_business_or_sport" : "colleague",
"replaces" : "related",
"replaced_by" : "related",
"killed_by" : "related",
"doctoral_advisor" : "related",
"doctoral_student" : "related",
"represented_by" : "related",
"different_from" : "no_relation",
"consecrator" : "no_relation",
"father" : "parent",
"mother" : "parent",
"spouse" : "spouse",
"sibling" : "sibling",
"stepparent" : "parent",
"child" : "child",
"unmarried_partner" : "partner",
"student" : "student",
"inspired_by" : "related"
}

attributes_map = {
"sex_or_gender" : "sex_or_gender",
"country_of_citizenship" : "country_of_citizenship",
"native_language" : "native_language",
"place_of_birth" : "place_of_birth",
"date_of_death" : "date_of_death",
"place_of_death" : "place_of_death",
"languages_spoken,_written_or_signed" : "languages_spoken,_written_or_signed",
"military_rank" : "military_rank",
"award_received" : "award_received",
"educated_at" : "educated_at",
"occupation" : "occupation",
"member_of_political_party" : "member_of_political_party",
"manner_of_death" : "manner_of_death",
"lifestyle" : "lifestyle",
"described_by_source" : "described_by_source",
"influenced_by" : "influenced_by",
"family" : "family",
"position_held" : "position_held",
"given_name" : "given_name",
"noble_title" : "noble_title",
"date_of_birth" : "date_of_birth",
"religion" : "religion",
"member_of" : "member_of",
"cause_of_death" : "cause_of_death",
"residence" : "residence",
"family_name" : "family_name",
"sport" : "sport",
"participant_in" : "participant_in",
"ethnic_group" : "ethnic_group",
"work_period_(start)" : "work_period_(start)",
"archives_at" : "archives_at",
"field_of_work" : "field_of_work",
"affiliation" : "affiliation",
"handedness" : "handedness",
"playing_hand" : "playing_hand",
"country_for_sport" : "country_for_sport",
"work_location" : "work_location",
"academic_degree" : "academic_degree",
"genre" : "genre",
"nominated_for" : "nominated_for",
"conflict" : "conflict",
"convicted_of" : "convicted_of",
"place_of_burial" : "place_of_burial",
"member_of_sports_team" : "member_of_sports_team",
"position_played_on_team_/_speciality" : "position_played_on_team_/_speciality",
"different_from" : "different_from",
"Eight_Banner_register" : "Eight_Banner_register",
"unmarried_partner" : "unmarried_partner",
"military_branch" : "military_branch",
"Roman_nomen_gentilicium" : "Roman_nomen_gentilicium",
"movement" : "movement",
"record_label" : "record_label",
"second_family_name_in_Spanish_name" : "second_family_name_in_Spanish_name",
"catalog" : "catalog",
"canonization_status" : "canonization_status",
"instrument" : "instrument",
"medical_condition" : "medical_condition",
"doctoral_advisor" : "doctoral_advisor",
"work_period_(end)" : "work_period_(end)",
"significant_event" : "significant_event",
"blood_type" : "blood_type",
"honorific_prefix" : "honorific_prefix",
"place_of_detention" : "place_of_detention",
"drafted_by" : "drafted_by",
"shooting_handedness" : "shooting_handedness",
"voice_type" : "voice_type",
"league" : "league",
"time_period" : "time_period",
"point_in_time" : "point_in_time",
"allegiance" : "allegiance",
"student_of" : "student_of",
"partner_in_business_or_sport" : "partner_in_business_or_sport",
"location_of_formation" : "location_of_formation",
"academic_major" : "academic_major",
"professorship" : "professorship",
"official_residence" : "official_residence",
"sports_discipline_competed_in" : "sports_discipline_competed_in",
"part_of" : "part_of",
"date_of_baptism_in_early_childhood" : "date_of_baptism_in_early_childhood",
"eye_color" : "eye_color",
"religious_order" : "religious_order",
"creator" : "creator",
"country_of_origin" : "country_of_origin",
"doctoral_student" : "doctoral_student",
"studies" : "studies",
"sexual_orientation" : "sexual_orientation",
"Roman_praenomen" : "Roman_praenomen",
"named_after" : "named_after",
"Fach" : "Fach",
"ancestral_home" : "ancestral_home",
"present_in_work" : "present_in_work",
"floruit" : "floruit",
"notable_work" : "notable_work",
"inception" : "inception",
"culture" : "culture",
"with" : "with",
"hair_color" : "hair_color",
"military_casualty_classification" : "military_casualty_classification",
"title_of_chess_person" : "title_of_chess_person",
"social_classification" : "social_classification",
"winner" : "winner",
"killed_by" : "killed_by",
"website_account_on" : "website_account_on",
"penalty" : "penalty",
"commander_of_(DEPRECATED)" : "commander_of_(DEPRECATED)",
"said_to_be_the_same_as" : "said_to_be_the_same_as",
"operator" : "operator",
"political_alignment" : "political_alignment",
"represented_by" : "represented_by",
"replaced_by" : "replaced_by",
"language_of_work_or_name" : "language_of_work_or_name",
"political_ideology" : "political_ideology",
"interested_in" : "interested_in",
"domain_of_saint_or_deity" : "domain_of_saint_or_deity"
}

i = 0
f = open('/Users/abhayms//Documents/ontology-learning-master/data/wikipeople/wikipeople_dataset.txt', 'r')
for line in f:
    line  = line.strip()
    parts = line.split("\t")
    i = i + 1
print(i)

default_person_attributes = {}
for k, v in attributes_map.items():
    default_person_attributes[k] = -1
#print(len(default_person_attributes))

entity_ids_by_type_map = {}
node_id_map = {}
# graph data is what we want to populate
# In the value th.tensor([0]) means first instance of Person and Award types respectively
#graph_data = {
#    # Abdullah of Saudi Arabia    award_received  Royal Victorian Chain
#    ('Person', 'award_received', 'Award') : (th.tensor([0]), th.tensor([0]))
#}
graph_data = {}
subject_map = {}
object_map = {}
f = open('/Users/abhayms//Documents/ontology-learning-master/data/wikipeople/wikipeople_dataset.txt', 'r')
for line in f:
    line  = line.strip()
    parts = line.split("\t")
    person = parts[0]
     
    if node_id_map.get(person) is None:
        node_id_map[person] = len(node_id_map.keys())
    subject_node_id = node_id_map.get(person)    
    # now either relation or attribute is going to be read from the input line
    relation = ""
    attribute = ""
    if parts[1] in list(relation_map.keys()):
        relation = parts[1]
        relation = relation_map[relation]
    elif parts[1] in list(attributes_map.keys()):
        attribute = parts[1]
    else:
        print(line, "has no attribute or relation_type")
        continue
 
   # if the person has not been seen before we assign a new id
    entity = parts[2]
    if relation != "":
        # because this is a relation, we ensure entity is also a node
        if node_id_map.get(entity) is None:
            node_id_map[entity] = len(node_id_map.keys())
        entity_node_id = node_id_map.get(entity)
        graph_entry_key = ("Person", relation, "Person")
        #print(person)
        #print(entity)
        #print(graph_entry_key)
        #print(graph_entry_value)
        #break
        # for every graph entry key, we want to generate tensor pairs like below
        # (tensor([0, 0, 0, 1]), tensor([1, 2, 3, 3]))
        # where the edges are (0,1), (0,2), (0,3) and (1,3)
        if subject_map.get(graph_entry_key) is None:
            subject_map[graph_entry_key] = []
        if object_map.get(graph_entry_key) is None:
            object_map[graph_entry_key] = []
        if graph_data.get(graph_entry_key) is None:
            graph_data[graph_entry_key] = None
        subject_list = subject_map.get(graph_entry_key)
        subject_list.append(subject_node_id)
        object_list = object_map.get(graph_entry_key)
        object_list.append(entity_node_id)
        subject_map[graph_entry_key] = subject_list
        object_map[graph_entry_key] = object_list
    # for each attribute, we want to create ids of entities like below
    # {'sex_or_gender': {'Male gender': 0, 'Female gender': 1}
    if attribute != "":
        if entity_ids_by_type_map.get(attribute) is None:
            entity_ids_by_type_map[attribute] = {}
        attribute_map = entity_ids_by_type_map.get(attribute)
        if attribute_map.get(entity) is None:
            attribute_map[entity] = len(attribute_map.keys())
        entity_ids_by_type_map[attribute] = attribute_map
        
for graph_entry_key in graph_data.keys():
    #print(subject_map[graph_entry_key])
    #print(graph_entry_key, ":", (th.tensor(subject_map[graph_entry_key]), th.tensor(object_map[graph_entry_key])))
    graph_data[graph_entry_key] = (th.tensor(subject_map[graph_entry_key]), th.tensor(object_map[graph_entry_key]))
#print(graph_data[('Person', 'parent', 'Person')])

#print(len(node_id_map))
#print(len(graph_data))
#print(len(subject_map))

my_set = set()
for k, v in subject_map.items():
    print(k, v, len(set(v)))
    for node_id in v:
        my_set.add(node_id)