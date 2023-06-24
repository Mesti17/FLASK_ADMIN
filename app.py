from flask import Flask, render_template, url_for, redirect
import os
import re
import requests
import numpy as np
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
# from scraping_data import scraping_tweet
from scraping_data import search_tweets_ganjar, search_tweets_anies, search_tweets_prabowo
import labeling_data
import preprocessing_data
from gabung_data import gabungdata

app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")


@app.route("/scraping_prabowo", methods=['GET', "POST"])
def scrapingTweetPrabowo():
    search_tweets_prabowo()
    return redirect(url_for("index"))


@app.route("/scraping_ganjar", methods=['GET', "POST"])
def scrapingTweetGanjar():
    search_tweets_ganjar()
    return redirect(url_for("index"))


@app.route("/scraping_anies", methods=['GET', "POST"])
def scrapingTweetAnies():
    search_tweets_anies()
    return redirect(url_for("index"))


@app.route("/gabungdata", methods=['GET', "POST"])
def gabungData():
    gabungdata()
    return redirect(url_for("index"))


@app.route("/labeldata", methods=['GET', "POST"])
def labelData():
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True, port=3000)
