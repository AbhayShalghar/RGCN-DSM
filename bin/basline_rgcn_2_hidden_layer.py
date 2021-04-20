import torch as th
import dgl
import networkx as nx
import numpy as np
from sklearn.metrics import roc_auc_score 
from sklearn.metrics import precision_recall_fscore_support 
import matplotlib.pyplot as plt

print(dgl.__version__)
lines = []
f = open("wikipeople_dataset.txt", "r")
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
#print(len(relation_map))

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

#print(singleton_nodes_list)

graph_entry_key = ("Person",'selfloop', "Person")
if graph_data.get(graph_entry_key) is None:
    graph_data[graph_entry_key] = None

subject_map[graph_entry_key] = singleton_nodes_list
object_map[graph_entry_key] = singleton_nodes_list

for graph_entry_key in graph_data.keys():
    graph_data[graph_entry_key] = (th.tensor(subject_map[graph_entry_key]), th.tensor(object_map[graph_entry_key]))
#print(graph_data[("Person",'selfloop', "Person")])

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

hetero_graph = dgl.heterograph(graph_data)

#print(hetero_graph.ntypes)
#print(hetero_graph.num_dst_nodes())
#print(hetero_graph.dstnodes())
#print(hetero_graph.etypes)
#print(hetero_graph.number_of_nodes())
#print(hetero_graph.number_of_edges())
#print(hetero_graph)

#for k, v in graph_data.items():
 #   print(len(v[0]))

#for person, id in person_attributes_map.items():
    #if node_id_map.get(person) is None:
      #  print(person)

#print(len(node_id_map))

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
#print(type(ndata_list))
#print(hetero_graph.ndata)

#for k,v in hetero_graph.ndata.items():
    #print(v)

#print(type(hetero_graph.nodes['Person'].data['Person']))

import torch
import dgl.nn as dglnn
import torch.nn as nn
import torch.nn.functional as F
import dgl.function as fn

class RGCN(nn.Module):
    def __init__(self, in_feats, hid_feats1, hid_feats2, out_feats, rel_names):
        super().__init__()

        self.conv1 = dglnn.HeteroGraphConv({
            rel: dglnn.GraphConv(in_feats, hid_feats1)
            for rel in rel_names}, aggregate='sum')
        self.conv2 = dglnn.HeteroGraphConv({
            rel: dglnn.GraphConv(hid_feats1, hid_feats2)
            for rel in rel_names}, aggregate='sum')
        self.conv3 = dglnn.HeteroGraphConv({
            rel: dglnn.GraphConv(hid_feats2, out_feats)
            for rel in rel_names}, aggregate='sum')

    def forward(self, graph, inputs):
        # inputs are features of nodes
        h = self.conv1(graph, inputs)
        h = {k: F.relu(v) for k, v in h.items()}
        h = self.conv2(graph, h)
        h = {k: F.relu(v) for k, v in h.items()}
        h = self.conv3(graph, h)
        return h

class HeteroDotProductPredictor(nn.Module):
    def forward(self, graph, h, etype):
        # h contains the node representations for each node type computed from
        # the GNN defined in the previous section (Section 5.1).
        with graph.local_scope():
            #print(h)
            h = h['Person'] #h(i)
            #for loop for 31000 entities
            #node id of both entities
            #th.matmul(h[index(node id)], vector)
            #some function theta
            #add with h
            graph.ndata['h'] = h
            graph.apply_edges(fn.u_dot_v('h', 'h', 'score'), etype=etype)
            return graph.edges[etype].data['score']

def construct_negative_graph(graph, k, etype):
    utype, _, vtype = etype
    src, dst = graph.edges(etype=etype)
    #print(src, dst)
    #change this
    neg_src = src.repeat_interleave(k)
    neg_dst = torch.randint(0, graph.number_of_nodes(vtype), (len(src) * k,))
    #print(neg_src, neg_dst)
    return dgl.heterograph(
        {etype: (neg_src, neg_dst)},
        num_nodes_dict={ntype: graph.number_of_nodes(ntype) for ntype in graph.ntypes})

class Model(nn.Module):
    def __init__(self, in_features, hidden_features1, hidden_features2, out_features, rel_names):
        super().__init__()
        self.sage = RGCN(in_features, hidden_features1, hidden_features2, out_features, rel_names)
        self.pred = HeteroDotProductPredictor()
    def forward(self, g, neg_g, x, etype):
        h = self.sage(g, x)
        return self.pred(g, h, etype), self.pred(neg_g, h, etype)
def compute_loss(pos_score, neg_score):
    # Cross entropy loss
    #print(pos_score)
    #print(neg_score)
    scores = torch.cat([pos_score, neg_score])
    labels = torch.cat([torch.ones(pos_score.shape[0]), torch.zeros(neg_score.shape[0])])
    #print(scores)
    #print(labels)
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

""" def compute_p_r_f(pos_score, neg_score):
    scores = torch.cat([pos_score, neg_score]).detach().numpy()
    labels = torch.cat(
        [torch.ones(pos_score.shape[0]), torch.zeros(neg_score.shape[0])]).numpy()
    return precision_recall_fscore_support(labels, scores) """

k = 1
model = Model(114, 20, 5, 1, hetero_graph.etypes)
#node_features = hetero_graph.nodes['Person'].data
node_features={'Person':hetero_graph.nodes['Person'].data['Person']}
#print(type(hetero_graph.nodes['Person'].data['Person']))
#print(hetero_graph.nodes['Person'].data['Person'])
#print(type(node_features))
#print(node_features)
#print(hetero_graph.nodes['Person'].data['Person'])
#nx.draw(hetero_graph.to_networkx())
#plt.show()
opt = torch.optim.Adam(model.parameters())
for epoch in range(200):
    negative_graph = construct_negative_graph(hetero_graph, k, ('Person', 'parent', 'Person'))
    #print((negative_graph))
    #nx.draw(negative_graph.to_networkx())
    #plt.show()
    #plt.plot(scalex=1000, scaley=1000, data=hetero_graph)
    #plt.show()
    pos_score, neg_score = model(hetero_graph, negative_graph, node_features, ('Person', 'parent', 'Person'))
    #print(pos_score, neg_score)
    margin_loss = compute_loss_margin(pos_score, neg_score)
    pos_score = pos_score.squeeze(1)
    neg_score = neg_score.squeeze(1)
    loss = compute_loss(pos_score, neg_score)
    opt.zero_grad()
    loss.backward()
    opt.step()
    print("Cross Entropy: ",loss.item(), "   Margin Loss: ",margin_loss.item())    

print(compute_auc(pos_score, neg_score))
#print(compute_p_r_f(pos_score, neg_score))