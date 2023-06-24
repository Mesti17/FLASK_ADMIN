import pandas as pd
import os
import pymysql

conn = pymysql.connect(host='localhost', port=int(
    3306), user='root', passwd='', db='capres')

negative_words = pd.read_csv(
    "dataset/data_label/negatif_ta2.csv", header=None)[0].tolist()
positive_words = pd.read_csv(
    "dataset/data_label/positif_ta2.csv", header=None)[0].tolist()

df = pd.read_csv("dataset/data_scraping/tweet_gabungan.csv")

# Function to count the number of negative and positive words in a tweet


def count_sentiment_words(tweet):
    negative_count = sum(1 for word in tweet.split()
                         if word.lower() in negative_words)
    positive_count = sum(1 for word in tweet.split()
                         if word.lower() in positive_words)
    return negative_count, positive_count


# Add columns for negative and positive word counts
df['Negative Count'] = 0
df['Positive Count'] = 0

# Iterate over each tweet and count the negative and positive words
for index, row in df.iterrows():
    tweet = row['Tweet']
    negative_count, positive_count = count_sentiment_words(tweet)
    df.at[index, 'Negative Count'] = negative_count
    df.at[index, 'Positive Count'] = positive_count

# Assign the label based on the count of negative and positive words
df['Label'] = 'netral'
df.loc[df['Negative Count'] > df['Positive Count'], 'Label'] = 'negatif'
df.loc[df['Positive Count'] > df['Negative Count'], 'Label'] = 'positif'
# df.loc[df['Positive Count'] == df['Negative Count'], 'Label'] = 'Positive'

df.to_csv("dataset/data_hasil_label/data_hasil_label.csv",
          index=False, encoding="utf-8")


# Create a cursor
cursor = conn.cursor()

# Define the SQL query
sql = "INSERT INTO sentimen (username, pesan, label) VALUES (%s, %s, %s)"


# Iterate over the rows of the DataFrame and insert each row into the table
for index, row in df.iterrows():
    values = (str(row['Username']), str(row['Tweet']), str(row['Label']))
    cursor.execute(sql, values)

# Commit the changes to the database
conn.commit()

# Close the connection
conn.close()
