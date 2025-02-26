import React, { ReactNode,useState } from "react";
import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import { Cosmograph } from '@cosmograph/react'
function getRandomColor() {
  const letters = '0123456789ABCDEF';
  let color = '#';
  for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}

class StreamlitCosmoGraph extends StreamlitComponentBase{
    public render = (): React.ReactNode => {
      const nodes = Array.from({ length: 10000 }, (_, index) => ({
        id: `${index + 1}`, 
        color: getRandomColor()
    }));

      // Dynamically generate links array. For simplicity, we'll connect each node to the next one.
      const links = [];
      for (let i = 1; i <= 10000; i++) {
          links.push({ source: `${i}`, target: `${i + 1}` });
      }
        return (
            <span>
               <Cosmograph
                  nodes={nodes}
                  links={links}
                  nodeColor={d => d.color}
                  nodeSize={5}
                  disableZoom={false}
                  linkWidth={2}
                  disableSimulation={false}
                />
            </span>
        )
    }
} 

export default withStreamlitConnection(StreamlitCosmoGraph)