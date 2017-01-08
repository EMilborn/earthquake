// $.get("/game", {})

var canvas = document.getElementById("gamecanvas");
var ctx = canvas.getContext("2d");

ctx.beginPath();
ctx.arc(100, 100, 25, 0, 2*Math.PI);
ctx.fillStyle = "red";
ctx.fill();
ctx.stroke();
ctx.closePath();

//http://javascript.info/tutorial/keyboard-events
document.body.addEventListener("keydown", function(e) {
    switch (e.keyCode) {
        case 37:
            $.get("/input", {key:"LeftArrow", state:"Down"});
            return false;
        case 38:
            $.get("/input", {key:"UpArrow", state:"Down"});
            return false;
        case 39:
            $.get("/input", {key:"RightArrow", state:"Down"});
            return false;
        case 40:
            $.get("/input", {key:"DownArrow", state:"Down"});
            return false;
    }
})

document.body.addEventListener("keyup", function(e) {
    switch (e.keyCode) {
        case 37:
            $.get("/input", {key:"LeftArrow", state:"Up"});
            return false;
        case 38:
            $.get("/input", {key:"UpArrow", state:"Up"});
            return false;
        case 39:
            $.get("/input", {key:"RightArrow", state:"Up"});
            return false;
        case 40:
            $.get("/input", {key:"DownArrow", state:"Up"});
            return false;
    }
})

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
