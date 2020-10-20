import React from 'react'
import {Component} from 'react'

import './Stat.css'
import Graph from '../Graph/Graph'

class Stat extends Component{


      render(){
            console.log(this.props)
           var show=null; 
          if(this.props.data===null){
                show = <h4>Search events to view Dynamics</h4>
          }else{
                show = <Graph stat={this.props.data}/>
          }
            
          return (

                <div className="Stat">
                      <h2>Dynamics</h2>  
                      <div className="stats">
                          {show}
                      </div>
                
                
                </div>

          )
      } 



}

export default Stat;