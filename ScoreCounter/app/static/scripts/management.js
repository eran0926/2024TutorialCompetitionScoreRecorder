socket = io.connect("/management");

socket.on("connect", () => {
    console.log("Connected to server");
});

socket.on("match_end", function (msg) {
    // document.querySelector(".load_btn").disabled = false;
    // document.querySelector(".start_btn").disabled = false;
    // document.querySelector(".stop_btn").disabled = false;
    tr = document.getElementById(msg.level + "_" + msg.id + "_tr");
    tr.dataset.state = "Ended";
    tr.querySelector(".state").innerText = "Ended";
    set_action_btn_visible(tr.querySelector(".actions"), false, false, false);
});

Array.from(document.getElementsByClassName("load_btn")).forEach(element => {
    element.addEventListener("click", function (e) {
        act_div = this.parentElement
        set_action_btn_visible(act_div, false, true, false);
        act_div.parentElement.parentElement.dataset.state = "Preparing";
        act_div.parentElement.parentElement.querySelector(".state").innerText = "Preparing";
        // act_div.querySelector(".load_btn").style.display = "none";
        // act_div.querySelector(".start_btn").style.display = "block";
        // act_div.querySelector(".stop_btn").style.display = "none";
        // document.querySelector(".load_btn").disabled = true;
        // document.querySelector(".start_btn").disabled = true;
        // document.querySelector(".stop_btn").disabled = true;

        socket.emit("load_match", {
            level: this.parentElement.parentElement.parentElement.dataset.level,
            id: this.parentElement.parentElement.parentElement.dataset.id
        });
    });

});
Array.from(document.getElementsByClassName("start_btn")).forEach(element => {
    element.addEventListener("click", function (e) {
        set_action_btn_visible(act_div, false, false, true);
        act_div = this.parentElement
        act_div.parentElement.parentElement.dataset.state = "Running";
        act_div.parentElement.parentElement.querySelector(".state").innerText = "Running";
        // act_div.querySelector(".load_btn").style.display = "none";
        // act_div.querySelector(".start_btn").style.display = "none";
        // act_div.querySelector(".stop_btn").style.display = "block";
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

function set_action_btn_disabled(target, load_btn, start_btn, stop_btn) {
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

function set_action_btn_visible(target, load_btn, start_btn, stop_btn) {
    load_btn = load_btn ? "block" : "none";
    start_btn = start_btn ? "block" : "none";
    stop_btn = stop_btn ? "block" : "none";
    target.querySelectorAll(".load_btn").forEach(element => {
        element.style.display = load_btn;
    });
    target.querySelectorAll(".start_btn").forEach(element => {
        element.style.display = start_btn;
    });
    target.querySelectorAll(".stop_btn").forEach(element => {
        element.style.display = stop_btn;
    }
    );
}

window.onload = function () {
    Array.from(document.getElementsByClassName("actions")).forEach(element => {
        state = element.parentElement.parentElement.dataset.state;
        console.log(element.parentElement.parentElement);
        console.log(state);
        if (state == "Not Started") {
            set_action_btn_visible(element, true, false, false);
        } else if (state == "Preparing") {
            set_action_btn_visible(element, false, false, false);
            // element.querySelector(".load_btn").style.display = "none";
            // element.querySelector(".start_btn").style.display = "block";
            // element.querySelector(".stop_btn").style.display = "none";
        } else if (state == "Running") {
            set_action_btn_visible(element, false, false, true);
            // element.querySelector(".load_btn").style.display = "none";
            // element.querySelector(".start_btn").style.display = "none";
            // element.querySelector(".stop_btn").style.display = "block";
        }
        else {
            element.set_action_btn_visible(element, false, false, false);
            // element.querySelector(".load_btn").style.display = "none";
            // element.querySelector(".start_btn").style.display = "none";
            // element.querySelector(".stop_btn").style.display = "none";
        }
    });
};
// $documenrt.getElementByClassName("info_tr").addEventListener("click", function() {
