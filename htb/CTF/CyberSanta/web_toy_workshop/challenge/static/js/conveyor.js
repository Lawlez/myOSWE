// Conveyor inspired from https://codepen.io/dariocorsi/pen/yOOBJK

var inputItem = document.getElementsByClassName('trash-in')[0];
var outputItem = document.getElementsByClassName('toy-out')[0];

var index = 0;

var ChristmasPresents = document.getElementsByClassName('ChristmasPresents');

function cycleChristmasPresents(){
  setInterval(function(){

    for (var i = 0; i < ChristmasPresents.length; ++i){
      ChristmasPresents[i].classList.remove('active');
      ChristmasPresents[i].classList.remove('active');
    };

    ChristmasPresents[index].classList.add('active');
    ChristmasPresents[index].classList.add('active');

    if(index < ChristmasPresents.length -1 ){
      index = index + 1;
    } else{
      index = 0;
    }

    console.log('index', index);  
  }, 10000);
};

cycleChristmasPresents();
// JavaScript Document
var c = document.getElementById('tiffany_snow'), 
    $c = c.getContext("2d");
var w = c.width = window.innerWidth, 
    h = c.height = window.innerHeight;

Snowy();
function Snowy() {
  var snow, arr = [];
  var num = 600, tsc = 1, sp = 1;
  var sc = 1.3, t = 0, mv = 20, min = 1;
    for (var i = 0; i < num; ++i) {
      snow = new Flake();
      snow.y = Math.random() * (h + 50);
      snow.x = Math.random() * w;
      snow.t = Math.random() * (Math.PI * 2);
      snow.sz = (100 / (10 + (Math.random() * 100))) * sc;
      snow.sp = (Math.pow(snow.sz * .8, 2) * .15) * sp;
      snow.sp = snow.sp < min ? min : snow.sp;
      arr.push(snow);
    }
  go();
  function go(){
    window.requestAnimationFrame(go);
      $c.clearRect(0, 0, w, h);
      $c.fillStyle = 'hsla(242, 95%, 3%, 1)';
      $c.fillRect(0, 0, w, h);
      $c.fill();
        for (var i = 0; i < arr.length; ++i) {
          f = arr[i];
          f.t += .05;
          f.t = f.t >= Math.PI * 2 ? 0 : f.t;
          f.y += f.sp;
          f.x += Math.sin(f.t * tsc) * (f.sz * .3);
          if (f.y > h + 50) f.y = -10 - Math.random() * mv;
          if (f.x > w + mv) f.x = - mv;
          if (f.x < - mv) f.x = w + mv;
          f.draw();}
 }
 function Flake() {
   this.draw = function() {
      this.g = $c.createRadialGradient(this.x, this.y, 0, this.x, this.y, this.sz);
      this.g.addColorStop(0, 'hsla(255,255%,255%,1)');
      this.g.addColorStop(1, 'hsla(255,255%,255%,0)');
      $c.moveTo(this.x, this.y);
      $c.fillStyle = this.g;
      $c.beginPath();
      $c.arc(this.x, this.y, this.sz, 0, Math.PI * 2, true);
      $c.fill();}
  }
}
/*________________________________________*/
// window.addEventListener('resize', function(){
//   c.width = w = window.innerWidth;
//   c.height = h = window.innerHeight;
// }, false);


