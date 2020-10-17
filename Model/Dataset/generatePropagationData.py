"""
filename:generatePropagationData.py
generating dataset for propagation dynamics data
@author:Abhishek Jha
"""

from datetime import datetime
from gensim.models.doc2vec import Doc2Vec
from nltk.tokenize import WordPunctTokenizer, word_tokenize
import re
from bs4 import BeautifulSoup
import warnings
import os
from tqdm import tqdm
import numpy as np
import json
import math

# suppress warnings
# warnings.filterwarnings("ignore", UserWarning)

# parameters
PERIOD = 50  # num of hours to be considered
DATASET_PATH = "/home/abhi17/Work/Projects/Projects/Sutra/Generated_Data/Dynamics"


# load doc2vec model
doc2vec = Doc2Vec.load('../Doc2Vec/doc2vec_v1.model')

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


# get time difference
def get_time_difference(time1, time2):

    date_format = '%Y-%m-%d %H:%M:%S'
    diff = datetime.strptime(time2, date_format) - datetime.strptime(time1, date_format)
    return int(diff.total_seconds() // 3600)


def get_dynamics(tweet_path):
    # list of tweets
    tweets = os.listdir(tweet_path)
    dynamics = [{"vec": np.ones(50), "count": 0} for i in range(PERIOD)]
    tweet_vector = []
    for tweet in tweets:
        with open(tweet_path + "/" + tweet, 'r') as json_file:
            data = json.load(json_file)
            vector = doc2vec.infer_vector(word_tokenize(clean(data["text"])))
            date = data["created_at"]
            date = datetime.strftime(datetime.strptime(date,'%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')

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


def generate_data(dir, type):
    label = [0, 0]
    if type == "real":
        label[1] = 1
    else:
        label[0] = 1
    label = np.array(label)

    # read articles from the directory
    articles = os.listdir(dir)
    num_articles = len(articles)
    for i in tqdm(range(num_articles)):
        article_path = os.path.join(dir, articles[i])
        tweet_path = os.path.join(article_path, "tweets")
        if os.path.exists(tweet_path):
            dynamics = get_dynamics(tweet_path)
            data_path = os.path.join(DATASET_PATH, articles[i])
            if not os.path.exists(data_path):
                os.mkdir(data_path)
            data_X = os.path.join(data_path, "X.npy")
            data_Y = os.path.join(data_path, "Y.npy")
            np.save(data_X, dynamics)
            np.save(data_Y, label)


if __name__=="__main__":

    if not os.path.exists(DATASET_PATH):
        os.mkdir(DATASET_PATH)

    real_dir  = "../../politifact/real"
    fake_dir  = "../../politifact/fake"

    generate_data(real_dir,"real")
    generate_data(fake_dir,"fake")
