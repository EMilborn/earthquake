// $.get("/game", {})

// var io = require('socket.io')
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
// connect(location.protocol + '//' + document.domain + ':' + location.port);
var socket = io()
var latestGameData = 0;
tempMsg = function(message, time) {  // time in ms
    var newEl = document.createElement("p");
    newEl.innerHTML = message;
    document.body.appendChild(newEl);
    var killEl = function() {
        document.body.removeChild(newEl);
    }
    setTimeout(killEl, time);
}
socket.on('connect', function() {
    tempMsg("Connected to server.", 4000);
    socket.emit('message', 'hello')
});
socket.on('hello', function(d) {
    console.log('server said ' + d);
});

socket.on('join', function(gid) {
    console.log('server said to join')
    gameid = gid
    // socket.emit('message', 'joined')
    // tempMsg(json, 10000);
    // json = JSON.parse(json);  // lol
    // tempMsg(json.user, 5000);
    // tempMsg(json.game, 5000);
    // if (json.user === id) {
    //     gameid = json.game;
    //     tempMsg("Connected to game, id = " + gameid, 10000);
    // }
});

socket.on('gamedata', function(json) {
    console.log('got that data')
    //tempMsg('Got gamedata', 500);
    latestGameData = json;
    console.log(latestGameData)
});


//http://javascript.info/tutorial/keyboard-events
document.body.addEventListener("mousedown", function(e) {
    socket.emit("input", JSON.stringify({user:id, key:"Mouse1", state:true}));
});

document.body.addEventListener("mouseup", function(e) {
    socket.emit("input", JSON.stringify({user:id, key:"Mouse1", state:false}));
});

document.body.addEventListener("keydown", function(e) {
    switch (e.keyCode) {
        case 37:
            socket.emit("input", {user:id, key:"LeftArrow", state:true});
            return false;
        case 38:
            socket.emit("input", {user:id, key:"UpArrow", state:true});
            return false;
        case 39:
            socket.emit("input", {user:id, key:"RightArrow", state:true});
            return false;
        case 40:
            socket.emit("input", {user:id, key:"DownArrow", state:true});
            return false;
    }
});

document.body.addEventListener("keyup", function(e) {
    switch (e.keyCode) {
        case 37:
            socket.emit("input", {user:id, key:"LeftArrow", state:false});
            return false;
        case 38:
            socket.emit("input", {user:id, key:"UpArrow", state:false});
            return false;
        case 39:
            socket.emit("input", {user:id, key:"RightArrow", state:false});
            return false;
        case 40:
            socket.emit("input", {user:id, key:"DownArrow", state:false});
            return false;
    }
})

var mainLoop = function() {
    if (gameid === -1) {
        socket.emit("givegame", {"user": id});
    }
    else {
        socket.emit("givedata", {"game": gameid})
    }
    d = latestGameData;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for(var i=0; i<d.length; i++) {
        ctx.beginPath();
        ctx.arc(d[i].x, d[i].y, 25, 0, 2*Math.PI);
        ctx.fillStyle = "red";
        ctx.fill();
        ctx.stroke();
        ctx.closePath();
    };
    setTimeout(mainLoop, 100);
}
mainLoop();
