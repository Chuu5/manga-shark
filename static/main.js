const fileInput = document.getElementById('banner');
let bannerImage = document.getElementById("home-banner")
let someText = document.getElementById("some-text")

fileInput.addEventListener('change', (e) => {
    // creating a url from the image input
    let file = e.target.files[0];
    let reader = new FileReader()

    reader.onloadend = function () {
        someText.value = reader.result
    }

    if (file) {
        reader.readAsDataURL(file);
    } else {
        bannerImage.src = "";
    }
    

    url = URL.createObjectURL(e.target.files[0])
    bannerImage.src = url
    bannerImage.style.display = "block"
})