import React from 'react'
import './Article.css'

const article = (props) =>{
        
      return(
               <div className="article">   
                   <div className="Image"
                   style={{ backgroundImage: `url(${props.article.urlToImage})` }}
                   
                   />
                   <div className="info">
                   <h5 className="title">{props.article.description}</h5>
                   <div className="sub_info">
                        <div className="author">{props.article.author}</div>
                        <div className="date">{props.article.publishedAt}</div>
                   </div>
                   </div>

               </div>   
           

      )


}

export default article;