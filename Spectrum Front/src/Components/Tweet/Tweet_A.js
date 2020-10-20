import React from 'react'
import './Tweet_A.css'



const Tweet = (props) =>{

      return(

              <div className="Tweet_A">
                   <div className="header">
                       <img className="profile" src={props.tweet.img} alt="p"/>
                        <b>{props.tweet.auth}</b>
                        <br/>
                        
                        {props.tweet.date}
                     
                   </div>
                   <div className="text">
                        {props.tweet.text}
                   </div> 


              </div>  
      ) 

}

export default Tweet;