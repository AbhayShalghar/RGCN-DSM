import torch as th
import dgl
import networkx as nx
import numpy as np
from sklearn.metrics import roc_auc_score 
from sklearn.metrics import precision_recall_fscore_support 
import matplotlib.pyplot as plt

def edge():
    lines = []
    f = open("tacred_dataset.txt", "r")
    for x in f:
        lines.append(x)

    #print(len(set(lines)))

    j=0
    for i, line in enumerate(lines):
        line  = line.strip()
        parts = line.split("\t")
        j=j+1
    #print(j)

    relation_map = {
	"child" : "child",
	"children" : "childrens",
	"colleague" : "colleague",
	"employee_of" : "employee_of",
	"founded_by" : "founded_by",
	"friend" : "friend",
	"member_of" : "member_of",
	"members" : "members",
	"no_relation" : "no_relation",
	"other_family" : "other_family",
	"parent" : "parent",
	"parents" : "parents",
	"partner" : "partner",
	"relation" : "relation",
	"relations" : "relations",
	"rival" : "rival",
	"shareholders" : "shareholders",
	"siblings" : "siblings",
	"spouse" : "spouse",
	"subsidiaries" : "subsidiaries",
	"top_members/employees" : "employees"
    }

    attributes_map = {
	"alternate_names" : "alternate_names",
	"cities_of_residence" : "city",
	"city" : "city",
	"city_of_birth" : "city",
	"city_of_death" : "city",
	"city_of_headquarters" : "city",
	"continent" : "continent",
	"countries_of_residence" : "country",
	"country" : "country",
	"country_of_birth" : "country",
	"country_of_headquarters" : "country",
	"county" : "county",
	"date_of_birth" : "date_of_birth",
	"date_of_death" : "date_of_death",
	"dissolved" : "dissolved",
	"email_address" : "email_address",
	"employee_of" : "employee_of",
	"first_name" : "first_name",
	"founded" : "founded",
	"gender" : "gender",
	"ideology" : "ideology",
	"last_name" : "last_name",
	"location" : "location",
	"middle_names" : "middle_names",
	"name" : "name",
	"name_suffix" : "name_suffix",
	"nationality" : "nationality",
	"org" : "org",
	"origin" : "origin",
	"per" : "per",
	#"political/religious_affiliation" : "affiliation",
	"province" : "province",
	"religion" : "religion",
	"salutation" : "salutation",
	"schools_attended" : "schools_attended",
	"state" : "state",
	"stateorprovince_of_birth" : "state",
	"stateorprovince_of_death" : "state",
	"stateorprovince_of_headquarters" : "state",
	"stateorprovinces_of_residence" : "state",
	"subsidiaries" : "subsidiaries",
	"top_members/employees" : "employees",
	"website" : "website",
	"zipcode" : "zipcode"
    }
    #print(len(attributes_map))

    default_person_attributes = {}
    for k, v in attributes_map.items():
        default_person_attributes[k] = -1
    #print(len(default_person_attributes))

    entity_ids_by_type_map = {}
    node_id_map = {}
    graph_data = {}
    subject_map = {}
    object_map = {}
    for i, line in enumerate(lines):
        line  = line.strip()
        parts = line.split("\t")

        person = parts[0]
        
        if node_id_map.get(person) is None:
            node_id_map[person] = len(node_id_map.keys())
        subject_node_id = node_id_map.get(person)    
        relation = ""
        attribute = ""
        if parts[1] in list(relation_map.keys()):
            relation = parts[1]
            relation = relation_map[relation]
        elif parts[1] in list(attributes_map.keys()):
            attribute = parts[1]
        else:
            #print(line, "has no attribute or relation_type")
            relation = "nothing"
    
        entity = parts[2]
        
        if relation != "":
            if node_id_map.get(entity) is None:
                node_id_map[entity] = len(node_id_map.keys())
            entity_node_id = node_id_map.get(entity)
            graph_entry_key = ("Person", relation, "Person")
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
        if attribute != "":
            if entity_ids_by_type_map.get(attribute) is None:
                entity_ids_by_type_map[attribute] = {}
            attribute_map = entity_ids_by_type_map.get(attribute)
            if attribute_map.get(entity) is None:
                attribute_map[entity] = len(attribute_map.keys())
            entity_ids_by_type_map[attribute] = attribute_map
            
    person_attributes_map = {}
    #print(attribute_map)
    #print(object_map)

    for person, node_id in node_id_map.items():
        person_attributes_map[person] = default_person_attributes.copy()

    for i, line in enumerate(lines):
        line  = line.strip()
        parts = line.split("\t")
        person = parts[0]
        subject_node_id = node_id_map.get(person) 
        relation = ""
        attribute = ""
        if parts[1] in list(relation_map.keys()):
            continue
        elif parts[1] in list(attributes_map.keys()):
            attribute = parts[1]
            attribute = attributes_map.get(attribute)
        else:
            #print(line, "has no attribute or relation_type")
            continue        
        entity = parts[2]
        if attribute != "":
            person_attributes = person_attributes_map[person]
            if person_attributes.get(attribute) is None:
                #print("person_attributes cannot be none for:", attribute)
                person_attributes[attribute] = -1
            entity_id_map = entity_ids_by_type_map.get(attribute)
            #print(entity_id_map)
            entity_id = entity_id_map.get(entity)
            person_attributes[attribute] = entity_id
            person_attributes_map[person] = person_attributes

    for graph_entry_key in graph_data.keys():
        graph_data[graph_entry_key] = (th.tensor(subject_map[graph_entry_key]), th.tensor(object_map[graph_entry_key]))

    hetero_graph = dgl.heterograph(graph_data)

    singleton_nodes_list=[]

    for k, v in person_attributes_map.items():
        if node_id_map.get(k) is None:
            continue
        node_id = node_id_map.get(k)
        if not hetero_graph.has_nodes(node_id):
            singleton_nodes_list.append(node_id)

    #print(singleton_nodes_list)

    """ graph_entry_key = ("Person",'selfloop', "Person")
    if graph_data.get(graph_entry_key) is None:
        graph_data[graph_entry_key] = None

    subject_map[graph_entry_key] = singleton_nodes_list
    object_map[graph_entry_key] = singleton_nodes_list

    for graph_entry_key in graph_data.keys():
        graph_data[graph_entry_key] = (th.tensor(subject_map[graph_entry_key]), th.tensor(object_map[graph_entry_key]))
    #print(graph_data[("Person",'selfloop', "Person")]) """

    #print(len(node_id_map))
    my_set=set()
    for k,v in node_id_map.items():
        my_set.add(v)
    #print(len(my_set))

    #print(len(graph_data))
    #print(subject_map[('Person', 'colleague', 'Person')])
    #print(object_map[('Person', 'colleague', 'Person')])

    my_set = set()
    for k, v in subject_map.items():
        #print(k, len(v), len(set(v)))
        for node_id in v:
            my_set.add(node_id)

    for k, v in object_map.items():
        #print(k, len(v), len(set(v)))
        for node_id in v:
            my_set.add(node_id)

    #print(len(my_set))
    #print(type(graph_data))
    hetero_graph = dgl.heterograph(graph_data)

    #print(hetero_graph.ntypes)
    #print(hetero_graph.num_dst_nodes())
    #print(hetero_graph.dstnodes())
    #print(hetero_graph.etypes)
    #print(hetero_graph.number_of_nodes())
    #print(hetero_graph.number_of_edges())
    #print(attributes_map)
    #print(hetero_graph)

    #for k, v in graph_data.items():
    #   print(len(v[0]))

    #for person, id in person_attributes_map.items():
        #if node_id_map.get(person) is None:
        #  print(person)

    #print(len(node_id_map))
    #print(attribute_map.keys())
    #print(person_attributes_map)
    ndata_list=[]
    for attribute in list(attributes_map.keys()):
        attribute_keys = []
        attribute_values = []
        for k, v in person_attributes_map.items():
            attribute_values.append(v.get(attribute))
            attribute_keys.append(k)
        #print(ndata_list)
        ndata_list.append(attribute_values)
        x=np.transpose(ndata_list)
    
    #print(ndata_list)
    x = np.vstack(x[:, :]).astype(float)
    hetero_graph.ndata['Person']=th.tensor(x)
    #print(hetero_graph.ndata)

    x = x.astype(np.int64)  
    #print(x)
    #print(x.dtype)
    hetero_graph.ndata['Person']=th.from_numpy(x)

    import json

    dsm = []
    f = open("vectors_exact_partial.json", "r")
    for line in f.readlines():
        line = eval(line)
        dsm_score = 0
        if line['title'] > 0:
            dsm_score = dsm_score + 0.1
        if line['infobox'] > 0:
            dsm_score = dsm_score + 0.4
        if line['first_section'] > 0:
            dsm_score = dsm_score + 0.2
        if line['section'] > 0:
            dsm_score = dsm_score + 0.2
        if line['text_sentence'] > 0:
            dsm_score = dsm_score + 0.1

        del line['title']
        del line['infobox']
        del line['first_section']
        del line['section']
        del line['text_sentence']

        line['score'] = round(dsm_score,1)
        line['entity1'] = node_id_map.get(line['entity1'])
        line['entity2'] = node_id_map.get(line['entity2'])

        dsm.append(line)

    #print(dsm[0:5])

    etypes_list = ['child', 'childrens', 'colleague', 'employee_of', 'employees', 'founded_by', 'friend', 'member_of', 'members', 'no_relation', 'nothing', 'other_family', 'parent', 'parents', 'partner', 'relation', 'relations', 'rival', 'shareholders', 'siblings', 'spouse', 'subsidiaries']
    edge_weights = {}
    for i in etypes_list:
        edge_weights[i] = []
    for k in etypes_list:
        print(k)
        for i in range(0,hetero_graph.number_of_edges(k)):
            #print(hetero_graph.number_of_edges(k))
            for j in dsm:
                if (j['entity1'] == graph_data[('Person', k, 'Person')][0][i].item()) and (j['entity2'] == graph_data[('Person', k, 'Person')][1][i].item()):
                    edge_weights[k].append(j['score'])
                    break
        if (len(edge_weights[k]) < hetero_graph.number_of_edges(k)):
            edge_weights[k].extend([0.0] * (hetero_graph.number_of_edges(k) - len(edge_weights[k])))
        edge_weights[k] = th.tensor(edge_weights[k])
        #print(len(edge_weights[k]))
        #print(edge_weights)
    
    main_dict = {}
    main_dict['edge_weight'] = []
    for k,v in edge_weights.items():
        main_dict['edge_weight'].append(v)
        #print(len(v))
        
    return(main_dict)
