socket = io.connect("/board");


socket.on("sync_match_info", function (data) {
    Object.keys(data).forEach(function (key) {
        console.log(key);
        document.getElementById(key).innerText = data[key];
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
    window.location.href = "/result";
});

socket.on("match_interrupted", function (data) {
    location.reload();
});

function start_auto_timer() {
    document.getElementById("match-period").innerText = "Auto";
    var end_time = new Date().setSeconds(new Date().getSeconds() + 15);
    var auto_timer = setInterval(function () {
        var distance = end_time - new Date();
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
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
    var end_time = new Date().setSeconds(new Date().getSeconds() + 135);
    var teloop_timer = setInterval(function () {
        var distance = end_time - new Date();
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
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