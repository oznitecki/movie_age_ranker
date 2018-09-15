import pickle
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

decription = raw_input("Enter a movie description: ")

trigrams = Set(nltk.trigrams(clean(decription).split()))
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

print "\nthis movie is probably " + mpaa + " rated"