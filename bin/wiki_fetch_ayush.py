#title,introduction,infobox,sectionwise,text
import pandas as pd
df = pd.read_csv('/Users/abhayms//Documents/ontology-learning-master/data/wikipeople/n-ary_train_qids.txt.0', delimiter = "\t", names=["Entity1"])
en = df['Entity1']
df1 = pd.read_csv('/Users/abhayms//Documents/ontology-learning-master/data/wikipeople/wikipeople_dataset.txt', delimiter = "\t")

entity1 = set(df1['Q1000727'])
f = open("/Users/abhayms//Documents/ontology-learning-master/data/wikipeople/n-ary_train_qid_details.json.0", "r")
print(f)

lines = f.readlines()
for entity in entity1:
        mg = {'name':entity,'title':0,'introduction':0,'text':0,'infobox':0}
        for line in lines:
            try:
                dic = eval(line)
            except:
                pass
            for z in en:
                try:
                    #print(dic['Q1001']['title'])              #title
                    mg['title'] = mg['title'] + dic[str(z)]['title'].count(entity)
                    #print(dic['Q1001']['first_section'])      #introduction
                    mg['introduction'] = mg['introduction'] + dic[str(z)]['first_section'].count(entity)
                    #print(dic['Q1001']['infobox'])            #infobox
                    info = str(dic[str(z)]['infobox'])
                    mg['infobox'] = mg['infobox'] + info.count(entity)
                    text = dic[str(z)]['text']               
                    res_list = (text.rstrip().split('\n\n')) 
                    for i in res_list:
                        k = (i.rstrip().split('\n'))
                        if(len(k[0]) < 70):
                            mg[k[0]] = i.count(entity)
                            if (mg[k[0]] == 0):
                                del mg[k[0]]
                        mg['text'] = mg['text'] + i.count(entity)
                except:
                    #print("KEY ERROR")
                    pass
        with open('result.txt', 'a+') as filehandle:
            filehandle.write('%s\n' % mg)

#print(mg)

