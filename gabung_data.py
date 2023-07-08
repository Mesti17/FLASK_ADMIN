import pandas as pd
import os

path = "dataset/data_scraping"


def gabungdata():
    
    df1 = pd.read_csv(path+"/Scraping_Anies2.csv")
    df2 = pd.read_csv(path+"/Scraping_Ganjar2.csv")
    df3 = pd.read_csv(path+"/Scraping_Prabowo2.csv")

    df4 = pd.concat([df1, df2, df3])

    # acak baris data
    df4 = df4.sample(frac=1).reset_index(drop=True)

    df4.to_csv(path+"/tweet_gabungan.csv", index=False, encoding="utf-8")