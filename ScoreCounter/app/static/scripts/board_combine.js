socket = io.connect("/board");


socket.on("sync_match_info", function (data) {
    setPage("board");
    Object.keys(data).forEach(function (key) {
        Array.from(document.getElementsByClassName(key)).forEach(function (element) {
            element.innerText = data[key];
        });
        // console.log(key);
        // document.getElementById(key).innerText = data[key];
    });
});

socket.on("update_value", function (data) {
    data["data"].forEach(function (element) {
        console.log(element);
        document.getElementById(element.id).innerText = element.value;
    });
});


socket.on("match_start", function (data) {
    document.getElementById("timer-min").innerText = "00";
    document.getElementById("timer-sec").innerText = "00";
    start_auto_timer();
})

socket.on("show_result", function (data) {
    console.log(data);
    dict_style_data = {}
    data.forEach(function (element) {
        dict_style_data[element.id] = element.value;
    });
    console.log(dict_style_data);
    document.getElementById("red-total-score").innerText = dict_style_data["red-total-score-with-penalty"];
    document.getElementById("blue-total-score").innerText = dict_style_data["blue-total-score-with-penalty"];
    if (dict_style_data["winner"] == "red") {
        document.getElementById("red-win").innerText = "WIN";
        document.getElementById("blue-win").innerText = "LOSE";
        document.getElementById("red-win-rp1").style.display = "block";
        document.getElementById("red-win-rp2").style.display = "block";
        document.getElementById("blue-win-rp1").style.display = "none";
        document.getElementById("blue-win-rp2").style.display = "none";
    } else if (dict_style_data["winner"] == "blue") {
        document.getElementById("red-win").innerText = "LOSE";
        document.getElementById("blue-win").innerText = "WIN";
        document.getElementById("red-win-rp1").style.display = "none";
        document.getElementById("red-win-rp2").style.display = "none";
        document.getElementById("blue-win-rp1").style.display = "block";
        document.getElementById("blue-win-rp2").style.display = "block";
    }
    else if (dict_style_data["winner"] == "tie") {
        document.getElementById("red-win").innerText = "TIE";
        document.getElementById("blue-win").innerText = "TIE";
        document.getElementById("red-win-rp1").style.display = "block";
        document.getElementById("red-win-rp2").style.display = "none";
        document.getElementById("blue-win-rp1").style.display = "block";
        document.getElementById("blue-win-rp2").style.display = "none";
    }

    document.getElementById("red-melody").style.display = dict_style_data["red-melody"] ? "block" : "none";
    document.getElementById("blue-melody").style.display = dict_style_data["blue-melody"] ? "block" : "none";
    document.getElementById("red-ensemble").style.display = dict_style_data["red-ensemble"] ? "block" : "none";
    document.getElementById("blue-ensemble").style.display = dict_style_data["blue-ensemble"] ? "block" : "none";
    setPage("result");
});
socket.on("match_interrupted", function (data) {
    location.reload();
});

function start_auto_timer() {
    document.getElementById("match-period").innerText = "Auto";
    var end_time = new Date().setSeconds(new Date().getSeconds() + 15);
    var auto_timer = setInterval(function () {
        var distance = end_time - new Date();
        var seconds = Math.floor((distance % (1000 * 60)) / 1000).toString().padStart(2, "0");
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60)).toString().padStart(2, "0");
        document.getElementById("timer-min").innerText = minutes;
        document.getElementById("timer-sec").innerText = seconds;

        if (distance <= 0) {
            clearInterval(auto_timer);
            setTimeout(start_teloop_timer, 1000);
            document.getElementById("timer-min").innerText = "00";
            document.getElementById("timer-sec").innerText = "00";
            document.getElementById("match-period").innerText = "Teleop";
        }
    });

}
function start_teloop_timer() {
    // var end_time = new Date().setSeconds(new Date().getSeconds() + 135);
    var end_time = new Date().setSeconds(new Date().getSeconds() + 5);
    var teloop_timer = setInterval(function () {
        var distance = end_time - new Date();
        var seconds = Math.floor((distance % (1000 * 60)) / 1000).toString().padStart(2, "0");
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60)).toString().padStart(2, "0");
        document.getElementById("timer-min").innerText = minutes;
        document.getElementById("timer-sec").innerText = seconds;

        if (distance <= 0) {
            clearInterval(teloop_timer);
            document.getElementById("timer-min").innerText = "00";
            document.getElementById("timer-sec").innerText = "00";
            // setTimeout(start_auto_timer, 1000);
        }
    }, 1000);
}

function setPage(page) {
    if (page == "board") {
        document.getElementById("board-div").style.display = "block";
        document.getElementById("result-div").style.display = "none";
    }
    else if (page == "result") {
        document.getElementById("board-div").style.display = "none";
        document.getElementById("result-div").style.display = "block";
    }

}

window.onload = function () {
    setPage("board");
}