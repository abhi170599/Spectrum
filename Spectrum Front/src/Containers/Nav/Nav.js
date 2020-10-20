import React from 'react';
import './Nav.css'
import spectrum from './spectrum_new.png'
import { Component } from 'react';

import Query from '../Query/Query'

class Nav extends Component{

      state={
          "query":"none"
      }
      
      
      render(){

           return(
               <div className="Nav">
                    
                    <img src={spectrum}  alt="Spectrum" className="Logo"/>
                    <Query query={this.props.query} input_query={this.props.on_change} onSubmit={this.props.onSubmit}/>
                    
               </div>     
           )
      }


}

export default Nav;

