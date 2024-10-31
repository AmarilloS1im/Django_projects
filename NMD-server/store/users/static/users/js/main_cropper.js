

const ImageBox = document.getElementById('image-box')
const username_fild = document.getElementById('username_id').value
const user_first_name_fild = document.getElementById('first_name_id').value
const user_last_name_fild = document.getElementById('last_name_id').value
const user_email_fild = document.getElementById('user_email_id')
const ProfileForm = document.getElementById('profile_form')
const confirmBtn = document.getElementById('confirm-btn')
const confirmNoBtn = document.getElementById('confirm-no-btn')
const input = document.getElementById('id_file')
const csrf = document.getElementsByName('csrfmiddlewaretoken')
const btn_save = document.getElementById('btn_save')




input.addEventListener('change', ()=>{
    confirmBtn.classList.remove('not-visible')
    confirmBtn.classList.add('cropper-confirm-btn')
    confirmNoBtn.classList.remove('cropper-confirm-no-btn')
    confirmNoBtn.classList.add('not-visible')
    confirmBtn.focus()


    const img_data = input.files[0]
    const file_name = img_data['name']
    const extension = file_name.split('.').at(-1)
    const url = URL.createObjectURL(img_data)
    ImageBox.innerHTML = "<img src="+url+" id='image'>"

    var $image = $('#image');
    $image.cropper({
      aspectRatio: 1/1,

      crop: function(event) {
        console.log('script is start');
        console.log(event.detail);
        console.log(event.detail.x);
        console.log(event.detail.y);
        console.log(event.detail.width);
        console.log(event.detail.height);
        console.log(event.detail.rotate);
        console.log(event.detail.scaleX);
        console.log(event.detail.scaleY);

      }
    });
    var cropper = $image.data('cropper');

    console.log(cropper)

    confirmBtn.addEventListener('click', ()=>{



        $('#user_email_id').attr("readonly", false)
        var cropped_file_name = user_email_fild.value + '_' + 'cropped_file.'+ extension
        cropper.getCroppedCanvas({width:180, height:180}).toBlob((blob)=>{
            const fd = new FormData()
            fd.append('username',username_fild)
            fd.append('first_name',user_first_name_fild)
            fd.append('last_name',user_last_name_fild)
            fd.append('email',user_email_fild.value)
            fd.append('image',blob,cropped_file_name)
            fd.append('csrfmiddlewaretoken',csrf[0].value)

            $.ajax({
                type: 'POST',
                url: ProfileForm.action,
                enctype: 'multipart/form-data',
                data: fd,
                success: function(response){

                    console.log('done')
                },
                error: function(error){
                    console.log('not done')
                },
                cache: false,
                contentType: false,
                processData: false,
            })
            $('#user_email_id').attr("readonly", true)
            ImageBox.classList.add('not-visible')
            confirmBtn.classList.add('not-visible')




        })

    })
    btn_save.click()

})




// Get the Cropper.js instance after initialized


