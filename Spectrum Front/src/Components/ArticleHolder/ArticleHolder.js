import React from 'react'
import './ArticleHolder.css'

import Article from '../Article/Article';

const articleHolder = (props) =>{
          
      var items = null;
      if(props.articles!==null){
      
           items = props.articles.map(article=>{
               return <Article article={article}/> 
         })}

      return(
          <div className="article_holder">
              {items}
          </div>
      )


}

export default articleHolder;