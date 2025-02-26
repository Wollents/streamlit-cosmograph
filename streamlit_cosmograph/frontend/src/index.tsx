import React from "react"
import ReactDOM from "react-dom"
// import { StreamlitProvider } from "streamlit-component-lib-react-hooks"
import StreamlitCosmoGraph from "./StreamlitCosmoGraph"


ReactDOM.render(
  <React.StrictMode>
      <StreamlitCosmoGraph/>
  </React.StrictMode>,
  document.getElementById("root")
);