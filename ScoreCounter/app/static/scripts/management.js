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
    set_action_btn_visible(tr.querySelector(".actions"), false, false, false, true);
});

socket.on("match_interrupted", function (msg) {
    // document.querySelector(".load_btn").disabled = false;
    // document.querySelector(".start_btn").disabled = false;
    // document.querySelector(".stop_btn").disabled = false;
    tr = document.getElementById(msg.level + "_" + msg.id + "_tr");
    tr.dataset.state = "Interrupted";
    tr.querySelector(".state").innerText = "Interrupted";
    set_action_btn_visible(tr.querySelector(".actions"), true, false, false);
});

socket.on("all_commited", function (msg) {
    tr = document.getElementById(msg.level + "_" + msg.id + "_tr");
    tr.dataset.state = "All Commited";
    tr.dataset.state = "All Commited";
    tr.querySelector(".state").innerText = "All Commited";
    tr.querySelector(".save_btn").classList.remove("btn-danger");
    tr.querySelector(".save_btn").classList.add("btn-success");
    set_action_btn_visible(tr.querySelector(".actions"), false, false, false, true);
});

Array.from(document.getElementsByClassName("load_btn")).forEach(element => {
    element.addEventListener("click", function (e) {
        document.querySelectorAll(".info_tr").forEach(tr => {
            act_div = tr.querySelector(".actions");
            if (act_div != this.parentElement) {
                if (act_div.parentElement.parentElement.dataset.state == "Preparing") {
                    set_action_btn_visible(act_div, true, false, false);
                    act_div.parentElement.parentElement.dataset.state = "Not Started";
                    act_div.parentElement.parentElement.querySelector(".state").innerText = "Not Started";
                }
            } else {
                set_action_btn_visible(act_div, false, true, false);
                act_div.parentElement.parentElement.dataset.state = "Preparing";
                act_div.parentElement.parentElement.querySelector(".state").innerText = "Preparing";
            }
        });
        act_div = this.parentElement
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
        act_div = this.parentElement
        set_action_btn_visible(act_div, false, false, true);
        act_div.parentElement.parentElement.dataset.state = "Running";
        act_div.parentElement.parentElement.querySelector(".state").innerText = "Running";
        // act_div.querySelector(".load_btn").style.display = "none";
        // act_div.querySelector(".start_btn").style.display = "none";
        // act_div.querySelector(".stop_btn").style.display = "block";
        console.log("Start Match");
        socket.emit("start_match", {
            level: this.parentElement.parentElement.parentElement.dataset.level,
            id: this.parentElement.parentElement.parentElement.dataset.id
        });

    });
});
Array.from(document.getElementsByClassName("stop_btn")).forEach(element => {
    element.addEventListener("click", function (e) {
        socket.emit("interrupt_match", {
            level: this.parentElement.parentElement.parentElement.dataset.level,
            id: this.parentElement.parentElement.parentElement.dataset.id
        });
    });
});

Array.from(document.getElementsByClassName("save_btn")).forEach(element => {
    element.addEventListener("click", function (e) {
        act_div = this.parentElement
        set_action_btn_visible(act_div, false, false, false);
        act_div.parentElement.parentElement.dataset.state = "Saved";
        act_div.parentElement.parentElement.querySelector(".state").innerText = "Saved";
        socket.emit("save_and_show", {
            level: this.parentElement.parentElement.parentElement.dataset.level,
            id: this.parentElement.parentElement.parentElement.dataset.id
        });
    });
});

function set_action_btn_disabled(target, load_btn, start_btn, stop_btn, save_btn) {
    target.querySelectorAll(".load_btn").forEach(element => {
        element.disabled = load_btn;
    });
    target.querySelectorAll(".start_btn").forEach(element => {
        element.disabled = start_btn;
    });
    target.querySelectorAll(".stop_btn").forEach(element => {
        element.disabled = stop_btn;
    });
    target.querySelectorAll(".save_btn").forEach(element => {
        element.disabled = save_btn;
    });
}

function set_action_btn_visible(target, load_btn, start_btn, stop_btn, save_btn = false) {
    load_btn = load_btn ? "block" : "none";
    start_btn = start_btn ? "block" : "none";
    stop_btn = stop_btn ? "block" : "none";
    save_btn = save_btn ? "block" : "none";
    target.querySelectorAll(".load_btn").forEach(element => {
        element.style.display = load_btn;
    });
    target.querySelectorAll(".start_btn").forEach(element => {
        element.style.display = start_btn;
    });
    target.querySelectorAll(".stop_btn").forEach(element => {
        element.style.display = stop_btn;
    });
    target.querySelectorAll(".save_btn").forEach(element => {
        element.style.display = save_btn;
    });
}

window.onload = function () {
    Array.from(document.getElementsByClassName("actions")).forEach(element => {
        state = element.parentElement.parentElement.dataset.state;
        if (state == "Not Started" || state == "Interrupted") {
            set_action_btn_visible(element, true, false, false);
        } else if (state == "Preparing") {
            set_action_btn_visible(element, false, true, false);
        } else if (state == "Running") {
            set_action_btn_visible(element, false, false, true);
        } else if (state == "Ended") {
            set_action_btn_visible(element, false, false, false, true);
            save_btn = document.querySelector(".save_btn");
            save_btn.classList.remove("btn-success");
            save_btn.classList.add("btn-danger");
        } else if (state == "All Commited") {
            set_action_btn_visible(element, false, false, false, true);
            save_btn = document.querySelector(".save_btn");
            save_btn.classList.remove("btn-danger");
            save_btn.classList.add("btn-success");
        } else {
            set_action_btn_visible(element, false, false, false);
        }
    });
};
// $documenrt.getElementByClassName("info_tr").addEventListener("click", function() {
