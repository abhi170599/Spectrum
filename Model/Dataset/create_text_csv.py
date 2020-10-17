'''
Filename : create_text_csv.py
Script to collect all the tweets and news articles from politifact dataset
@author:Abhishek Jha
'''

import csv
import json
import os
from tqdm import tqdm

#Dataset paths
BASE_DIR = "../../politifact/"
FAKE_DIR = BASE_DIR+"fake/"
REAL_DIR = BASE_DIR+"real/"

#function to create a list of tweet text from a 'tweet' directory
def collect_tweets(path):
    tweets = []
    files = os.listdir(path)
    for file in files:
        with open(path+"/"+file,'r') as json_file:
            data = json.load(json_file)
            tweets.append([data["text"]])
    return tweets

#fucntion to create a list of tweet texts from a base dir
def Tweets(dir):
    tweets = []
    articles = os.listdir(dir)
    num_articles = len(articles)
    for i in tqdm(range(num_articles)):
        article = articles[i]
        path = os.path.join(dir,article)
        if os.path.exists(path+"/tweets"):
            path = os.path.join(path,"tweets")
            tweets+=collect_tweets(path)

    return tweets

def collect_news_articles(dir):
    news_text = []
    articles = os.listdir(dir)
    num_articles = len(articles)
    for i in tqdm(range(num_articles)):
        article = articles[i]
        file_path = os.path.join(dir,article,"news_content.json")
        if os.path.exists(file_path):
            with open(file_path,'r') as json_file:
                data=json.load(json_file)
                news_text.append([data["text"]])
    return news_text




if __name__=="__main__":
    tweets_fake = Tweets(FAKE_DIR)
    tweets_real = Tweets(REAL_DIR)
    news_fake   = collect_news_articles(FAKE_DIR)
    news_real   = collect_news_articles(REAL_DIR)


    texts = tweets_fake+tweets_real+news_fake+news_real

    csv_file_path = "../../Generated_Data/text_doc2vev.csv"
    #write the tweets to the file
    with open(csv_file_path,'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['text'])
        writer.writerows(texts)












