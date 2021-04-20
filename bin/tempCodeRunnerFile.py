import pandas as pd
df = pd.read_csv('/Users/abhayms//Documents/ontology-learning-master/data/wikipeople/wikipeople_dataset.txt', delimiter = "\t", names=["Entity1"])
print(df['Entity1'])