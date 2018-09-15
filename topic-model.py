import unicodecsv as csv
from sets import Set
import pickle
from nltk.stem.wordnet import WordNetLemmatizer
import string
from nltk.corpus import stopwords
import nltk
stop = set(stopwords.words('english'))
exclude = set(string.punctuation) 
allowedTags = ['NN','NNS','VBG','JJ','VBD','VBN','VB','VBP','VBZ']
lemma = WordNetLemmatizer()
import gensim
from gensim import corpora

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
        TOPIC_NUM = 2 if age != 'G' else 3
        WORD_NUM = 200 if age != 'NC-17' else 50
        doc_clean = [clean(doc).split() for doc in wordSets[age]]
        dictionary = corpora.Dictionary(doc_clean)
        doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
        Lda = gensim.models.ldamodel.LdaModel
        ldamodel = Lda(doc_term_matrix, num_topics=TOPIC_NUM, id2word = dictionary)
        topics = [item[0] for topic in ldamodel.show_topics(num_words=WORD_NUM,formatted=False) for item in topic[1]]
        topicSets[age].update(topics)
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

topicSets = dict({"G":Set([]),"PG":Set([]),"PG-13":Set([]),"R":Set([]),"NC-17":Set([])})
train(wordSets,topicSets)

diffSets = dict({"PG":(topicSets['PG']-topicSets['G']),
                 "PG-13":(topicSets['PG-13']-topicSets['PG']-topicSets['G']),
                 "R":(topicSets['R']-topicSets['PG-13']-topicSets['PG']-topicSets['G']),
                 "NC-17":(topicSets['NC-17']-topicSets['R']-topicSets['PG-13']-topicSets['PG']-topicSets['G'])})
    
save_obj(diffSets, 'diffSets')