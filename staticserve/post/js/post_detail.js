$(document).ready(function(){
    $('img').addClass('img-fluid rounded');
    console.log($('#post-content').find('img'))
    console.log($('#post-content').text().length/200);
})


$(document).on('click', '.r_btn', function(ev){
    $('#reply_form').remove();
    $(`<form class="mb-2" id='reply_form'>
        <textarea id='reply_box' class="form-control-sm px-lg-4 form-control w-100 py-1" placeholder="write your reply here..."></textarea>
        <div class="text-center" id='reply_div'>
            <button onclick="reply(${ev.target.dataset['id']})" class="btn btn-sm mr-2 btn-outline-info nofocus px-4 px-lg-5 py-0" title="Add Comment"><i class="fas fa-share"></i></button>
        </div>
    </form>`).insertAfter(ev.target.parentNode);
})