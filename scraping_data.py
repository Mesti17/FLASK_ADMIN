import re
import pandas as pd
import os
import time
import csv
from getpass import getpass
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By

path = "dataset/data_scraping"

def scrape_tweet(search_term):
    edgeOption = webdriver.EdgeOptions()
    edgeOption.use_chromium = True
    driver = webdriver.Edge(options=edgeOption)
    driver.get("https://twitter.com/login")

    time.sleep(2)

    # enter email
    email = driver.find_element(By.TAG_NAME, "input")
    email.send_keys("sentimen2024@gmail.com")

    time.sleep(2)

    # press on the "next" button
    all_buttons = driver.find_elements(By.XPATH, "//div[@role='button']")
    all_buttons[-2].click()

    time.sleep(2)

    heading = driver.find_element(By.XPATH, "//h1[@role='heading']").text

    if "Enter your phone number or username" in heading:
        
        #mengisi username
        username = driver.find_element(By.TAG_NAME, "input")
        username.send_keys("sentimen2024")

        time.sleep(2)

        #click button    
        all_buttons = driver.find_elements(By.XPATH, "//div[@role='button']")
        all_buttons[-1].click()

        time.sleep(5)

        #Mengisi password
        password = driver.find_element(By.XPATH, "//input[@type='password']")
        password.send_keys("Olofmeister")

        time.sleep(2)

        all_buttons = driver.find_elements(By.XPATH, "//div[@role='button']")
        all_buttons[-1].click()
        
    else:
        
        #isi password dan kemudian login
        password = driver.find_element(By.XPATH, "//input[@type='password']")
        password.send_keys("Olofmeister")
        # password.send_keys("Mesti1957301014")
        # password.send_keys("@Homest4y")

        time.sleep(2)

        # press on the login button
        all_buttons = driver.find_elements(By.XPATH, "//div[@role='button']")
        all_buttons[-1].click()  
    
    time.sleep(2)
    keyword = search_term
    driver.get("https://twitter.com/search?q="+"%20%23"+keyword+f"%20lang%3Aid%20-filter%3Alinks&src=typed_query")

    time.sleep(5)

    tweet_set = set()
    target_tweet = 300

    while len(tweet_set) < target_tweet:
        tweets = driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')
        last_tweet_count = len(tweet_set)

        for tweet in tweets:
            try:
                iklan = tweet.find_element(By.XPATH, ".//span[contains(text(), 'Promoted')]").text
                continue  # Skip the promoted tweet
            except NoSuchElementException:
                pass

            try:
                tag_text = tweet.find_element(By.CSS_SELECTOR, 'div[data-testid="User-Name"]').text
                nama, username, dot, waktu = tag_text.split('\n')
            except (NoSuchElementException, ValueError):
                tag_text = ""  # Set an empty value if user name is not present
                nama = ""
                username = ""
                dot = ""
                waktu = ""

            tweet_text = tweet.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetText"]').text
            tweet_set.add((nama, username, tweet_text))

            if len(tweet_set) >= target_tweet:
                break

        if last_tweet_count == len(tweet_set):
            # No new unique tweets were loaded, break out of the loop
            break

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        
    df = pd.DataFrame(tweet_set, columns=["Username", "Nama", "Tweet"])    
    df.to_csv(os.path.join(path, "Scraping_"+search_term+"2.csv"), index=False, encoding="utf-8")
    
    driver.quit()   
    
