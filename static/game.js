// $.get("/game", {})

var id = document.getElementById("thegame").innerHTML
var gameid = -1
var canvas = document.getElementById("gamecanvas");
var ctx = canvas.getContext("2d");
ctx.beginPath();
ctx.arc(100, 100, 25, 0, 2*Math.PI);
ctx.fillStyle = "red";
ctx.fill();
ctx.stroke();
ctx.closePath();
var socket = io.connect('http://' + document.domain + ':' + location.port);
var latestGameData = 0;
socket.on('connect', function() {
    var tn = document.createElement("p");
    tn.innerHTML = "Connected to server.";
    document.body.appendChild(tn);
    var deltn = function() {
        document.body.removeChild(tn);
    }
    setTimeout(deltn, 4000)
});
socket.on('gamedata', function(json) {
    latestGameData = JSON.parse(json)[gameid];
})
socket.on('join', function(json) {
    json = JSON.parse(json);  // lol
    if json['user'] == id:
        gameid = json['game']
})
//http://javascript.info/tutorial/keyboard-events
document.body.addEventListener("keydown", function(e) {
    switch (e.keyCode) {
        case 37:
            socket.emits("input", JSON.stringify({user:id, key:"LeftArrow", state:true}));
            return false;
        case 38:
            socket.emits("input", JSON.stringify({user:id, key:"UpArrow", state:true}));
            return false;
        case 39:
            socket.emits("input", JSON.stringify({user:id, key:"RightArrow", state:true}));
            return false;
        case 40:
            socket.emits("input", JSON.stringify({user:id, key:"DownArrow", state:true}));
            return false;
    }
})

    switch (e.keyCode) {
        case 37:
            socket.emits("input", JSON.stringify({user:id, key:"LeftArrow", state:false}));
            return false;
        case 38:
            socket.emits("input", JSON.stringify({user:id, key:"UpArrow", state:false}));
            return false;
        case 39:
            socket.emits("input", JSON.stringify({user:id, key:"RightArrow", state:false}));
            return false;
        case 40:
            socket.emits("input", JSON.stringify({user:id, key:"DownArrow", state:false}));
            return false;
    }
})

var mainLoop = function() {
    d = latestGameData;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for(var i=0; i<d.length; i++) {
        ctx.beginPath();
        ctx.arc(d[i].x, d[i].y, 25, 0, 2*Math.PI);
        ctx.fillStyle = "red";
        ctx.fill();
        ctx.stroke();
        ctx.closePath();
    });
    setTimeout(mainLoop, 100);
}
mainLoop();
