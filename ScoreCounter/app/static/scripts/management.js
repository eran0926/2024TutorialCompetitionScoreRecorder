socket = io.connect("/management");

socket.on("connect", () => {
    console.log("Connected to server");
});

socket.on("match_end", function (msg) {
    document.querySelector(".load_btn").disabled = false;
    document.querySelector(".start_btn").disabled = false;
    document.querySelector(".stop_btn").disabled = false;
    tr = document.getElementById(msg.level + "_" + msg.id + "_tr");
    tr.dataset.state = "Ended";
    tr.querySelector(".state").innerText = "Ended";
});

Array.from(document.getElementsByClassName("load_btn")).forEach(element => {
    element.addEventListener("click", function (e) {
        act_div = this.parentElement
        act_div.parentElement.parentElement.dataset.state = "Preparing";
        act_div.parentElement.parentElement.querySelector(".state").innerText = "Preparing";
        act_div.querySelector(".load_btn").style.display = "none";
        act_div.querySelector(".start_btn").style.display = "block";
        act_div.querySelector(".stop_btn").style.display = "none";
        document.querySelector(".load_btn").disabled = true;
        document.querySelector(".start_btn").disabled = true;
        document.querySelector(".stop_btn").disabled = true;

        socket.emit("load_match", {
            level: this.parentElement.parentElement.parentElement.dataset.level,
            id: this.parentElement.parentElement.parentElement.dataset.id
        });
    });

});
Array.from(document.getElementsByClassName("start_btn")).forEach(element => {
    element.addEventListener("click", function (e) {
        act_div = this.parentElement
        act_div.parentElement.parentElement.dataset.state = "Running";
        act_div.parentElement.parentElement.querySelector(".state").innerText = "Running";
        act_div.querySelector(".load_btn").style.display = "none";
        act_div.querySelector(".start_btn").style.display = "none";
        act_div.querySelector(".stop_btn").style.display = "block";
        socket.emit("start_match", {
            level: this.parentElement.parentElement.parentElement.dataset.level,
            id: this.parentElement.parentElement.parentElement.dataset.id
        });
    });
});
Array.from(document.getElementsByClassName("stop_btn")).forEach(element => {
    element.addEventListener("click", function (e) {
        socket.emit("stop_match", {
            level: this.parentElement.parentElement.parentElement.dataset.level,
            id: this.parentElement.parentElement.parentElement.dataset.id
        });
    });
});

function set_action_btn_useable(target, load_btn, start_btn, stop_btn) {
    load_btn = load_btn ? false : true;
    target.querySelectorAll(".load_btn").forEach(element => {
        element.disabled = load_btn;
    });
    target.querySelectorAll(".start_btn").forEach(element => {
        element.disabled = start_btn;
    });
    target.querySelectorAll(".stop_btn").forEach(element => {
        element.disabled = stop_btn;
    }
    );
}

window.onload = function () {
    Array.from(document.getElementsByClassName("actions")).forEach(element => {
        state = element.parentElement.parentElement.dataset.state;
        console.log(element.parentElement.parentElement);
        console.log(state);
        if (state == "Not Started") {
            element.querySelector(".load_btn").style.display = "block";
            element.querySelector(".start_btn").style.display = "none";
            element.querySelector(".stop_btn").style.display = "none";
        } else if (state == "Preparing") {
            element.querySelector(".load_btn").style.display = "none";
            element.querySelector(".start_btn").style.display = "block";
            element.querySelector(".stop_btn").style.display = "none";
        } else if (state == "Running") {
            element.querySelector(".load_btn").style.display = "none";
            element.querySelector(".start_btn").style.display = "none";
            element.querySelector(".stop_btn").style.display = "block";
        }
        else {
            element.querySelector(".load_btn").style.display = "none";
            element.querySelector(".start_btn").style.display = "none";
            element.querySelector(".stop_btn").style.display = "none";
        }
    });
};
// $documenrt.getElementByClassName("info_tr").addEventListener("click", function() {
