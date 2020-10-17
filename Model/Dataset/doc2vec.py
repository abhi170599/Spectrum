'''
filename: doc2vec.py
script to create and train a Doc2Vec(CBOW) model from collected texts
@author:Abhishek Jha
'''

import nltk
nltk.download('punkt')

import pandas as pd
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import WordPunctTokenizer, word_tokenize
import re
from bs4 import BeautifulSoup
import warnings

warnings.simplefilter("ignore",UserWarning)


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


def create_doc2vec(text_list, model_path):
    # create tagged word list
    tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()),
                                  tags=[str(i)]) for i, _d in enumerate(text_list)]

    max_epochs = 100
    vec_size = 50
    alpha = 0.025

    # train the doc2vec model
    model = Doc2Vec(size=vec_size,
                    alpha=alpha,
                    min_alpha=0.00025,
                    min_count=1,
                    dm=1)

    model.build_vocab(tagged_data)

    for epoch in range(max_epochs):
        print('iteration {0}'.format(epoch))
        model.train(tagged_data,
                    total_examples=model.corpus_count,
                    epochs=model.iter)
        # decrease the learning rate
        model.alpha -= 0.0002
        # fix the learning rate, no decay
        model.min_alpha = model.alpha

    model.save(model_path)
    print("Model Saved")


if __name__ == "__main__":
    '''Read and clean the text dataset'''
    print('Cleaning the tweets ...')
    data = pd.read_csv("../../Generated_Data/text_doc2vev.csv")
    data["text"] = data["text"].apply(clean)

    print('Creating and Training Doc2Vec Model')
    create_doc2vec(data["text"],"doc2vec_v1.model")
