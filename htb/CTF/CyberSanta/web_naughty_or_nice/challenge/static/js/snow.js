// From: https://codepen.io/whqet/pen/vyzPGR
(function() {
    var winW = window.innerWidth;
    var winH = window.innerHeight;
    var num = 500;
    var snowArray = new Array();
  
    function random(min, max, isInt) {
      var a = min + Math.random() * (max - min);
      return isInt ? parseInt(a) : a;
    }
    //Snow类的构造函数
    function Snow() {
      this.init();
      this.draw();
    }
    //Snow类的参数初始化
    Snow.prototype.init = function() {
        //设置初始的坐标、速度、风、大小、透明度
        this.x = random(0, winW, true);
        this.y = random(-winH, 0, true);
        this.speed = random(0.5, 3);
        this.wind = random(-2, 2);
        this.size = random(3, 6, true);
        this.alpha = random(0.2, 1);
      }
      //Snow类的绘制
    Snow.prototype.draw = function() {
        //雪花添加到页面，并且初始值赋值
        this.o = document.createElement("div");
        this.o.className = "snow";
        document.body.appendChild(this.o);
        this.o.style.width = this.o.style.height = this.size + "px";
        this.o.style.opacity = this.alpha;
      }
      //Snow类的位置更新
    Snow.prototype.update = function() {
      this.x += this.wind;
      this.y += this.speed;
  
      if (this.y > winH) {
        this.init();
      }
  
      this.o.style.left = this.x + "px";
      this.o.style.top = this.y + "px";
    }
  
    //生成Snow粒子
    for (var i = 0; i < num; i++) {
      var snow = new Snow();
      snowArray.push(snow);
    }
  
    //运动Snow粒子
    (function() {
      for (var i = 0; i < snowArray.length; i++) {
        snowArray[i].update();
      }
      requestAnimationFrame(arguments.callee);
    }());
  }());