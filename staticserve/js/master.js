$(function () {
    if(window.innerWidth > 992) {
      $('[data-toggle="popover"]').popover();
    }
  })

$('.popover-dismiss').popover({
  trigger: 'focus'
})

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

$("#comment-box-opener").click(function() {
  $("#comment-box").css('overflow-y','auto');
  
  $(this).remove();
  $("#form-unlock").removeClass('d-none');
  $("#form-btn").removeClass('d-none');
  window.scrollTo(0,document.body.scrollHeight+200);
})

function likeit(id) {
  $.ajax({
      url: '/user/post/api/like/',
      method:'GET',
      data:{'post_id':id},
      success: function(re) {
          re.status ? $(`#like_${id}`).addClass('active') : $(`#like_${id}`).removeClass('active');
      },
      error: function(re) {
          console.log('connection problem!');
      }
  })
}


$(document).ready(function(){
  $('#left-bar').hide();
  $('#left-toggle').click(function(){
    $('#left-bar').toggle('slide');
    $(this).toggleClass('text-warning');
  })
})