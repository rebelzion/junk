
var size = 1024;
function setup() {
  createCanvas(size, size);
  background(220);
}

function getIntersection(r, s){

  let r_px = r.a.x;
  let r_py = r.a.y;
  let r_dx = r.b.x - r.a.x;
  let r_dy = r.b.y - r.a.y;

  let s_px = s.a.x;
  let s_py = s.a.y;
  let s_dx = s.b.x - s.a.x;
  let s_dy = s.b.y - s.a.y;

  //Are they parallel?
  if(r_dx*s_dy == r_dy*s_dx){
    return null;
  }

  const T2 = (r_dx*(s_py-r_py) + r_dy*(r_px-s_px))/(s_dx*r_dy - s_dy*r_dx);

  const T1 = (s_py+s_dy*T2-r_py)/r_dy;

  if(T1 < 0){
    return null;
  }
  if(T2 < 0 || T2 > 1){
    return null;
  }

  return {
    x: r_px+r_dx*T1,
    y: r_py+r_dy*T1,
    param: T1
  };
}

function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1)) + min;
}



function create_square_at(x, y, height, width) {

  let xleft = x - width / 2;
  let xright = x + width / 2;
  let yleft = y - height / 2;
  let yright = y + height / 2;

  return [
    {a: {x: xleft, y: yleft}, b: {x: xright, y: yleft}},
    {a: {x: xright, y: yleft}, b: {x: xright, y: yright}},
    {a: {x: xright, y: yright}, b: {x: xleft, y: yright}},
    {a: {x: xleft, y: yright}, b: {x: xleft, y: yleft}},
  ];
}


var segs = [
  //border
  {a: {x:0, y:0}, b: {x: size, y: 0}},
  {a: {x:0, y:0}, b: {x: 0, y: size}},
  {a: {x:0, y:size}, b: {x: size, y: size}}
];


var rays = [];

for (let i = 0; i < 10; i++) {
  segs.push(...create_square_at(
    getRandomInt(400, 500),
    getRandomInt(400, 700),
    height=getRandomInt(15, 20),
    width=getRandomInt(10, 20)));
}

function l2_distance(p, q) {
  return Math.sqrt((p.x - q.x)**2 + (q.y - q.y)**2);
}

function mouseClicked() {
  rays.push({x: mouseX, y: mouseY});
}

function draw() {
  background(0);
  stroke('red');
  strokeWeight(1);

  for (var ray of rays) {
    stroke('orange');
    fill('orange');
    circle(ray.x, ray.y, 10);
  }


  if (mouseIsPressed) {

    for (var i = 0; i < rays.length; i++) {
      let mpos = {x: mouseX, y: mouseY};
      d = l2_distance(rays[i], mpos);
      if (d <= 5+2) {
        rays[i].x = mouseX;
        rays[i].y = mouseY;
      }
    }

  }

  stroke('red');
  for(let seg of segs){
    line(seg.a.x, seg.a.y, seg.b.x, seg.b.y);
  }

  beginShape();
  // rays.push({x: mouseX, y: mouseY});
  for(let j = 0; j < PI*2; j+=PI*2/100){
    for (var r of rays.concat([{x: mouseX, y: mouseY}])){
      let ray = {a: {x: r.x, y: r.y}, b: {x: r.x+sin(j), y: r.y+cos(j)}};
      //Finding the closest intersection
      let closestIntersection = null;
      for(let seg of segs){
        let intersect = getIntersection(ray, seg);
        if(!intersect) continue;
        if(!closestIntersection || intersect.param < closestIntersection.param){
          closestIntersection = intersect;
        }
      }
      stroke('white');
      if(closestIntersection){
        line(ray.a.x, ray.a.y, closestIntersection.x, closestIntersection.y);
        fill('white');
        circle(closestIntersection.x, closestIntersection.y, 5);
      }
    }
  }
  endShape(CLOSE);


}
