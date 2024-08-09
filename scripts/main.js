var slide = 0;
function swipePage(increment) {
    previousSlide = slide
    slides = document.getElementById("main-holder").children
    if (slide + increment < slides.length && slide + increment >= 0) {
        slides[slide].style.display = "none";
        slide += increment;
        window.scrollTo(0, 0);
        slides[slide].style.display = "table";
        // document.getElementById('data').innerHTML = "";
        // document.getElementById('copyButton').setAttribute('value', 'Copy Data');

    }
}
document.getElementById("auto-leave-select").addEventListener("click", function (e) {
    console.log(e);
    console.log(" ddefef");
    Array.from(document.getElementById("auto-leave-select").children).forEach(function (element) {
        if (element == e.target) {
            element.classList.remove("btn-secondary");
            element.classList.add("btn-info");
            document.getElementById("auto-leave-select").value = element.value;
            console.log(element);
        }
        else {
            element.classList.remove("btn-info");
            element.classList.add("btn-secondary");
        };
    });
});

init = function () {

    allStage = document.getElementById("main-holder").children;
    for (let i = 1; i < allStage.length; i++) {
        allStage[i].style.display = "none";
    }
    for (let i = 0; i < allStage.length; i++) {
        allStage[i].querySelectorAll(".count-btn").forEach(function (element) {
            element.addEventListener("click", function (e) {
                console.log(this)
                score_div = this.querySelector(".score-div");
                if (!this.parentElement.parentElement.querySelector("#decrease-btn").classList.contains("active")) {
                    score_div.innerText = parseInt(score_div.innerText) + 1;
                }
                else {
                    score_div.innerText = parseInt(score_div.innerText) - 1;
                    this.parentElement.parentElement.querySelector("#decrease-btn").classList.toggle("active");
                    this.parentElement.parentElement.querySelector("#decrease-btn").innerText = "Decrease";
                }
            });
        });
        allStage[i].querySelectorAll("#decrease-btn").forEach(function (element) {
            console.log(element)
            element.addEventListener("click", function (e) {
                this.classList.toggle("active");
                if (this.classList.contains("active")) {
                    this.innerText = "Increase";
                }
                else {
                    this.innerText = "Decrease";
                }
            });
        });
    }
}


window.onload = init()