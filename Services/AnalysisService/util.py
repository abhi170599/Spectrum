"""
Utility funtions to generate propagation dynamics from tweets
"""
from datetime import datetime
import nltk
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import WordPunctTokenizer, word_tokenize
import re
from bs4 import BeautifulSoup
import warnings
import numpy as np
import json
import math

import requests


warnings.simplefilter("ignore",UserWarning)
tweet_url = "http://twt:5002/search?q={}"
tweets    = "http://twt:5002/tweets?q={}"
trends    = "http://twt:5002/trends"
model_url = "http://tfs:8501/v1/models/FakeNews:predict"

PERIOD = 50


# function to clean the tweet
tok = WordPunctTokenizer()
pat1 = r'@[A-Za-z0-9]+'
pat2 = r'https?://[A-Za-z0-9./]+'
combined_pat = r'|'.join((pat1, pat2))


# function to clean the text
def clean(text):
    soup = BeautifulSoup(text, 'lxml')
    souped = soup.get_text()
    stripped = re.sub(combined_pat, '', souped)
    try:
        cleaned = stripped.decode("utf-8-sig").replace(u"\ufffd", "?")
    except Exception as e:
        cleaned = stripped

    letters_only = re.sub("[^a-zA-Z]", " ", cleaned)
    lower_case = letters_only.lower()
    # During the letters_only process two lines above, it has created necessary white spaces,
    # I will tokenize and join together to remove unnecessary white spaces
    words = tok.tokenize(lower_case)
    return (" ".join(words)).strip()


#function to get time difference
def get_time_difference(time1, time2):

    date_format = '%Y-%m-%d %H:%M:%S'
    diff = datetime.strptime(time2, date_format) - datetime.strptime(time1, date_format)
    return int(diff.total_seconds() // 3600)


# function to generate dynamics data
def get_dynamics(tweets,doc2vec):
    # list of tweets
    
    dynamics = [{"vec": np.ones(50), "count": 0} for i in range(PERIOD)]
    tweet_vector = []
    for data in tweets:
            
            vector = doc2vec.infer_vector(word_tokenize(clean(data["text"])))
            date = data["date"]
            #date = datetime.strftime(datetime.strptime(date,'%a %b %d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')

            tweet_vector.append({"vec": vector, "date": date})

    # sort by date
    tweet_vector.sort(key=lambda x: x["date"])
    init_date = tweet_vector[0]["date"]
    for i in range(1, len(tweet_vector)):

        _time = tweet_vector[i]["date"]
        diff = get_time_difference(init_date, _time)
        if diff < PERIOD and diff >= 0:

            vec = tweet_vector[i]["vec"]

            if dynamics[diff]["count"] == 0:
                dynamics[diff]["vec"] = vec
                dynamics[diff]["count"] += 1
            else:
                dynamics[diff]["vec"] += vec
                dynamics[diff]["count"] += 1

    matrix = []
    for i in range(PERIOD):
        scaling = math.log(dynamics[i]["count"] + 1) + 1
        matrix.append(scaling * dynamics[i]["vec"] / (dynamics[i]["count"] + 1))

    return np.array(matrix)




#collect number of tweets done hourly
def collect_hourly_stats(tweets):
    stats = [0]*PERIOD
    tweets.sort(key=lambda x:x["date"])
    init_date = tweets[0]["date"]
    for i in range(1, len(tweets)):

        _time = tweets[i]["date"]
        diff = get_time_difference(init_date, _time)
        if diff < PERIOD and diff >= 0:
           stats[diff]+=1

    return stats        
            

def collect_tweets(query):
    response    = requests.get(tweets.format(query))
    tweets_json = response.json()
    if tweets_json["status"]!=200:
        return {"msg":"tweets not found","status":401}
    return response.json()

def collect_trends():
    response    = requests.get(trends)
    tweets_json = response.json()
    if tweets_json["status"]!=200:
        return {"msg":"tweets not found","status":401}
    return response.json()



def get_tweet_stats(query):
    response    = requests.get(tweet_url.format(query))
    tweets_json = response.json()
    if tweets_json["status"]!=200:
        return {"msg":"tweets not found","status":401}
    stats = collect_hourly_stats(tweets_json["tweets"])
    print(stats)
    return {"stat":stats,"status":200}




def get_tweet_pd(query,doc2vec):
    

    response    = requests.get(tweet_url.format(query))
    tweets_json = response.json()
    if tweets_json["status"]!=200:
        return {"msg":"tweets not found","status":401}

    dynamics    = get_dynamics(tweets_json["tweets"],doc2vec)
    
    # query the tensorflow model
    data = json.dumps({"instances":[{"input_dyn":dynamics.tolist()}]})
    headers = {"content-type": "application/json"}

    json_res = requests.post(model_url,data=data,headers=headers)
    print(json_res.json())
    #json_res = model_request(data,headers)
    res = json_res.json()["predictions"]
    if np.argmax(res)==1:
        return {"res":"real","status":200}
    return {"res":"fake","status":200}



"""

if __name__=="__main__":

    doc2vec = Doc2Vec.load("./doc2vec/doc2vec_v1.model")
    res = get_tweet_pd("tesla to launch model y",doc2vec)
    print(res)

"""










