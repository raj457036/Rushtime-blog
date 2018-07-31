function avatar_filler(gender, counter) {
    let i = 0;
    let htm = ''
    for (i = 1; i <= counter; i++) {
        htm += `<div class="d-inline-block avatars" style="max-width:90px; cursor:pointer" >
    <img class='img-fluid' src="/static/registration/Avatars/${gender}/${gender[0]}(${i}).svg" data-avatar='${i}'>
    </div>`
    }

    return htm;
}

$('#modal-container').append(avatar_filler('male', 14));
$(document).on('change', '#id_gender',function () {
    $('#modal-container').html('');
    switch ($(this).val()) {
        case 'm':
            $('#modal-container').append(avatar_filler('male', 14));
            break;
        case 'f':
            $('#modal-container').append(avatar_filler('female', 9));
            break;
    }
})

$(document).on('click', '.avatars',function (ev) {
    $('.avatars').addClass('avatar_notactive');
    $('#id_avatar_number').val(ev.target.dataset.avatar);
    $('#id_display_img').val('');
    $(this).removeClass('avatar_notactive');
})

$(document).on('change','#id_display_img', function () {
    $('.avatars').removeClass('avatar_notactive');
    $('#id_avatar_number').val(-1);
})