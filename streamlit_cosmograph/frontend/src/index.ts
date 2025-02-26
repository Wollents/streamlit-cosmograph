import './style.css';
import { pointPositions, links } from "./data-gen";
import { Graph, GraphConfigInterface } from '@cosmograph/cosmos';
import { Streamlit, RenderData } from "streamlit-component-lib"

// const div = document.getElementById('graph') as HTMLDivElement;
const div = document.body.appendChild(document.createElement("div"))
div.className = 'app';
const div_actions = document.body.appendChild(document.createElement("div"))
div_actions.className = 'actions';
let graph: Graph;
let click = false;
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
    if (index !== undefined) {
      click = true;
      console.log('clicking  ', click);
      graph.selectPointByIndex(index);
      var neighbor = graph.getAdjacentIndices(index) || [];
      const return_dict = {"node": index, "neighbor": neighbor};
      Streamlit.setComponentValue(return_dict)
      neighbor?.push(index)
      graph.selectPointsByIndices(neighbor)
      graph.zoomToPointByIndex(index);
      graph.fitViewByPointIndices(neighbor)
    } else {
      graph.unselectPoints();
    }
    console.log('Clicked point index: ', index);
  },
};

graph = new Graph(div, config);
// const canvas = div.querySelector('canvas');
graph.setPointPositions(pointPositions);
graph.setLinks(links);

graph.zoom(0.8);
graph.render();

/* ~ Demo Actions ~ */
// Start / Pause
let isPaused = false;
const pauseButton = div_actions.appendChild(document.createElement("button"))
pauseButton.textContent = 'Pause';

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

pauseButton.addEventListener('click', togglePause);

// Zoom and Select
function getRandomPointIndex() {
  return Math.floor((Math.random() * pointPositions.length) / 2);
}

function getRandomInRange([min, max]: [number, number]): number {
  return Math.random() * (max - min) + min;
}

function fitView() {
  graph.fitView();
}

function zoomIn() {
  const pointIndex = getRandomPointIndex();
  graph.zoomToPointByIndex(pointIndex);
  graph.selectPointByIndex(pointIndex);
  pause();
}

function selectPoint() {
  const pointIndex = getRandomPointIndex();
  graph.selectPointByIndex(pointIndex);
  graph.fitView();
  pause();
}

function selectPointsInArea() {
  const w = canvas.clientWidth;
  const h = canvas.clientHeight;
  const left = getRandomInRange([w / 4, w / 2]);
  const right = getRandomInRange([left, (w * 3) / 4]);
  const top = getRandomInRange([h / 4, h / 2]);
  const bottom = getRandomInRange([top, (h * 3) / 4]);
  pause();
  graph.selectPointsInRange([
    [left, top],
    [right, bottom],
  ]);
}
function onRender(event: Event): void {
  // Get the RenderData from the event
  const data = (event as CustomEvent<RenderData>).detail
  console.log("receving data", data)

  // 从Streamlit接收数据
  const nodes = data.args["nodes"]; // 假设Python端传递了points参数
  const links_ = data.args["links"];   // 假设Python端传递了links参数
  const colors = data.args["colors"];
  const configs = data.args["configs"];
  const layout = configs["layout"] || "Random"
  console.log("receiving configs", configs)
  if(click){
    console.log("click is", click);
    if(click){
      click = false;
      console.log("chaning click to ", click)
      return;
    }
  }
  // 更新图形数据
  graph.setPointPositions(nodes);
  graph.setLinks(links_);
  graph.setPointColors(colors);
  graph.render();
  pause();
  console.log("layout is", layout)
  if(layout == "Random"){
    start();
  }
  fitView();
  Streamlit.setComponentValue(undefined);
  
  Streamlit.setFrameHeight(600)
}
// first RENDER_EVENT until we call this function.
Streamlit.setComponentReady()
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
// Tell Streamlit we're ready to start receiving data. We won't get our

// Finally, tell Streamlit to update our initial height. We omit the
// `height` parameter here to have it default to our scrollHeight.
Streamlit.setFrameHeight(600)
const fitviewButton = div_actions.appendChild(document.createElement("button"))
fitviewButton.textContent = 'fitView';
fitviewButton.addEventListener('click', fitView);


