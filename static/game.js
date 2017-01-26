// $.get("/game", {})

// var io = require('socket.io')
var state = 'WAITING'
/* states:
WAITING - user hasn't queued yet
QUEUEING - user is in queue
PLAYING - user is in game
*/
var id = document.getElementById("thegame").innerHTML;
var gameid = -1;
var canvas = document.getElementById("gamecanvas");
var ctx = canvas.getContext("2d");
ctx.textAlign = "center";
var width = canvas.width;
var height = canvas.height;
var queuebutton = document.getElementById("queuebutton");
var map = -1;
var me = {x: 0, y: 0};
var names = {};
queuebutton.addEventListener("click", function(e) {
    state = 'QUEUEING';
    queuebutton.style.display = 'none'
})

drawCircle = function(x, y, r, col) {
    ctx.beginPath();
    ctx.arc(x, y, r, 0, 2*Math.PI);
    ctx.fillStyle = col;
    ctx.strokeStyle = 'rgba(0,0,0,0)';
    ctx.fill();
    ctx.stroke();
    ctx.closePath();
}

getOffsets = function(myX, myY) {
    return {
        x: width / 2 - myX,  // so that player is always centered
        y: height / 2 - myY
    }
}

drawPlayer = function(myX, myY, x, y, name) {
    var o = getOffsets(myX, myY);
    drawCircle(x + o.x, y + o.y, 25, "red");
    ctx.font = "24px Arial";
    ctx.fillStyle = "white";
    ctx.fillText(name, x + o.x, y + o.y + 6)

}

drawBullet = function(myX, myY, x, y) {
    var o = getOffsets(myX, myY);
    drawCircle(x + o.x, y + o.y, 10, "blue");
}

drawMap = function(myX, myY) {  // draws map based on where player currently is
    if(map == -1)
        return;
    ctx.beginPath();
    ctx.strokeStyle = "white";
    ctx.fillStyle = "white";
    var o = getOffsets(myX, myY);
    for(var i = 0; i < map.length; i++) {
        var coo = map[i];
        ctx.moveTo(coo[0] + o.x, coo[1] + o.y);
        ctx.lineTo(coo[2] + o.x, coo[3] + o.y);
    }
    ctx.stroke();
    ctx.closePath();
}

/*
//This allows for the use of images instead of cirlces
img = new Image();
img.src = '/static/nobel.jpg';
img.onload = function(){
ctx.drawImage(img, 10, 10, 245, 309);
}
*/

var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
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
});
socket.on('hello', function(d) {
    console.log('server said ' + d);
});

socket.on('join', function(json) {
    console.log('server said to join');
    gameid = json.gid;
    map = json.map;
    names = json.names;
    if (state === 'QUEUEING')
        state = 'PLAYING';
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
    //console.log('got that data')
    //tempMsg('Got gamedata', 500);
    latestGameData = json;
    if(latestGameData === -1)
        location.reload(true);  // we aren't registered as a user
    //console.log(latestGameData)
});

socket.on('pong', function() {
    socket.emit('ping2', {'user': id, 'game': gameid});
});


var mouseposmatters = false;
var mousex = -1;
var mousey = -1;
sendMousePos = function() {
    var o = getOffsets(me.x, me.y);
    socket.emit("input", {user:id, event:"mousemove", x: mousex - o.x, y: mousey - o.y});  // reverse offsets to get real mouse loc
}
//http://javascript.info/tutorial/keyboard-events
canvas.addEventListener("mousedown", function(e) {
    sendMousePos();
    mouseposmatters = true;
    socket.emit("input", {user:id, event:"key", key:"Mouse1", state:true});
    // mouse1 is a key for all we care, acts the same way
});

canvas.addEventListener("mouseup", function(e) {
    mouseposmatters = false;
    socket.emit("input", {user:id, event:"key", key:"Mouse1", state:false});
});

canvas.addEventListener("mousemove", function(e) {
    mousex = e.offsetX;
    mousey = e.offsetY;
    if(mouseposmatters) {
        sendMousePos();
    }
})

//document.body.addEventListener("mousemove")

document.body.addEventListener("keydown", function(e) {
    switch (e.keyCode) {
        case 65:
            socket.emit("input", {user:id, event:"key", key:"LeftArrow", state:true});
            return false;
        case 87:
            socket.emit("input", {user:id, event:"key", key:"UpArrow", state:true});
            return false;
        case 68:
            socket.emit("input", {user:id, event:"key", key:"RightArrow", state:true});
            return false;
        case 83:
            socket.emit("input", {user:id, event:"key", key:"DownArrow", state:true});
            return false;
    }
});

document.body.addEventListener("keyup", function(e) {
    switch (e.keyCode) {
        case 65:
            socket.emit("input", {user:id, event:"key", key:"LeftArrow", state:false});
            return false;
        case 87:
            socket.emit("input", {user:id, event:"key", key:"UpArrow", state:false});
            return false;
        case 68:
            socket.emit("input", {user:id, event:"key", key:"RightArrow", state:false});
            return false;
        case 83:
            socket.emit("input", {user:id, event:"key", key:"DownArrow", state:false});
            return false;
    }
})

var framec = 0;
var mainLoop = function() {
    framec++;
    if (framec % 5 === 0) {
        socket.emit("ping", {"user": id, "game": gameid});
    }
    if (state === 'QUEUEING') {
        console.log("began queueing");
        socket.emit("givegame", {"user": id});
        ctx.font = "30px Arial";
        ctx.fillStyle = "red";
        ctx.fillText("Waiting for game...", width / 2, height / 2);
    }
    else if (state === 'PLAYING') {
        socket.emit("givedata", {"game": gameid, "user": id});
        d = latestGameData;
        if (d !== 0 && d !== 1 && d !== -1) {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            var users = d.users;
            me = users[id];
            drawMap(me.x, me.y);
            var bullets = d.bullets;
            for(var uid in users) {
                drawPlayer(me.x, me.y, users[uid].x, users[uid].y, names[uid]);
                //ctx.drawImage(img, d[i].x, d[i].y, 245, 309);
            };
            for(var i=0; i<bullets.length; i++) {
                drawBullet(me.x, me.y, bullets[i].x, bullets[i].y);
            };
        }
    }
    setTimeout(mainLoop, 15);
}
mainLoop();
