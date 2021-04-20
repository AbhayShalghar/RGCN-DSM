import torch as th
import dgl
import networkx as nx
import numpy as np
from sklearn.metrics import roc_auc_score 
from sklearn.metrics import precision_recall_fscore_support 
import matplotlib.pyplot as plt

def func(re):
    #print(dgl.__version__)
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
    #print(type(ndata_list))
    #print(hetero_graph.ndata)

    #for k,v in hetero_graph.ndata.items():
        #print(v)

    #print(type(hetero_graph.nodes['Person'].data['Person']))
    #print(hetero_graph.number_of_edges())

    import json

    dsm = []
    f = open("vectors_exact_partial.json", "r")
    for line in f.readlines():
        line = eval(line)
        vector = []
        vector.append(line['title'])
        vector.append(line['infobox'])
        vector.append(line['first_section'])
        vector.append(line['section'])
        vector.append(line['text_sentence'])

        del line['title']
        del line['infobox']
        del line['first_section']
        del line['section']
        del line['text_sentence']

        line['tensor'] = vector
        line['entity1'] = node_id_map.get(line['entity1'])
        line['entity2'] = node_id_map.get(line['entity2'])

        dsm.append(line)

    print(len(dsm))
    import torch
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
            h = self.conv1(graph, inputs)
            h = {k: F.relu(v) for k, v in h.items()}
            h = self.conv2(graph, h)
            return h

    class HeteroDotProductPredictor(nn.Module):
        def forward(self, graph, h, etype):
            # h contains the node representations for each node type computed from
            # the GNN defined in the previous section (Section 5.1).
            with graph.local_scope():
                #print(h)
                h = h['Person'] #h(i)
                h_iota = h.clone()
                #print(h_iota)
                #for loop for 31000 entities
                for doc in dsm:
                    #add_up = []
                    index_1 = doc['entity1']
                    index_2 = doc['entity2']
                    #add_up.append(sum(doc['tensor']))
                    add_up = [sum(doc['tensor'])]
                    try:
                        ds = th.matmul(h[index_1], (torch.FloatTensor(up)))
                        h_iota[index_1] = h[index_1] + torch.sigmoid(ds)
                        ds_1 = th.matmul(h[index_2], (torch.FloatTensor(up)))
                        h_iota[index_2] = h[index_2] + torch.sigmoid(ds_1)
                    except:
                        pass
                
                graph.ndata['h'] = h_iota
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
        def __init__(self, in_features, hidden_features, out_features, rel_names):
            super().__init__()
            self.sage = RGCN(in_features, hidden_features, out_features, rel_names)
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

    k = 1
    model = Model(43, 20, 1, hetero_graph.etypes)
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
        #print('a')
        negative_graph = construct_negative_graph(hetero_graph, k, ('Person', re, 'Person'))
        #print((negative_graph))
        #nx.draw(negative_graph.to_networkx())
        #plt.show()
        #plt.plot(scalex=1000, scaley=1000, data=hetero_graph)
        #plt.show()
        pos_score, neg_score = model(hetero_graph, negative_graph, node_features, ('Person', re, 'Person'))
        #print(pos_score, neg_score)
        margin_loss = compute_loss_margin(pos_score, neg_score)
        pos_score = pos_score.squeeze(1)
        neg_score = neg_score.squeeze(1)
        loss = compute_loss(pos_score, neg_score)
        opt.zero_grad()
        loss.backward()
        opt.step()
        print("Cross Entropy: ",loss.item(), "   Margin Loss: ",margin_loss.item())    

    auc = compute_auc(pos_score, neg_score)
    print(auc)
    return auc

etypes_list = ['child', 'childrens', 'colleague', 'employee_of', 'employees', 'founded_by', 'friend', 'member_of', 'members', 'no_relation', 'nothing', 'other_family', 'parent', 'parents', 'partner', 'relation', 'relations', 'rival', 'shareholders', 'siblings', 'spouse', 'subsidiaries']
for re in etypes_list:
    Sum = 0
    for i in range(5):
        Sum = Sum + func(re)

    avg = Sum/5
    print("Average = " + re + " " + str(avg))