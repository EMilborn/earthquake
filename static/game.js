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
var width = canvas.width;
var height = canvas.height;
var queuebutton = document.getElementById("queuebutton");
queuebutton.addEventListener("click", function(e) {
    state = 'QUEUEING';
    queuebutton.style.display = 'none'
})

drawCircle = function(x, y, r, col) {
    ctx.beginPath();
    ctx.arc(x, y, r, 0, 2*Math.PI);
    ctx.fillStyle = col;
    ctx.fill();
    ctx.stroke();
    ctx.closePath();
}

drawPlayer = function(x, y) {
    drawCircle(x, y, 25, "red");
}

drawBullet = function(x, y) {
    drawCircle(x, y, 5, "blue");
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

socket.on('join', function(gid) {
    console.log('server said to join');
    gameid = gid;
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
    socket.emit("input", {user:id, event:"mousemove", x: mousex, y: mousey})
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
    mousex = e.pageX;
    mousey = e.pageY;
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
        ctx.fillStyle = "black";
        ctx.textAlign = "center";
        ctx.fillText("Waiting for game...", width / 2, height / 2);
    }
    else if (state === 'PLAYING') {
        socket.emit("givedata", {"game": gameid, "user": id});
        d = latestGameData;
        if (d !== 0 && d !== 1 && d !== -1) {
            users = d.users;
            bullets = d.bullets;
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            for(var i=0; i<users.length; i++) {
                drawPlayer(users[i].x, users[i].y);
                //ctx.drawImage(img, d[i].x, d[i].y, 245, 309);
            };
            for(var i=0; i<bullets.length; i++) {
                drawBullet(bullets[i].x, bullets[i].y);
            };
        }
    }
    setTimeout(mainLoop, 15);
}
mainLoop();
