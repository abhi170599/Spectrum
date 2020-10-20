import React from 'react'
import './Query.css'
import {Component} from 'react'
import search from './si.png'
import mic from './m.png'

class Query extends Component{

      
    
      render(){

             return(
                    <div className="Query">
                           
                           <input type="text"  value = {this.props.query} onChange={this.props.input_query} className="input" placeholder="Search for an Event"/>
                           <img src={mic} style={{height:"18px","margin-right":"2%","margin-top":"0.8%","margin-left":"2%",float:"left"}} alt="search"/>

                           <img src={search} style={{height:"19px","margin-right":"2%","margin-top":"0.8%","margin-left":"1%",float:"right"}} alt="search" onClick={this.props.onSubmit}/>
                           
                           

                    </div>
             )

      }

}

export default Query;
