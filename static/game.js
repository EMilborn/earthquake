var canvas = document.getElementById("gamecanvas");
var ctx = canvas.getContext("2d");

ctx.beginPath();
ctx.arc(100, 100, 25, 0, 2*Math.PI);
ctx.fillStyle = "red";
ctx.fill();
ctx.stroke();
ctx.closePath();

//http://javascript.info/tutorial/keyboard-events
document.body.onkeydown = function(e) {
    switch (e.keyCode) {
        case 37:
            $.get("/input", {key:"LeftArrow"});
            return false;
        case 38:
            $.get("/input", {key:"UpArrow"});
            return false;
        case 39:
            $.get("/input", {key:"RightArrow"});
            return false;
        case 40:
            $.get("/input", {key:"DownArrow"});
            return false;
    }
}

var mainLoop = function() {
    $.get("/fetch", function(d) {
        d = JSON.parse(d);
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.beginPath();
        ctx.arc(d.x, d.y, 25, 0, 2*Math.PI);
        ctx.fillStyle = "red";
        ctx.fill();
        ctx.stroke();
        ctx.closePath();
    });
    setTimeout(mainLoop, 50);
}
mainLoop();
