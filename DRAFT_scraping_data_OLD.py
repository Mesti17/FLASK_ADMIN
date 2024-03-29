from flask import Flask, render_template, request
import tweepy
import pandas as pd
import re
import os

path = "data_scraping"


def cari():

    # client = tweepy.Client(bearer_token="AAAAAAAAAAAAAAAAAAAAAMP6bAEAAAAAbEBt9bnifXMUG%2BcP8Pbt0rxTo%2F0%3DAVMwUuBirJHGiIuGorxWalSLQ2TeTlCMZdwgffhA7WTLMkPUgh",
    #                        consumer_key="ZHrfmilC6viwW6PbPU1taJ4uP",
    #                        consumer_secret="GDJDT4AgzoauafyP2pLkCpgBNb9nW4vSyg7EofWp4zB0mmA0wr",
    #                        access_token="1512143020648386585-nlWO1PsMNXcNnrrMQVOqMOpUfsjorh",
    #                        access_token_secret="Jv42ZmzsILSCJHRDkhI6WL12KwWd4dTOrwLK1bTyOF1r2")
    # return client

    API_KEY = "gwHLgCMqZ3PDnU0xpq5vbvPxa"
    API_KEY_SECRET = "ABsMw4guZKrNJKOgTGF4LpZRemzUFT2pNGgr8tslSj4BDlfVPm"
    BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAK%2B9lgEAAAAAjSAZPsz0k5Bioh%2F1%2F7gcj6iWWoc%3DIbZlWhY0O5dKm8cjnpKqY37pkPAIEia1hLyfHbqrN33rCudcQi"
    ACCESS_TOKEN = "3465396372-BcaLYvTGYzAWkGHCCSYaU1M37DvruBkRQOhiDtY"
    ACCESS_TOKEN_SECRET = "7QTf87DDwq7MClRBSSYfyUm8NSbGbJhs8zd6M16wgAdXM"

    client = tweepy.Client(bearer_token=BEARER_TOKEN,
                           consumer_key=API_KEY,
                           consumer_secret=API_KEY_SECRET,
                           access_token=ACCESS_TOKEN,
                           access_token_secret=ACCESS_TOKEN_SECRET
                           )
    return client


def search_tweets_anies(query):
    data_anies = []

    client = cari()
    tweets = client.search_recent_tweets(query=query, max_results=100)
    tweet_data = tweets.data

    # if db.is_connected():
    #     print("Berhasil terhubung ke database")
    #     cursor = db.cursor()
    if not tweet_data is None and len(tweet_data) > 0:
        for tweet in tweet_data:

            username = tweet.id
            pesan = tweet.text.encode("utf-8")

            # sql = "INSERT INTO user(username,tweet,label) VALUE (%s,%s,%s)"
            # data = (username, pesan, "")
            data_anies.append({
                'Username': username,
                'Tweet': pesan,
            })
            # cursor.execute(sql, data)
            # db.commit()

    df = pd.DataFrame(data_anies)
    df.to_csv(os.path.join(path, "scraping_anies.csv"),
              index=False, encoding="utf-8")


def search_tweets_prabowo(query):
    data_prabowo = []

    client = cari()
    tweets = client.search_recent_tweets(query=query, max_results=100)
    tweet_data = tweets.data

    # if db.is_connected():
    #     print("Berhasil terhubung ke database")
    #     cursor = db.cursor()
    if not tweet_data is None and len(tweet_data) > 0:
        for tweet in tweet_data:

            username = tweet.id
            pesan = tweet.text.encode("utf-8")

            # sql = "INSERT INTO user(username,tweet,label) VALUE (%s,%s,%s)"
            # data = (username, pesan, "")
            data_prabowo.append({
                'Username': username,
                'Tweet': pesan,
            })
            # cursor.execute(sql, data)
            # db.commit()

    df = pd.DataFrame(data_prabowo)
    df.to_csv(os.path.join(path, "scraping_prabowo.csv"),
              index=False, encoding="utf-8")


def search_tweets_ganjar(query):
    data_ganjar = []

    client = cari()
    tweets = client.search_recent_tweets(query=query, max_results=100)
    tweet_data = tweets.data

    # if db.is_connected():
    #     print("Berhasil terhubung ke database")
    #     cursor = db.cursor()
    if not tweet_data is None and len(tweet_data) > 0:
        for tweet in tweet_data:

            username = tweet.id
            pesan = tweet.text.encode("utf-8")

            # sql = "INSERT INTO user(username,tweet,label) VALUE (%s,%s,%s)"
            # data = (username, pesan, "")
            data_ganjar.append({
                'Username': username,
                'Tweet': pesan,
            })
            # cursor.execute(sql, data)
            # db.commit()

    df = pd.DataFrame(data_ganjar)
    df.to_csv(os.path.join(path, "scraping_ganjar.csv"),
              index=False, encoding="utf-8")


def scraping_tweet():
    tweet_anies = search_tweets_anies("Anies Baswedan")
    tweet_prabowo = search_tweets_prabowo("Prabowo Subianto")
    tweet_ganjar = search_tweets_ganjar("Ganjar Pranowo")
