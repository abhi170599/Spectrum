import React from 'react'
import {Component} from 'react'

import './Tweet.css'
import TweetHolder from '../../Components/TweetHolder/TweetHolder'

class Tweet extends Component{


      render(){
          console.log(this.props);
          return (

                <div className="Tweet">
                      {this.props.are_tweets===true?<h2 className="heading">Tweets</h2>:<h2 className="heading">Trending</h2>} 
                      <TweetHolder tweets={this.props.tweets} are_tweets={this.props.are_tweets}/>
                
                
                </div>

          )
      } 



}

export default Tweet;