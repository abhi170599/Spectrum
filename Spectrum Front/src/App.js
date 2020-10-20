import React from 'react';
import {Component} from 'react';
import axios from 'axios'

import './App.css';

import Nav from './Containers/Nav/Nav'
import News from './Containers/News/News'
import Tweet from './Containers/Tweet/Tweet'
import Stat from './Containers/Stats/Stats'


class App extends Component {


  state = {
         
     loading:true,
     query  :"none",
     articles:null,
     stats:null,
     tweets:null,
     res:"none",
     analysis:false,
     are_tweets:false

  }

  componentDidMount(){
    
    axios.get("http://newsapi.org/v2/top-headlines?country=In&category=business&apiKey=6fbc8038e2594c228ceb83618241780f")
         .then(res=>{
               
               const articles = res.data.articles;
               axios.get("http://0.0.0.0:5002/trends")
               .then(res=>{
                  var trends = res.data.trend;
                  console.log(trends)
                  const new_state={...this.state,articles:articles,tweets:trends,loading:false,are_tweets:false};
                  this.setState(new_state);
                  console.log(this.state);
               });
               
        });   
     
  }

  onQueryInput = (event) => {
    console.log(event.target.value);
    const new_state = {...this.state,query:event.target.value}
    this.setState(new_state);

  }
  
  getResults = () => {
       //send request for tweets
       this.setState({...this.state,loading:true});
       axios.get("http://localhost:5001/predict?q="+this.state.query)
            .then(res=>{
                 var result = res.data.res;

                 axios.get("http://localhost:5001/tweets?q="+this.state.query)
                      .then(res=>{
                        var tweets = res.data.tweets;
                        axios.get("http://localhost:5001/stats?q="+this.state.query)
                              .then(res=>{
                            var stats = res.data.stat;
                            var new_state = {...this.state,tweets:tweets,res:result,stats:stats,loading:false,are_tweets:true,analysis:true};
                            this.setState(new_state);
                            console.log(this.state);
                          

                              });
                      }); 
            });
      
            
      // get news articles      
      axios.get("http://newsapi.org/v2/everything?country=in&q="+this.state.query+"&apiKey=6fbc8038e2594c228ceb83618241780f")
            .then(res=>{

                   const new_state = {...this.state,articles:res.data.articles};
                   this.setState(new_state);

            });    


  }
  


  render(){
    const loading_bar = (<div className="loading">
                              <div className="loading_line_wrapper">
                                    <div className="loading_line">
                                        <div className="loading_line_inner loading_line_inner--1"></div>
                                        <div className="loading_line_inner loading_line_inner--2"></div>
                                    </div>
                              </div>
                        </div>)

    const line = (<div className="line"></div>)                    

    const style_real = {"background-image": "linear-gradient(to right,#000000,#000000,#0c2c02)"};
    const style_fake = {"background-image": "linear-gradient(to right,#000000,#000000,#360200)"};
    const style_nor  = {"background-image": "linear-gradient(to right,#000000,#000000,#09022c)"};

    var style_color;
    if(this.state.res==="real") style_color=style_real;
    else if(this.state.res==="fake") style_color=style_fake;
    else style_color=style_nor;
    

  return (
    <div className="App" style={style_color}>
      
         <Nav value={this.state.query} on_change={this.onQueryInput} onSubmit={this.getResults}/>
         {this.state.loading === true? loading_bar: line }
         <News articles={this.state.articles}/>
         <Tweet tweets={this.state.tweets} are_tweets={this.state.are_tweets}/>
         <Stat analysis={this.state.analysis} data={this.state.stats}/>

      
       
    </div>
  
  );
}

}

export default App;
