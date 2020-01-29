# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 20:06:21 2020

@author: kleok
"""

######################## Workflow Implementation #######################################
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
import pandas as pd
import nltk
nltk.download('wordnet')
from textblob import TextBlob
from nltk.tokenize import sent_tokenize


# from Anne-Claire's dataframe  
Reviews = df["review_comment"]

stemmer = SnowballStemmer("english")


# lemmatize the verbs - bring to the initial form
def lemmatize_stemming(text):
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))
# Tokenize and lemmatize
def preprocess(text):
    result=[]
    for token in gensim.utils.simple_preprocess(text) :
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))       
    return result

# break reviews to sentences
review_sentences = []
for review in Reviews:
    for x in sent_tokenize(review):
        review_sentences.append(x)
        
# Clean data
processed_reviews = []
for sentence in review_sentences:
    processed_reviews.append(preprocess(lemmatize_stemming(sentence)))
    
# Dictionary
dictionary = gensim.corpora.Dictionary(processed_reviews)

# Bag of words
bow_corpus = [dictionary.doc2bow(rev) for rev in processed_reviews]
        
##### TO DO -  Remove companies' names #####

lda_model =  gensim.models.LdaMulticore(bow_corpus, 
                                   num_topics = 5,   # choose correct number 
                                   id2word = dictionary,                                    
                                   passes = 10,
                                   workers = 2)

# print topics
for idx, topic in lda_model.print_topics(-1):
    print("Topic: {} \nWords: {}".format(idx, topic ))
    print("\n")
    

    
# bow_corpus = [dictionary.doc2bow(rev) for rev in processed_reviews]

###### Sentiment score #######
sentence_polarity = []
sentence_sensitivity = []
for sentence in review_sentences:
    sentence_polarity.append(TextBlob(sentence).sentiment.polarity)
    sentence_sensitivity.append(TextBlob(sentence).sentiment.subjectivity)
#I have many zeros
    
