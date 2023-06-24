from flask import Flask, render_template, request
import snscrape.modules.twitter as sntwitter
import tweepy
import pandas as pd
import re
import os

path = "dataset/data_scraping"


def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


def search_tweets_prabowo():
    data_prabowo = []

    for i, tweet in enumerate(sntwitter.TwitterSearchScraper("Prabowo Subianto").get_items()):
        if i > 100:
            break
        data_prabowo.append([tweet.user.username, tweet.content])

        # db.commit()

    df = pd.DataFrame(data_prabowo, columns=['Username', "Tweet"])
    df.to_csv(os.path.join(path, "scraping_prabowo.csv"),
              index=False, encoding="utf-8")


def search_tweets_ganjar():
    data_ganjar = []

    for i, tweet in enumerate(sntwitter.TwitterSearchScraper("Ganjar Pranowo").get_items()):
        if i > 100:
            break
        data_ganjar.append([tweet.user.username, tweet.content])

        # db.commit()

    df = pd.DataFrame(data_ganjar, columns=['Username', "Tweet"])
    df.to_csv(os.path.join(path, "scraping_ganjar.csv"),
              index=False, encoding="utf-8")


def search_tweets_anies():
    data_anies = []

    for i, tweet in enumerate(sntwitter.TwitterSearchScraper("Anies Baswedan").get_items()):
        if i > 100:
            break
        data_anies.append([tweet.user.username, tweet.content])

        # db.commit()

    df = pd.DataFrame(data_anies, columns=['Username', "Tweet"])
    df.to_csv(os.path.join(path, "scraping_anies.csv"),
              index=False, encoding="utf-8")
