from flask import Flask, render_template, url_for, redirect
import os
import re
import requests
import numpy as np
import pandas as pd
# import nltk
# from nltk.tokenize import sent_tokenize, word_tokenize
# from nltk.corpus import stopwords
# from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
# from scraping_data import scraping_tweet
from scraping_data import scrape_tweet
from labeling_data import label_data
from preprocessing_data import preprocess
from gabung_data import gabungdata
from model import modeldata

app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")


@app.route("/scraping_prabowo", methods=['GET', "POST"])
def scrapingTweetPrabowo():
    scrape_tweet('Prabowo')
    return redirect(url_for("index"))


@app.route("/scraping_ganjar", methods=['GET', "POST"])
def scrapingTweetGanjar():
    scrape_tweet('Ganjar')
    return redirect(url_for("index"))


@app.route("/scraping_anies", methods=['GET', "POST"])
def scrapingTweetAnies():
    scrape_tweet('Anies')
    return redirect(url_for("index"))


@app.route("/gabungdata", methods=['GET', "POST"])
def gabungData():
    gabungdata()
    return redirect(url_for("index"))


@app.route("/labeldata", methods=['GET', "POST"])
def labelData():
    label_data()
    return redirect(url_for("index"))


@app.route("/preprocessing", methods=['GET', "POST"])
def preprocessingData():
    preprocess()
    return redirect(url_for("index"))


@app.route("/model", methods=['GET', "POST"])
def modelData():
    modeldata()
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True, port=3000)
