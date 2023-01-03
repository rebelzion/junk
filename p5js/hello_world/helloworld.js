let velocityX = 85;
let velocityY = 0;
let objX = getRandomInt(0, window.innerWidth);
let objY = getRandomInt(0, window.innerHeight);
var ellipses = [];

function setup() {
    createCanvas(window.innerWidth, window.innerHeight);
}

function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1)) + min;
}


function draw() {
  background(240);
    let trace_length = 50;
    if (ellipses.length > trace_length){
        ellipses.shift();
    }
    ellipses.push({objX, objY, velocityX, velocityY});
  for (el of ellipses) {
      //console.log("el=", el);
      ellipse(el.objX, el.objY, 100, 100);
  }

    if (mouseIsPressed) {
        velocityX = 85;
        velocityY = 0;
    }

  // Update the position of the text
  objX += velocityX;
  objY += velocityY;
  velocityX *= 0.99;
  velocityY *= 0.99;
  // Check if the text has reached the edge of the canvas
  if (objX > width || objX < 0) {
    velocityX *= -1;
  }
  if (objY > height || objY < 0) {
    velocityY *= -1;
  }
}
