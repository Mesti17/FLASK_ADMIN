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
from scraping_data import scraping_tweet

app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")


@app.route("/scraping", methods=['GET', "POST"])
def scrapingTweet():
    scraping_tweet()
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True, port=3000)
