function changeImage() {
    if (document.getElementById("water-drop").getAttribute("src") == "/static/images/water-drop-empty.svg") {
        document.getElementById("water-drop").src = "/static/images/water-drop-full.svg";
    } else {
        document.getElementById("water-drop").src = "/static/images/water-drop-empty.svg";
    }
    fetch('/switchPumping').then((response) => {
        console.log(response);
    });
}