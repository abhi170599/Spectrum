import React from 'react'
import {Component} from 'react'



import './News.css'

import ArticleHolder from '../../Components/ArticleHolder/ArticleHolder'


class News extends Component{
      
      

      render(){
          return (

                <div className="News">
                      <h2>Articles</h2> 
                      <ArticleHolder articles={this.props.articles}/>
                
                
                </div>

          )
      } 



}

export default News;