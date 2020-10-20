import React from 'react'
import './TweetHolder.css'

import Trend from '../Trend/Trend'
import Tweet from '../Tweet/Tweet_A'

const TweetHolder = (props) =>{
      
      if(props.tweets===null){
          return null;
      }
      var areTweets = props.are_tweets;
      
      if(areTweets===false){
          var trends = props.tweets.map(tweet=>{
                  return <Trend trend={tweet}/>;
          });
          return (
                    <div className="TrendHolder">
                        
                        {trends}
                    </div>

          )
      }

      var tweets = props.tweets.map(tweet=>{
          return <Tweet tweet={tweet}/>
      })
      return (
        <div className="TweetHolder">
                        
            {tweets}
        </div>
      );

}

export default TweetHolder;