const uploadForm = document.getElementById('upload-form')
const input = document.getElementById('id_image')
console.log(input)

const alertBox = document.getElementById('alert-box')
const imageBox = document.getElementById('image-box')
const progressBox = document.getElementById('upload-progress-box')
const cancelBox = document.getElementById('cancel-box')
const cancelBtn = document.getElementById('cancel-btn')
const classification_btn = document.getElementById("classification-btn");

const csrf = document.getElementsByName('csrfmiddlewaretoken')

input.addEventListener('change', ()=>{
    classification_btn.classList.remove('not-visible')
    progressBox.classList.remove('not-visible')
    cancelBox.classList.remove('not-visible')
    uploadForm.classList.add('not-visible')

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
            console.log('before')
            alertBox.innerHTML=""
            imageBox.innerHTML=""
        },
        xhr: function(){
            const xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener('progress', e=>{
                if (e.lengthComputable) {
                    const percent = e.loaded / e.total * 100
                    console.log(percent)
                    progressBox.innerHTML = `<div class="progress" role="progressbar" aria-label="Basic example" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100">
                                                <div class="progress-bar" style="width: ${percent}%">${percent}%</div>
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
                classification_btn.classList.add('not-visible')
                uploadForm.classList.remove('not-visible')
            })
            return xhr
        },
        success: function(response){
            console.log(response)
            imageBox.innerHTML = `<img src='${url}' class="fit">`
            alertBox.innerHTML = `<div class="alert alert-success" role="alert">
                                    Image successfully upload!
                                  </div>`
        },
        error: function(error){
            console.log(error)
            alertBox.innerHTML = `<div class="alert alert-danger" role="alert">
                                    Opps, something wrong! Images must be less than 10mb.
                                  </div>`
        },
        cache: false,
        contentType: false,
        processData: false,
    })
})