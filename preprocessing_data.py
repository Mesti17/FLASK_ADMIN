import pickle
import pymysql
# import swifter
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
# import mysql.connector
import pandas as pd
import numpy as np
import string
import re  # regex library
import matplotlib.pyplot as plt
import pymysql
# import word_tokenize & fregdist from NLTK
import nltk
nltk.download('punkt')
nltk.download('stopwords')


conn = pymysql.connect(host='localhost', port=int(
    3306), user='root', password='', db='capres')

df = pd.read_sql_query("SELECT * FROM sentimen", conn)


df['case_folding'] = df['pesan'].str.lower()


def remove_tweet_special(text):
    # remove tab, new line, ans back slice
    text = text.replace('\\t', " ").replace(
        '\\n', " ").replace('\\u', " ").replace('\\', " ")

    # remove non ASCII (emoticon, chinese word. etc)
    text = text.encode('ascii', 'replace').decode('ascii')

    # remove mention, link, hastaq
    text = ' '.join(
        re.sub("([@#][A-Za-z0-9]+)|(\w+:\/\/\S+)", " ", text).split())

    # removw incomplete URL
    return text.replace("http://", " ").replace("https://", " ")


df['cleaning'] = df['case_folding'].apply(remove_tweet_special)


# remove number
def remove_number(text):
    return re.sub(r"\d+", "", text)


df['cleaning'] = df['cleaning'].apply(remove_number)

# remove punctution


def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))


df['cleaning'] = df['cleaning'].apply(remove_punctuation)

# remove whitespace leading & trailing


def remove_whitespace_LT(text):
    return text.strip()


df['cleaning'] = df['cleaning'].apply(remove_whitespace_LT)

# remove multiple whitespace into single whitespace


def remove_whitespace_multiple(text):
    return re.sub('\s+', ' ', text)


df['cleaning'] = df['cleaning'].apply(remove_whitespace_multiple)

# remove single char


def remove_single_char(text):
    return re.sub(r"\b[a-zA-Z]\b", "", text)


df['cleaning'] = df['cleaning'].apply(remove_single_char)


# get stopword from NLTK stopword
# get stopword indonesia
list_stopwords = stopwords.words('indonesian')
data = 'https://raw.githubusercontent.com/Braincore-id/IndoTWEEST/main/stopwords_twitter.csv'

# manualy add stopword
# append additional stopword
list_stopwords.extend(['yg', 'dg', 'dgn', 'ny', 'klo', 'kalo',
                       'biar', 'bikin', 'bilang', 'gak', 'ga', 'krn',
                       'nya', 'nih', 'sih', 'si', 'tau', 'utk', 'ya',
                       'jd', 'jgn', 'sdh', 'aja', 'nyg', '&amp', 'yah',
                       'loh', 'rt', 'hehe', 'pen', 'u', 't', 'd', 'amp'])


df_stopwords = pd.read_csv(data, names=['stopword'])
df_stopwords = df_stopwords.sort_values(by="stopword", ascending=True)
df_stopwords.reset_index(drop=True, inplace=True)

new_stopwords = []

for data in df_stopwords['stopword']:
    new_stopwords.append(data)

list_stopwords.extend(new_stopwords)
len(list_stopwords)
list_stopwords.sort()

# remove stopword pada list token


def stopwords_removal(words):
    wordlist = words.split()
    return [word for word in wordlist if word not in list_stopwords]


ser = pd.Series(df['cleaning'].apply(stopwords_removal))

kata2 = []
for pjg in range(len(ser)):
    gabung2 = " ".join(ser[pjg])
    kata2.append(gabung2)


kata2_series = pd.Series(kata2)
df['hasil_stopwords'] = kata2_series


# # TOKENIZING


def word_tokenize_wrapper(text):
    return word_tokenize(text)


df['tweet_tokens'] = df['hasil_stopwords'].apply(word_tokenize_wrapper)

# STEMMING
# create stemming
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# stemmed


def stemmed(term):
    return stemmer.stem(term)


term_dict = {}

for document in df['tweet_tokens']:
    for term in document:
        if term not in term_dict:
            term_dict[term] = " "


n = 1
for term in term_dict:
    term_dict[term] = stemmed(term)

    # apply stemmed term to dataframe


def get_stemmer_term(document):
    return [term_dict[term] for term in document]


df['tweet_stemmer'] = df['tweet_tokens'].swifter.apply(get_stemmer_term)

# Mengubah "Positif" jadi 1 , "Neutral" jadi 0,     dan "Negatif" jadi -1

angka = []
for el in range(len(df["label"])):

    if df["label"][el] == "positif":
        angka_baru = 1
    elif df["label"][el] == "netral":
        angka_baru = 0
    else:
        angka_baru = -1
    angka.append(angka_baru)


angka_series = pd.Series(angka)
df['label_angka'] = angka_series

# acak baris data
df = df.sample(frac=1).reset_index(drop=True)

# Rearrange kolom
new_col = ['id_calon', 'username', 'pesan', 'label', 'label_angka',
           'case_folding', 'cleaning', 'hasil_stopwords', 'tweet_tokens', 'tweet_stemmer']
df = df.reindex(columns=new_col)

# Check which columns contain empty strings
columns_with_empty_strings = df.columns[df.isin(['']).any()].tolist()
# Identify rows with empty strings in the specified columns
empty_string_rows = df[df[columns_with_empty_strings].isin(
    ['']).any(axis=1)].index

# Delete rows with empty strings in any of the specified columns
df = df.drop(empty_string_rows)

df.to_csv('data_bersih/hasil_preprocessing.csv', index=False)
