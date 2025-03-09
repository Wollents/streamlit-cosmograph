import './style.css';
import { Graph, GraphConfigInterface } from '@cosmograph/cosmos';
import { Streamlit, RenderData } from "streamlit-component-lib"

// const div = document.getElementById('graph') as HTMLDivElement;
const div = document.body.appendChild(document.createElement("div"))
div.className = 'app';
const div_actions = document.body.appendChild(document.createElement("div"))
div_actions.className = 'actions';
let graph: Graph;
let click = false;
let frameHeight = 600;
const config: GraphConfigInterface = {
  spaceSize: 4096,
  backgroundColor: '#151515',
  pointSize: 4,
  pointColor: '#4B5BBF',
  pointGreyoutOpacity: 0.1,
  linkWidth: 0.01,
  linkColor: '#696969',
  linkArrows: false,
  linkGreyoutOpacity: 0,
  curvedLinks: true,
  renderHoveredPointRing: true,
  hoveredPointRingColor: '#4B5BBF',
  enableDrag: true,
  simulationLinkDistance: 1,
  simulationLinkSpring: 2,
  simulationRepulsion: 0.2,
  simulationGravity: 0.1,
  simulationDecay: 100000,
  fitViewOnInit: true,
  onClick: (
    index: number | undefined,
    pointPosition: [number, number] | undefined,
    event: MouseEvent
  ) => {
    click = true;
    console.log('clicking  ', click);
    if (index !== undefined) {  
      graph.selectPointByIndex(index);
      var neighbor = graph.getAdjacentIndices(index) || [];
      const return_dict = {"node": index, "neighbor": neighbor};
      Streamlit.setComponentValue(return_dict)
      neighbor?.push(index)
      graph.selectPointsByIndices(neighbor)
      graph.zoomToPointByIndex(index);
      graph.fitViewByPointIndices(neighbor)
    } else {
      console.log("unselecting index");
      graph.unselectPoints();
      
    }
    console.log('Clicked point index: ', index);
  },
};

graph = new Graph(div, config);

/* ~ Demo Actions ~ */
// Start / Pause
let isPaused = false;
const pauseButton = div_actions.appendChild(document.createElement("button"))
pauseButton.textContent = 'Pause';
pauseButton.addEventListener('click', togglePause);

const fitviewButton = div_actions.appendChild(document.createElement("button"))
fitviewButton.textContent = 'fitView';
fitviewButton.addEventListener('click', fitView);
function pause() {
  isPaused = true;
  pauseButton.textContent = 'Start';
  graph.pause();
}

function start() {
  isPaused = false;
  pauseButton.textContent = 'Pause';
  graph.start();
}

function togglePause() {
  if (isPaused) start();
  else pause();
}

function fitView() {
  graph.fitView();
}

function onRender(event: Event): void {
  // Get the RenderData from the event
  const data = (event as CustomEvent<RenderData>).detail
  console.log("receving data", data)

  // params from streamlit
  const nodes = data.args["nodes"];
  const links_ = data.args["links"];   
  const colors = data.args["colors"];
  const rec_configs = data.args["configs"];
  const simulation = rec_configs["simulation"];
  frameHeight = rec_configs["frameHeight"] || 600;
  Object.assign(config, rec_configs);

  // update graph
  graph.setPointPositions(nodes);
  graph.setLinks(links_);
  graph.setPointColors(colors);
  graph.render();
  graph.setConfig(config);

  pause();
  if(simulation!==false){
    console.log("starting simulation")
    
    start();
  }
  // just make sure to fitView
  setTimeout(() => {
    graph.fitView(250, 0.1); 
  }, 800);
  Streamlit.setFrameHeight(frameHeight);
}

// first RENDER_EVENT until we call this function.
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)

// Tell Streamlit we're ready to start receiving data. We won't get our
Streamlit.setComponentReady()

// Finally, tell Streamlit to update our initial height. We omit the
// `height` parameter here to have it default to our scrollHeight.
Streamlit.setFrameHeight(frameHeight)