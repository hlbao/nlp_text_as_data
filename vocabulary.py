import nltk, re, string
from nltk.corpus import conll2000
from nltk.tokenize import sent_tokenize
import numpy as np
recover_list = {"wa":"was", "ha":"has"}


class VocabularySentenceLayer:
    def __init__(self, stopwords, wl, excluds_stopwords=False):
        self.vocas = []        # id to word
        self.vocas_id = dict() # word to id
        self.docfreq = []      # id to document frequency
        self.excluds_stopwords = excluds_stopwords
        self.stopwords = stopwords
        self.wl =  wl
        self.table = {ord(c): None for c in string.punctuation}

    def is_stopword(self, w):
        return w in self.stopwords

    def lemmatize(self, w0):
        w0 = w0.translate(self.table)
        w = self.wl.stem(w0.lower())
        if w in recover_list:
            return recover_list[w]
        return w

    def term_to_id(self, term0, training):
        term = self.lemmatize(term0)
        if not re.match(r'[a-z]+$', term): 
            return None
        if self.excluds_stopwords and self.is_stopword(term): 
            return None
        try:  
            term_id = self.vocas_id[term]
        except:
            if not training: 
                return None
            term_id = len(self.vocas)
            self.vocas_id[term] = term_id
            self.vocas.append(term)
            self.docfreq.append(0)
        return term_id
