import unicodecsv as csv
from sets import Set
import pickle
from nltk.stem.wordnet import WordNetLemmatizer
import string
from nltk.corpus import stopwords
import nltk
from nltk.probability import FreqDist
stop = set(stopwords.words('english'))
exclude = set(string.punctuation) 
allowedTags = ['NN','NNS','VBG','JJ','VBD','VBN','VB','VBP','VBZ']
lemma = WordNetLemmatizer()

def save_obj(obj, name):
    with open('output/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def clean(doc):
    pos = nltk.pos_tag(nltk.word_tokenize(doc))
    tagged = " ".join([j[0] for j in pos if j[1] in allowedTags])
    stop_free = " ".join([i for i in tagged.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split() if word != 's')
    return normalized

def append(wordSets, inputFileName):
    f = open(inputFileName, "rb")
    csvreader = csv.reader(f)
    for row in csvreader:
        if wordSets.has_key(row[3]):
            wordSets[row[3]].append(row[2])
    f.close()
    print inputFileName + " - done appending"
    return

def train(wordSets, topicSets):
    for age in wordSets.keys():
        doc_clean = nltk.Text(''.join([clean(doc) for doc in wordSets[age]]).split())
        topicSets[age] = FreqDist(doc_clean)
        print age + " - done training"
    return

wordSets = dict({"G":[],"PG":[],"PG-13":[],"R":[],"NC-17":[]})
append(wordSets,"input/train.csv")
append(wordSets,"input/gold.csv")
append(wordSets,"input/gold2.csv")
append(wordSets,"input/trainG.csv")
append(wordSets,"input/trainPG.csv")
append(wordSets,"input/trainPG13.csv")
append(wordSets,"input/trainR.csv")
append(wordSets,"input/trainNC17.csv")

topicSets = dict({"G":[],"PG":[],"PG-13":[],"R":[],"NC-17":[]})
train(wordSets,topicSets)

diffSets = dict({"G":Set([]),"PG":Set([]),"PG-13":Set([]),"R":Set([]),"NC-17":Set([])})

for item in topicSets['G'].most_common(1000):#350 #>5
    topicSets['PG'].pop(item[0],None)
    topicSets['PG-13'].pop(item[0],None)
    topicSets['R'].pop(item[0],None)
    topicSets['NC-17'].pop(item[0],None)
    diffSets['G'].add(item[0])
for item in topicSets['PG'].most_common(500):#350 #>6
    topicSets['PG-13'].pop(item[0],None)
    topicSets['R'].pop(item[0],None)
    topicSets['NC-17'].pop(item[0],None)
    diffSets['PG'].add(item[0])
for item in topicSets['PG-13'].most_common(350):#350 #>2
    topicSets['R'].pop(item[0],None)
    topicSets['NC-17'].pop(item[0],None)
    diffSets['PG-13'].add(item[0]) 
for item in topicSets['R'].most_common(350):#350 #>5
    topicSets['NC-17'].pop(item[0],None)
    diffSets['R'].add(item[0])    
for item in topicSets['NC-17'].most_common(20):#20 #>1
    diffSets['NC-17'].add(item[0])    
save_obj(diffSets, 'diffSets')