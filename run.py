
from gensim import corpora, models, similarities  
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string
import csv

def get_report(explanation):
    model =  models.LdaModel.load('./static/lda.model')
    file = open('./static/dictionary.csv')
    csvreader = csv.reader(file)

    words = []
    for row in csvreader:
        words.append(row[1])

    topics = ['not valid data type/ too many arguments / variable not intialized', 'unable to import', ' documentation not set/ variable property not set','syntax error', 'function not defined, function is not returning the correct item' ]
    # for i in range(0, model.num_topics):
    #     print(f"Topic {i+1}:")
    #     print (model.print_topic(i))

    doc_complete = []
    doc_complete.append(explanation)

    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation) 
    lemma = WordNetLemmatizer()

    def clean(doc):
        stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
        punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
        normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
        return normalized

    doc_clean = [clean(doc).split() for doc in doc_complete]
    def check(index):
        for items in doc_term_matrix:
            if items[0] == index:
                return False
        return True

    doc_term_matrix = []
    for word in doc_clean[0]:
        if word in words:
            index = words.index(word)
            item = tuple()
            if check(index):
                item = (index, 1)
                doc_term_matrix.append(item)
            else:
                for i in doc_term_matrix:
                    if i[0] == index:
                        id = i[1] + 1
                        doc_term_matrix.remove(i);
                        doc_term_matrix.append((index, id))
    print(doc_term_matrix)
        


    # doc_term_matrix = [(0, 1), (88, 1), (110, 1), (111, 1)]
    print("Topic is:")
    flag = False
    pos = 0
    index = sorted(model[doc_term_matrix], key=lambda tup: -1*tup[1])[0][0]
    return topics[index]
        

    