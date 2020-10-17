from flask import Flask,request,jsonify 
from flask_cors import CORS 

from AgentPool import AgentPool
import json 

app = Flask(__name__)
CORS(app)

"""
Read the cred list from the json file
"""
with open('creds.json','r') as creds:
    data = json.load(creds)
    cred_list = data["creds"]

agent_pool = AgentPool(cred_list)

@app.route("/search",methods=["GET"])
def search():
    q = request.args.get('q')
    try:
        tweets = agent_pool.search(q)
        if tweets==None:
            return jsonify({
                "msg":"unsuccessful",
                "status":501
            })
        elif len(tweets)==0:
            return jsonify({
                "msg":"no tweets",
                "status":502
            })
        return jsonify({
            "tweets":tweets,
            "msg"   :"success",
            "status":200
        })
    except Exception as e:
        print(e)
        return jsonify({
            "msg":"unsuccessful",
            "status":500
        })

@app.route("/tweets",methods=["GET"])
def get_tweets():
    q = request.args.get('q')
    try:
        tweets = agent_pool.tweets(q)
        if tweets==None:
            return jsonify({
                "msg":"unsuccessful",
                "status":501
            })
        elif len(tweets)==0:
            return jsonify({
                "msg":"no tweets",
                "status":502
            })
        return jsonify({
            "tweets":tweets,
            "msg"   :"success",
            "status":200
        })
    except Exception as e:
        print(e)
        return jsonify({
            "msg":"unsuccessful",
            "status":500
        })

@app.route("/trends",methods=["GET"])
def get_trends():
    
    try:
        res = agent_pool.trends()
        return jsonify(res)
    except Exception as e:
        print(e)
        return jsonify({
            "msg":"unsuccessful",
            "status":500
        })        


if __name__=="__main__":
    app.run(host="0.0.0.0",port=5002)        




