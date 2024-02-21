//VARIABLES
const modal = document.getElementById("model-dialog");
const start_btn = document.getElementById("start-btn");
const close_btn = document.getElementById("close-btn");
const cancel_btn = document.getElementById("cancel-btn");

const uploadForm = document.getElementById('upload-form')
const input = document.getElementById('id_image')

const alertBox = document.getElementById('alert-box')
const imageBox = document.getElementById('image-box')

const progressBox = document.getElementById('upload-progress-box')

const classificationBox = document.getElementById('classification-box')
const classification_btn = document.getElementById("classification-btn")

const resultsBox = document.getElementById('results-box')

const cancelBox = document.getElementById('cancel-box')
const cancelBtn = document.getElementById('cancel-btn')

const csrf = document.getElementsByName('csrfmiddlewaretoken')

//MODAL WINDOW
start_btn.onclick = function() {
  modal.style.display = "block";
};
close_btn.onclick = function() {
  modal.style.display = "none";
};
cancel_btn.onclick = function() {
  modal.style.display = "none";
};
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
};

//UPLOAD FORM
input.addEventListener('change', ()=>{
    progressBox.classList.remove('not-visible')
    cancelBox.classList.remove('not-visible')
    resultsBox.classList.add('not-visible')

//    uploadForm.classList.add('not-visible')

    const img_data = input.files[0]
    const url = URL.createObjectURL(img_data)
    console.log(img_data)

    const fd = new FormData()
    fd.append('csrfmiddlewaretoken', csrf[0].value)
    fd.append('image', img_data)

    $.ajax({
        type: 'POST',
        url: uploadForm.action,
        enctype: 'multipart/form-data',
        data: fd,
        beforeSend: function(){
            alertBox.innerHTML=""
            imageBox.innerHTML=""
        },
        xhr: function(){
            const xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener('progress', e=>{
                if (e.lengthComputable) {
                    const percent = e.loaded / e.total * 100
                    console.log(percent)
                    progressBox.innerHTML = `<div
                        class="progress"
                        role="progressbar"
                        aria-label="Basic example"
                        aria-valuenow="0"
                        aria-valuemin="0"
                        aria-valuemax="100">
                        <div class="progress-bar"
                            style="width: ${percent}%">${Math.round(percent)}%
                        </div>
                    </div>`
                }
            })
            cancelBtn.addEventListener('click',()=>{
                xhr.abort()
                uploadForm.reset()
                progressBox.innerHTML = ""
                alertBox.innerHTML=""
                imageBox.innerHTML=""
                cancelBox.classList.add('not-visible')
                classificationBox.classList.add('not-visible')
                uploadForm.classList.remove('not-visible')
            })
            return xhr
        },
        success: function(response){
            classificationBox.classList.remove('not-visible')

            imageBox.innerHTML = `<img src='${url}' class="fit">`
            alertBox.innerHTML = `<div
                class="alert alert-success center"
                role="alert">Image successfully upload!
            </div>`
        },
        error: function(error){
            classificationBox.classList.add('not-visible')

            console.log(error)
            alertBox.innerHTML = `<div
                class="alert alert-danger center"
                role="alert">Opps, something wrong!
            </div>`
        },
        cache: false,
        contentType: false,
        processData: false,
    })
});

//CLASSIFICATION RESULTS
$(document).on('click', '.alink', function () {
    var url = $("#classification-btn").attr("data-url")
    console.log('classification button activated!')

    $.ajax({
        url: url,
        data: "json",
        success : function(results) {
            resultsBox.classList.remove('not-visible')

            results = JSON.stringify(results)
            results = JSON.parse(results)
            document.getElementById("first").innerHTML = results.first
            console.log(results.first)
            document.getElementById("second").innerHTML = results.second
            console.log(results.second)
            document.getElementById("third").innerHTML = results.third
            console.log(results.third)
        },
        error: function(error){
            console.log(error)
        },
    })
});