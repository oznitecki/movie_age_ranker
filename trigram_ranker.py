import pickle
import unicodecsv as csv
from sets import Set
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
import string
from nltk.corpus import stopwords
stop = set(stopwords.words('english'))
exclude = set(string.punctuation) 
allowedTags = ['NN','NNS','VBG','JJ','VBD','VBN','VB','VBP','VBZ']
lemma = WordNetLemmatizer()

def load_obj(name):
    with open('output/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def clean(doc):
    pos = nltk.pos_tag(nltk.word_tokenize(doc))
    tagged = " ".join([j[0] for j in pos if j[1] in allowedTags])
    stop_free = " ".join([i for i in tagged.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

diffSets = load_obj('trigram_diffSets')
biSets = load_obj('bigram_diffSets')
uniSets = load_obj('diffSets')

f = open("input/test4.csv", "rb")
f2 = open("output/result4.csv", "wb")
csvreader = csv.reader(f)
fieldnames = ['id','title', 'plot', 'mpaa']
writer = csv.DictWriter(f2, fieldnames=fieldnames)
writer.writeheader()
firstrow = True
for row in csvreader:
    if firstrow:
        firstrow = False
        continue
    trigrams = Set(nltk.trigrams(clean(row[2]).split()))
    if len(trigrams & (diffSets['G'] | diffSets['PG-13'] | diffSets['R'] | diffSets['NC-17'])) > 0:
        mpaa = 'G'
        if len(diffSets['PG'] & trigrams) > 0:
            mpaa = 'PG'
        if len(diffSets['PG-13'] & trigrams) > 0:
            mpaa = 'PG-13'
        if len(diffSets['R'] & trigrams) > 0:
            mpaa = 'R'
        if len(diffSets['NC-17'] & trigrams) > 0:
            mpaa = 'NC-17'
    else:
        mpaa = 'R'
    """ bigrams = Set(nltk.bigrams(clean(row[2]).split()))
        if len(bigrams & (biSets['G'] | biSets['PG-13'] | biSets['R'] | biSets['NC-17'])) > 0:
            mpaa = 'G'
            if len(biSets['PG'] & bigrams) > 0:
                mpaa = 'PG'
            if len(biSets['PG-13'] & bigrams) > 0:
                mpaa = 'PG-13'
            if len(biSets['R'] & bigrams) > 0:
                mpaa = 'R'
            if len(biSets['NC-17'] & bigrams) > 0:
                mpaa = 'NC-17'
        else:
            mpaa = 'R'
            plotwords = Set(clean(row[2]).split())
            if len(plotwords - uniSets['G'] - uniSets['PG-13'] - uniSets['R'] - uniSets['NC-17']) <= 0.5*len(plotwords):
                minimalHits = len(plotwords)/30
                mpaa = 'G'
                if len(uniSets['PG'] & plotwords) > minimalHits:
                    mpaa = 'PG'
                if len(uniSets['PG-13'] & plotwords) > minimalHits:
                    mpaa = 'PG-13'
                if len(uniSets['R'] & plotwords) > minimalHits:
                    mpaa = 'R'
                if len(uniSets['NC-17'] & plotwords) > minimalHits:
                    mpaa = 'NC-17' """
    writer.writerow({'id':row[0],'title': row[1], 'plot': row[2], 'mpaa': mpaa})
f.close()
f2.close()