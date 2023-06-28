from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
import swifter
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
import mysql.connector
import pandas as pd
import numpy as np
import pickle
import pymysql
import nltk
nltk.download('punkt')
nltk.download('stopwords')


def modeldata():
    # menghubungkan ke database
    conn = pymysql.connect(host='localhost', port=int(
        3306), user='root', passwd='', db='capres')

    df = pd.read_sql_query("SELECT * FROM hasil_preprocessing ", conn)
    df2 = pd.read_sql_query("SELECT * FROM sentimen ", conn)

    # df.info()

    # TF-IDF

    vectorizer = TfidfVectorizer()
    v_data = vectorizer.fit_transform(df['tweet_stemmer']).toarray()

    # Split dataset dan bikin model

    x_train, x_test, y_train, y_test = train_test_split(
        v_data, df['label_angka'], test_size=0.2, random_state=0, shuffle=True)
    modelNB = MultinomialNB()
    md = modelNB.fit(x_train, y_train)
    pred_nb = modelNB.predict(x_test)

    # confusin matrix dan accuracy

    print(confusion_matrix(y_test, pred_nb))
    print(classification_report(y_test, pred_nb))
    print('nilai akurasinya adalah ', accuracy_score(y_test, pred_nb))

    # TES PREDIKSI

    teks = str(df2['pesan'])
    vec = vectorizer.transform([teks])
    prediksi = modelNB.predict(vec)

    if prediksi == 1:
        print('Sentimen tweet adalah POSITIF')
    else:
        print('Sentimen tweet adalah NEGATIF')

    # name file5
    filename = 'model_nb.pickle'

    # Save model
    pickle.dump(modelNB, open(filename, 'wb'))

    # Load model yg udah disimpan

    loaded_model = pickle.load(open('model_nb.pickle', "rb"))
