import string
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
import streamlit as st

""" data -> pandas series"""

EMOTIONS = {'happy':0, 'sadness':1, 'anger':2, 'fear':3, 'love':4, 'surprise':5}

def clean_text(data):

    punctuation = string.punctuation
    for p in punctuation:
        data = data.str.replace(p,'')

    data = data.str.lower()
    data = data.replace('(http://|https://|ftp://|ssh://)\S*','',regex=True)
    data = data.replace('@\S*','',regex=True)

    stops_r = list(map(lambda x: x.replace("'",""), stopwords.words('english')))
    stops = stopwords.words('english') + stops_r
    not_stop_words = ['didn',"hadn't",'wouldn',"mustn't", 'aren', 'doesn',"aren't", 'shant', 'not', 'hasnt', "needn't", 'couldnt', "isn't", "didn't",
                    "mightn't", "don't", 'haven', 'shouldn', 'neednt', 'wasn', 'dont', 'no', 'isn', 'havent', 'wasnt', 'hadnt', 'mightnt', 'mustn',
                    "shan't", "hasn't", 'couldn', 'don', 'werent', 'doesnt', "doesn't", 'mightn', 'arent', 'needn', "wasn't", 'didnt', 'weren', 'hasn',
                    'wouldnt', 'hadn', 'mustnt', "shouldn't", "weren't", 'won', "won't","couldn't", "haven't", "wouldn't", 'ain', 'aren', 'couldn', 'didn',
                    'doesn', 'hadn', 'hasn', 'haven', 'isn', 'isnt', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'shouldnt', 'wasn', 'weren', 'won',
                    'wont', 'wouldn']
    for w in not_stop_words:
        stops.remove(w)

    stops = set(stops)
    for word in stops:
        data = data.str.replace(' ' + word + ' ', ' ')
    return pd.DataFrame(data.str.replace('^i ', '', regex=True).replace('^im ', '', regex=True))

def texts_to_sequences(data, word_index):
    sequences = []
    for sentence in data:
        sentence = sentence.split()
        sequences.append([0 if w not in word_index.keys() else word_index[w] for w in sentence])
    return sequences

def prediction_to_emotions(prediction):
    arg = np.argmax(prediction, axis=1)
    key_list = list(EMOTIONS.keys())
    return pd.DataFrame([key_list[i] for i in arg], columns={'prediction'})