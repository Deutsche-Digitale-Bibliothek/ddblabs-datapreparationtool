function toggleElementVisibility(_elementId) {
    var toggle_elements = document.getElementById(_elementId);

    if (toggle_elements.style.display === "none") {
        toggle_elements.style.display = "block";
    } else {
        toggle_elements.style.display = "none";
    }
}

function toggleMultipleElementVisibility(_elementName) {
    var toggle_elements = document.querySelectorAll(_elementName);

    for (var i = 0; i < toggle_elements.length; i++) {
        if (toggle_elements[i].style.display === "none") {
            toggle_elements[i].style.display = "block";
        } else {
            toggle_elements[i].style.display = "none";
        }
    }
}
