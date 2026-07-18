const imageInput = document.getElementById("imageInput");
const preview = document.getElementById("preview");

imageInput.onchange = function () {

    const file = imageInput.files[0];

    if(file){

        preview.src = URL.createObjectURL(file);

    }

};