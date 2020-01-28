# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 18:08:15 2020

@author: kleok
"""

# pip install gensim
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
import pandas as pd

Reviews = df["review_comment"]


stemmer = SnowballStemmer("english")

import nltk
nltk.download('wordnet')

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

# example
init_review = df["review_comment"][1]
stem1 = lemmatize_stemming(init_review)
preprocessed = preprocess(stem1)



processed_reviews = []

for review in Reviews:
    processed_reviews.append(preprocess(lemmatize_stemming(review)))
    
    
# Bag of words
dictionary = gensim.corpora.Dictionary(processed_reviews)


bow_corpus = [dictionary.doc2bow(rev) for rev in processed_reviews]

lda_model =  gensim.models.LdaMulticore(bow_corpus, 
                                   num_topics = 5, 
                                   id2word = dictionary,                                    
                                   passes = 10,
                                   workers = 2)



for idx, topic in lda_model.print_topics(-1):
    print("Topic: {} \nWords: {}".format(idx, topic ))
    print("\n")


unseen_document = init_review
bow_vector = dictionary.doc2bow(preprocess(unseen_document))

for index, score in sorted(lda_model[bow_vector], key=lambda tup: -1*tup[1]):
    print("Score: {}\t Topic: {}".format(score, lda_model.print_topic(index, 5)))
    
    
# Sentiment Analysis
    
import nltk;
nltk.download('punkt')
from textblob import TextBlob

blob1 = TextBlob("I hate Monday")
print(format(blob1.sentiment))

init_review_textblob = TextBlob(init_review)
init_review_textblob.sentences


from nltk.tokenize import sent_tokenize
sent_tokenize(init_review)
['Hello World.', "It's good to see you.", 'Thanks for buying this book.']

k = 0
for x in sent_tokenize(init_review):
    print("counter %d, %s"% (k, x))
    k += 1
    
######################## Workflow Implementation #######################################
    
Reviews = df["review_comment"]

stemmer = SnowballStemmer("english")

import nltk
nltk.download('wordnet')

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

# break it to sentences
    
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
        
##### Remove companies #####

lda_model =  gensim.models.LdaMulticore(bow_corpus, 
                                   num_topics = 5, 
                                   id2word = dictionary,                                    
                                   passes = 10,
                                   workers = 2)

for idx, topic in lda_model.print_topics(-1):
    print("Topic: {} \nWords: {}".format(idx, topic ))
    print("\n")
    

    
bow_corpus = [dictionary.doc2bow(rev) for rev in processed_reviews]

###### Sentiment score #######
sentence_polarity = []
sentence_sensitivity = []
for sentence in review_sentences:
    sentence_polarity.append(TextBlob(sentence).sentiment.polarity)
    sentence_sensitivity.append(TextBlob(sentence).sentiment.subjectivity)
#I have many zeros
    


    


    
    
    