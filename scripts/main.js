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
    // e.classList.add("btn-info");
    // e.classList.remove("btn-secondary");
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
        // swipePage(1);
    });
});

