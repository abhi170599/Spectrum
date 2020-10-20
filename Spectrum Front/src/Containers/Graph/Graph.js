import React, { Component } from 'react';
import LineChart from 'react-linechart';

 
import './graph.css';

export default class Graph extends Component {
    render() {
        var dataPoints = null;
        console.log(this.props)
        if(this.props.data!==null){
        dataPoints =  this.props.stat.map((v,i)=>{
            return {x:i+1,y:v}
        }); 
    }


        const data = [
            {									
                color: "white", 
                xLabel: "Hours from Origin",
                yLabel: "% of tweets",
                points: dataPoints 
            }
        ];
        return (
            <div>
                <div className="graph">
                
                    <LineChart 
                        width={700}
                        height={250}
                        data={data}
                    />
                </div>				
            </div>
        );
    }
}