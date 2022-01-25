// index.js
// Fork of an original work by John Chin-Jew (https://codepen.io/johnchinjew/pen/JYWYXq)
// vars
var src, trmnl, caret, pos, speed;
trmnl = $('#terminal');
caret = $('#caret');
pos = 0;
speed = 3;

// main
$('html').on('keydown', function(e) {
  pos += speed;
  if (pos > src.length + speed - src.length % speed) {
    //pos = 0;
  }
  trmnl.html(trmnl.html() + src.slice(pos - speed, pos));
  caret.removeClass('transparent');
  line.css({
    'top': caret.offset().top
  });
  window.scrollTo(0, document.body.scrollHeight);
});

// caret animation
setInterval(function() {
  caret.toggleClass('transparent');
}, 600);

// filler code
src = "\n\n\n|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\n";
src+= "|||||                  ZEUS SAT 2019  - CONSOLE                   |||||||\n";
src+= "|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\n";
src+= "[+] Sending 1024 bytes . . .\n"
src+= ">> Connecting on Sattelite Zeus\n>> Connection Established\n...\n...\n";
