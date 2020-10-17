from flask import Flask,request,jsonify
from flask_cors import CORS

from gensim.models.doc2vec import Doc2Vec
from util import get_tweet_pd,get_tweet_stats,collect_tweets,collect_trends

app = Flask(__name__)
CORS(app)


# load doc2vec model
doc2vec = Doc2Vec.load('./doc2vec/doc2vec_v1.model')

# predict authenticity of the news
@app.route("/predict",methods=["GET"])
def predict():
    q = request.args.get("q")
    res = get_tweet_pd(q,doc2vec)
    return jsonify(res)

# collect hourly stats
@app.route("/stats",methods=["GET"])
def stats():
    q = request.args.get("q")
    res = get_tweet_stats(q)
    return jsonify(res)

@app.route("/tweets",methods=["GET"])
def tweets():
    q = request.args.get("q")
    res = collect_tweets(q)
    return jsonify(res)    

@app.route("/trends",methods=["GET"])
def trends():
    
    res = collect_trends()
    return jsonify(res)

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5001)


