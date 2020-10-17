"""
Twitter agent to extract tweets for given keywords
@author: Abhishek Jha
"""
import tweepy

class TweetAgent:

    #initialize the agent with a key
    def __init__(self,creds):
        self.creds = creds 
        self.auth  = tweepy.OAuthHandler(
            self.creds["CONSUMER_KEY"],
            self.creds["CONSUMER_SEC"]
        )

        self.auth.set_access_token(
            self.creds["ACCESS_TOKEN"],
            self.creds["ACCESS_SECRET"]
        )

        self.api = tweepy.API(self.auth) 
    
    ''' funtion to search for tweets
        @params: query : keywords
                 limit : maximum number of tweets
                 lang  : language for search
    '''
    def _search(self,query,limit,lang='en'):
        data = []
        try:
            tweets = tweepy.Cursor(self.api.search,
                                   q=query,
                                   lang=lang).items(limit)
            print("Extracted Tweets")
            print(tweets)                       

            #convert tweets to json
            for tweet in tweets:
                tweet_json = {}
                tweet_text = str(tweet.text)
                tweet_date = str(tweet.created_at)
                tweet_json["text"]=tweet_text
                tweet_json["date"]=tweet_date 
                data.append(tweet_json)

            return data
        except Exception as e:
            print(e)
            return None 

    ''' funtion to search for tweets
        @params: query : keywords
                 limit : maximum number of tweets
                 lang  : language for search
    '''
    def _tweets(self,query,limit,lang='en'):
        data = []
        try:
            tweets = tweepy.Cursor(self.api.search,
                                   q=query,
                                   lang=lang).items(limit)
            print("Extracted Tweets")
            print(tweets)                       

            #convert tweets to json
            for tweet in tweets:
                
                tweet_json = {}
                tweet_text = str(tweet.text)
                tweet_date = str(tweet.created_at)
                tweet_json["text"]=tweet_text
                tweet_json["date"]=tweet_date
                tweet_json["auth"]=tweet.user.name
                tweet_json["img"]=tweet.user.profile_image_url 
                data.append(tweet_json)

            return data
        except Exception as e:
            print(e)
            return None

    def trends(self):
        res = []
        trends = self.api.trends_place(id = 2282863) 
        for value in trends: 
            for trend in value['trends']:
                if trend['name'][2]!="u":
                    res.append(trend['name'])

        return {"msg":"success","trend":res,"status":200}








