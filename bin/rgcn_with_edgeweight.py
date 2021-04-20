import torch as th
import dgl
import networkx as nx
import numpy as np
from sklearn.metrics import roc_auc_score 
from sklearn.metrics import precision_recall_fscore_support 
import matplotlib.pyplot as plt
import calculate_edge_weights as cew

edge_weights = cew.edge()
#print(edge_weights)

def func():
    lines = []
    f = open("/Users/abhayms//Documents/ontology-learning-master/data/wikipeople/wikipeople_dataset.txt", "r")
    for x in f:
        lines.append(x)

    j=0
    for i, line in enumerate(lines):
        line  = line.strip()
        parts = line.split("\t")
        j=j+1

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

    default_person_attributes = {}
    for k, v in attributes_map.items():
        default_person_attributes[k] = -1

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
            continue        
        entity = parts[2]
        if attribute != "":
            person_attributes = person_attributes_map[person]
            if person_attributes.get(attribute) is None:
                print("person_attributes cannot be none for:", attribute)
                person_attributes[attribute] = -1
            entity_id_map = entity_ids_by_type_map.get(attribute)
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


    graph_entry_key = ("Person",'selfloop', "Person")
    if graph_data.get(graph_entry_key) is None:
        graph_data[graph_entry_key] = None

    subject_map[graph_entry_key] = singleton_nodes_list
    object_map[graph_entry_key] = singleton_nodes_list

    for graph_entry_key in graph_data.keys():
        graph_data[graph_entry_key] = (th.tensor(subject_map[graph_entry_key]), th.tensor(object_map[graph_entry_key]))

    my_set=set()
    for k,v in node_id_map.items():
        my_set.add(v)

    my_set = set()
    for k, v in subject_map.items():
        #print(k, len(v), len(set(v)))
        for node_id in v:
            my_set.add(node_id)

    for k, v in object_map.items():
        for node_id in v:
            my_set.add(node_id)


    hetero_graph = dgl.heterograph(graph_data)

    ndata_list=[]
    for attribute in list(attributes_map.keys()):
        attribute_keys = []
        attribute_values = []
        for k, v in person_attributes_map.items():
            attribute_values.append(v.get(attribute))
            attribute_keys.append(k)
        ndata_list.append(attribute_values)
        x=np.transpose(ndata_list)
        
    hetero_graph.ndata['Person']=th.tensor(x)

    """ import json

    with open('/Users/abhayms//Documents/ontology-learning-master/bin/names.json','r') as h:
        names = json.load(h)

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
            

        if node_id_map.get(line['entity1']) is None:
            for name in names:
                for k,v in name.items():
                    if line['entity1'] == v:
                        qid = k
                        if qid is not None:
                            line['entity1'] = node_id_map.get(qid)
                            break
                    break
        else:      
            line['entity1'] = node_id_map.get(line['entity1'])

        cid = None
        if node_id_map.get(line['entity2']) is None:
            for name in names:
                for k,v in name.items():
                    if line['entity2'] == v:
                        cid = k
                        if cid is not None:
                            line['entity2'] = node_id_map.get(cid)
                            break
                    break
        else:   
            line['entity2'] = node_id_map.get(line['entity2']) 

        dsm.append(line)

    etypes_list = ['child',
                    'colleague',
                    'employer',
                    'no_relation',
                    'nothing',
                    'parent',
                    'partner',
                    'related',
                    'relative',
                    'selfloop',
                    'sibling',
                    'spouse',
                    'student']
    edge_weights = {'child': [],
                    'colleague': [],
                    'employer': [],
                    'no_relation': [],
                    'nothing': [],
                    'parent': [],
                    'partner': [],
                    'related': [],
                    'relative': [],
                    'selfloop': [],
                    'sibling': [],
                    'spouse': [],
                    'student': []}
    for k in etypes_list:
        for i in range(0,hetero_graph.number_of_edges(k)):
            for j in dsm:
                if (j['entity1'] == graph_data[('Person', k, 'Person')][0][i].item()) and (j['entity2'] == graph_data[('Person', k, 'Person')][1][i].item()):
                    edge_weights[k].append(j['score'])
                    break
            if (len(edge_weights[k]) < hetero_graph.number_of_edges(k)):
                for z in range(len(edge_weights[k]),hetero_graph.number_of_edges(k)):
                    edge_weights[k].append(0)
        
    
    print(edge_weights) """
    import torch

    #x = torch.tensor(etypes_tensor)

    import dgl.nn as dglnn
    import torch.nn as nn
    import torch.nn.functional as F
    import dgl.function as fn

    class RGCN(nn.Module):
        def __init__(self, in_feats, hid_feats, out_feats, rel_names):
            super().__init__()

            self.conv1 = dglnn.HeteroGraphConv({
                rel: dglnn.GraphConv(in_feats, hid_feats)
                for rel in rel_names}, aggregate='sum')

            self.conv2 = dglnn.HeteroGraphConv({
                rel: dglnn.GraphConv(hid_feats, out_feats)
                for rel in rel_names}, aggregate='sum')

        def forward(self, graph, inputs):
            # inputs are features of nodes
            h = self.conv1(graph, inputs ,edge_weights)
            h = {k: F.relu(v) for k, v in h.items()}
            h = self.conv2(graph, h,edge_weights)
            return h

    class HeteroDotProductPredictor(nn.Module):
        def forward(self, graph, h, etype):
            # h contains the node representations for each node type computed from
            # the GNN defined in the previous section (Section 5.1).
            with graph.local_scope():
                #print(h)
                h = h['Person']
                #print(h)
                graph.ndata['h'] = h
                graph.apply_edges(fn.u_dot_v('h', 'h', 'score'), etype=etype)
                return graph.edges[etype].data['score']

    def construct_negative_graph(graph, k, etype):
        utype, _, vtype = etype
        src, dst = graph.edges(etype=etype)
        #print(src, dst)
        neg_src = src.repeat_interleave(k)
        neg_dst = torch.randint(0, graph.number_of_nodes(vtype), (len(src) * k,))
        return dgl.heterograph(
            {etype: (neg_src, neg_dst)},
            num_nodes_dict={ntype: graph.number_of_nodes(ntype) for ntype in graph.ntypes})

    class Model(nn.Module):
        def __init__(self, in_features, hidden_features, out_features, rel_names):
            super().__init__()
            self.sage = RGCN(in_features, hidden_features, out_features, rel_names)
            self.pred = HeteroDotProductPredictor()
        def forward(self, g, neg_g, x, etype):
            h = self.sage(g, x)
            return self.pred(g, h, etype), self.pred(neg_g, h, etype)
    def compute_loss(pos_score, neg_score):
        # Cross entropy loss
        scores = torch.cat([pos_score, neg_score])
        labels = torch.cat([torch.ones(pos_score.shape[0]), torch.zeros(neg_score.shape[0])])
        return F.binary_cross_entropy_with_logits(scores, labels)

    def compute_loss_margin(pos_score, neg_score):
        # Margin loss
        n_edges = pos_score.shape[0]
        return (1 - neg_score.view(n_edges, -1) + pos_score.unsqueeze(1)).clamp(min=0).mean()

    def compute_auc(pos_score, neg_score):
        scores = torch.cat([pos_score, neg_score]).detach().numpy()
        labels = torch.cat(
            [torch.ones(pos_score.shape[0]), torch.zeros(neg_score.shape[0])]).numpy()
        return roc_auc_score(labels, scores)

    k = 1
    model = Model(114, 20, 5, hetero_graph.etypes)
    #node_features = hetero_graph.nodes['Person'].data
    node_features={'Person':hetero_graph.nodes['Person'].data['Person']}
    #print(hetero_graph.edges(etype='partner'))
    #print(hetero_graph.nodes['Person'].data['Person'])
    #print(type(node_features))
    #print(node_features)
    #print(hetero_graph.ndata['Person'])
    opt = torch.optim.Adam(model.parameters())
    for epoch in range(500):
        negative_graph = construct_negative_graph(hetero_graph, k, ('Person', 'student', 'Person'))
        #print(negative_graph)
        pos_score, neg_score = model(hetero_graph, negative_graph, node_features, ('Person', 'student', 'Person'))
        #print(pos_score, neg_score)
        margin_loss = compute_loss_margin(pos_score, neg_score)
        pos_score = pos_score.squeeze(1)
        neg_score = neg_score.squeeze(1)
        loss = compute_loss(pos_score, neg_score)
        opt.zero_grad()
        loss.backward()
        opt.step()


        #print("Cross Entropy: ",loss.item(), "   Margin Loss: ",margin_loss.item())    

    auc = compute_auc(pos_score, neg_score)
    print(auc)
    return auc

sum = 0
for i in range(10):
    sum = sum + func()

avg = sum/10
print(avg)