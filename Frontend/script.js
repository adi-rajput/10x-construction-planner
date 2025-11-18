// frontend/script.js

const API = "http://127.0.0.1:8000/trajectory";

const canvas = document.getElementById('cv');
const ctx = canvas.getContext('2d');
const cw = canvas.width, ch = canvas.height;

let currentPath = [];
let meta = null;
let playIdx = 0;
let playTimer = null;

function worldToCanvas(x, y, wall) {
  // scale world to fit canvas inside margins
  const margin = 20;
  const usableW = cw - margin*2;
  const usableH = ch - margin*2;
  const sx = usableW / wall.width;
  const sy = usableH / wall.height;
  const s = Math.min(sx, sy);
  const cx = margin + x * s;
  const cy = ch - (margin + y * s); // flip y
  return [cx, cy];
}

function drawAll(){
  ctx.clearRect(0,0,cw,ch);
  if(!meta) return;
  // draw wall border
  ctx.strokeStyle = "#000";
  ctx.lineWidth = 2;
  ctx.strokeRect(10,10,cw-20,ch-20);

  // draw obstacles
  for(const o of meta.obstacles){
    const [x1,y1] = worldToCanvas(o.x, o.y, meta.wall);
    const [x2,y2] = worldToCanvas(o.x + o.width, o.y + o.height, meta.wall);
    const w = x2 - x1;
    const h = y1 - y2;
    ctx.fillStyle = "#cc0000";
    ctx.fillRect(x1, y2, w, h); // y2 is top in canvas coords after flip
  }

  // draw path lines
  if(currentPath && currentPath.length>0){
    ctx.strokeStyle = "#0066ff";
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    const [sx,sy] = worldToCanvas(currentPath[0][0], currentPath[0][1], meta.wall);
    ctx.moveTo(sx,sy);
    for(let i=1;i<currentPath.length;i++){
      const [cx,cy] = worldToCanvas(currentPath[i][0], currentPath[i][1], meta.wall);
      ctx.lineTo(cx,cy);
    }
    ctx.stroke();

    // draw small circles for points for clarity (optional)
    ctx.fillStyle = "#0066ff";
    for(const p of currentPath){
      const [cx,cy] = worldToCanvas(p[0], p[1], meta.wall);
      ctx.beginPath(); ctx.arc(cx,cy,1.5,0,Math.PI*2); ctx.fill();
    }
  }
}

function drawPointerAt(i){
  drawAll();
  if(!currentPath || currentPath.length==0) return;
  const p = currentPath[i];
  const [cx,cy] = worldToCanvas(p[0], p[1], meta.wall);
  ctx.fillStyle = "#ff9900";
  ctx.beginPath(); ctx.arc(cx,cy,6,0,Math.PI*2); ctx.fill();
}

document.getElementById('createBtn').onclick = async () => {
  const name = document.getElementById('name').value;
  const wallW = parseFloat(document.getElementById('wallW').value);
  const wallH = parseFloat(document.getElementById('wallH').value);
  const res = parseFloat(document.getElementById('res').value);

  const payload = {
    name,
    wall: {width: wallW, height: wallH},
    obstacles: [{x:1.0,y:1.0,width:0.25,height:0.25}], // example window
    resolution: res
  };

  const r = await fetch(API + "/create", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify(payload)
  });
  const data = await r.json();
  console.log("create:", data);
  // load created item
  await loadLast();
};

async function loadLast(){
  const r = await fetch(API + "/list?skip=0&limit=1");
  const list = await r.json();
  if(list.length==0) return;
  // get the first item's id
  const id = list[0].id;
  const r2 = await fetch(API + "/" + id);
  const obj = await r2.json();
  currentPath = obj.path;
  meta = obj.meta;
  document.getElementById('explain').innerText = `Loaded id=${id} name=${obj.name}`;
  drawAll();
}

document.getElementById('playBtn').onclick = () => {
  if(!currentPath || currentPath.length==0) return;
  if(playTimer){ clearInterval(playTimer); playTimer = null; return; }
  playIdx = 0;
  playTimer = setInterval(()=>{
    drawPointerAt(playIdx);
    playIdx++;
    if(playIdx >= currentPath.length) { clearInterval(playTimer); playTimer=null; }
  }, 25); // 25ms per step -> adjust
}

document.getElementById('loadBtn').onclick = loadLast;

// initial draw
drawAll();
