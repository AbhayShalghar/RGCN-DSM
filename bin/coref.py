import spacy
import neuralcoref

nlp = spacy.load('en_core_web_sm')  # load the model
neuralcoref.add_to_pipe(nlp)

text = "Ayush is a bad boy.He is an asshole"
doc = nlp(text)  # get the spaCy Doc (composed of Tokens)

print(doc._.coref_clusters)
# Eva and Martha: [Eva and Martha, their, they]
# Jenny: [Jenny, her]

print(doc._.coref_resolved)
# Eva and Martha didn't want Eva and Martha friend Jenny \
# to feel lonely so Eva and Martha invited Jenny to the party.