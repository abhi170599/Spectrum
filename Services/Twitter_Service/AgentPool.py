'''
 Twitter Agent Pool to allocate agents on per request basis
 @author:Abhishek Jha
'''

from TwitterAgent import TweetAgent

class AgentPool:
    
    ''' 
        init
        @cred_list: list of twitter credentials       
    '''
    def __init__(self,cred_list):
        self.num_agents = len(cred_list)
        self.cred_list = cred_list

        #initialize the list of agents
        self.agents = [TweetAgent(cred_list[i]) for i in range(self.num_agents)]

        #initialize the turn to 0
        self.turn = 0
    
    ''' funtion to search for tweets
        @params: query : keywords
                 limit : maximum number of tweets
    '''
    def search(self,query,limit=100,lang='en'):
        self.turn = (self.turn+1)%self.num_agents
        try:
            data = self.agents[self.turn]._search(query,limit,lang)
            return data 
        except Exception as e:
            print(e)
            return None

    def tweets(self,query,limit=10,lang='en'):
        self.turn = (self.turn+1)%self.num_agents
        try:
            data = self.agents[self.turn]._tweets(query,limit,lang)
            return data 
        except Exception as e:
            print(e)
            return None

    def trends(self):
        self.turn = (self.turn+1)%self.num_agents
        try:
            data = self.agents[self.turn].trends()
            return data 
        except Exception as e:
            print(e)
            return None                     

        



