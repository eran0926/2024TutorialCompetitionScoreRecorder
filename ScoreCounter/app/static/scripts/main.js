document.addEventListener("touchstart", startTouch, false);
document.addEventListener("touchend", moveTouch, false);

var initialX = null;
var xThreshold = 0.3;
var slide = 0;
var config = {
    "decrease-leave": "manual",
};
var gameStatus = "stop";

function swipePage(increment) {
    previousSlide = slide;
    slides = document.getElementById("main-holder").children;
    if (slide + increment < slides.length && slide + increment >= 0) {
        slides[slide].style.display = "none";
        slide += increment;
        window.scrollTo(0, 0);
        slides[slide].style.display = "table";
        // document.getElementById('data').innerHTML = "";
        // document.getElementById('copyButton').setAttribute('value', 'Copy Data');
    }
}

function startTouch(e) {
    initialX = e.touches[0].screenX;
}

function moveTouch(e) {
    if (initialX === null) {
        return;
    }

    var currentX = e.changedTouches[0].screenX;
    var diffX = initialX - currentX;

    // sliding horizontally
    if (diffX / screen.width > xThreshold) {
        // swiped left
        if (slide != 0) {
            swipePage(1);
        }
    } else if (diffX / screen.width < -xThreshold) {
        // swiped right
        swipePage(-1);
    }
    initialX = null;
}

// document.getElementById("auto-leave-select").addEventListener("click", function (e) {
//     console.log(e);
//     console.log(" ddefef");
//     Array.from(document.getElementById("auto-leave-select").children).forEach(function (element) {
//         if (element == e.target) {
//             element.classList.remove("btn-secondary");
//             element.classList.add("btn-info");
//             document.getElementById("auto-leave-select").value = element.value;
//             console.log(element);
//         }
//         else {
//             element.classList.remove("btn-info");
//             element.classList.add("btn-secondary");
//         };
//     });
// });

function update_score(elementId, score) {
    const cooectionId = socket.id;
    socket.emit("update_score", {
        from: cooectionId,
        data: [
            {
                id: elementId,
                score: score
            }
        ]
    });
}

function update_selection(elementId, choice) {
    const cooectionId = socket.id;
    socket.emit("update_selection", {
        from: cooectionId,
        data: [
            {
                id: elementId,
                choice: choice
            }
        ]
    });
}

function setEventListener() {
    allStage = document.getElementById("main-holder").children;
    for (let i = 1; i < allStage.length; i++) {
        allStage[i].style.display = "none";
    }


    document.querySelectorAll(".select-btn-group").forEach(function (btn_group) {
        btn_group.addEventListener("click", function (e) {
            Array.from(btn_group.children).forEach(function (child) {
                if (child == e.target) {
                    child.classList.remove("btn-secondary");
                    child.classList.add("btn-info");
                    btn_group.value = child.value;
                    update_selection(btn_group.id, btn_group.value);
                    // config[element.parentElement.id] = element.value;
                } else {
                    child.classList.remove("btn-info");
                    child.classList.add("btn-secondary");
                }
            });
        });
    });

    for (let i = 0; i < allStage.length; i++) {
        allStage[i].querySelectorAll(".count-btn").forEach(function (element) {
            element.addEventListener("click", function (e) {
                console.log(this);
                score_div = this.querySelector(".score-div");
                if (
                    !this.parentElement.parentElement
                        .querySelector("#decrease-btn")
                        .classList.contains("active")
                ) {
                    score_div.innerText = parseInt(score_div.innerText) + 1;
                    update_score(this.id, score_div.innerText);
                } else {
                    if (parseInt(score_div.innerText) > 0) {
                        score_div.innerText = parseInt(score_div.innerText) - 1;
                        update_score(this.id, score_div.innerText);
                    }
                    if (config["decrease-leave"] == "auto") {
                        this.parentElement.parentElement
                            .querySelector("#decrease-btn")
                            .classList.toggle("active");
                        this.parentElement.parentElement.querySelector(
                            "#decrease-btn"
                        ).innerText = "Decrease";
                    }
                }
            });
        });


        allStage[i].querySelectorAll("#decrease-btn").forEach(function (element) {
            console.log(element);
            element.addEventListener("click", function (e) {
                this.classList.toggle("active");
                if (this.classList.contains("active")) {
                    this.innerText = "Increase";
                } else {
                    this.innerText = "Decrease";
                }
            });
        });

    }

}

function start() {
    if (gameStatus == "started") {
        document.getElementById("start-btn").disabled = false;

        // swipePage(1);
    }
}

function setSocket() {
    socket = io.connect();

    socket.on("connect", () => {
        console.log("connected");
        Array.from(document.getElementsByClassName("connection-status")).forEach(
            function (element) {
                element.classList.remove("danger");
                element.innerText = "Connected";
                element.classList.add("success");
            }
        );
    });

    socket.on("disconnect", () => {
        Array.from(document.getElementsByClassName("connection-status")).forEach(
            function (element) {
                element.classList.remove("success");
                element.innerText = "Disconnected";
                element.classList.add("danger");
            }
        );
    });

    socket.on("sync_game_status", function (msg) {
        gameStatus = msg.matchStatus;
        console.log(gameStatus);
        if (gameStatus != "started") {
            console.log(gameStatus);
            document.getElementById("start-btn").disabled = true;
        } else {
            document.getElementById("start-btn").disabled = false;
        }
        Array.from(document.getElementById("level-select").children).forEach(
            function (element) {
                if (element.value == msg.matchLevel) {
                    element.classList.remove("btn-secondary");
                    element.classList.add("btn-info");
                } else {
                    element.classList.remove("btn-info");
                    element.classList.add("btn-secondary");
                }
            }
        );

        document.getElementById("matchNumberInput").value = msg.matchNumber;

        Array.from(document.getElementById("alliance-select").children).forEach(
            function (element) {
                if (element.value == msg.alliance) {
                    element.classList.remove("btn-secondary");
                    element.classList.add("btn-info");
                } else {
                    element.classList.remove("btn-info");
                    element.classList.add("btn-secondary");
                }
            }
        );

        Array.from(document.getElementsByClassName("tean-number1")).forEach(
            function (element) {
                element.innerText = msg.team1;
            }
        );
        Array.from(document.getElementsByClassName("tean-number2")).forEach(
            function (element) {
                element.innerText = msg.team2;
            }
        );
    });

    socket.on("gaem_start", function (msg) {
        gameStatus = "started";
        swipePage(1);
    });
    socket.on("game_stop", function (msg) {
        gameStatus = "finished";
        window.location.reload();
    });

    socket.on("update_score", function (msg) {
        console.log(msg);
        if (msg.from == socket.id) {
            return;
        }
        msg.data.forEach(function (element) {
            document.getElementById(element.id).querySelector(".score-div").innerText = element.score;
        })
    });

    socket.on("update_selection", function (msg) {
        console.log(msg);
        if (msg.from == socket.id) {
            return;
        }
        msg.data.forEach(function (element) {
            Array.from(document.getElementById(element.id).children).forEach(function (child) {
                if (child.value == element.choice) {
                    child.classList.remove("btn-secondary");
                    child.classList.add("btn-info");
                } else {
                    child.classList.remove("btn-info");
                    child.classList.add("btn-secondary");
                }
            });
        });
    });
}

// function syncGameStatus(msg) { }

function init() {
    console.log("init");
    setEventListener();
    setSocket();
}

window.onload = init();
