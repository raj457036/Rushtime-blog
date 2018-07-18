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
  window.scrollTo(0,document.body.scrollHeight+200);
  
  // comment area security
  
  $('#comment-area').on('keydown keyup paste cut', function(){
    if (($(this).val()).length > 0) {
      $("#form-btn").removeClass('d-none');
    }
    else { $("#form-btn").addClass('d-none'); }
  })
})

function likeit(id) {
  $.ajax({
      url: '/user/post/api/like/',
      method:'GET',
      data:{'post_id':id},
      beforeSend: function(re){
        $(`#like_${id}`).html('<i class="fas fa-spin fa-spinner"></i>')
      },
      success: function(re) {
        $(`#like_${id}`).html('<i class="far fa-heart" title="Love it"></i>')
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

  $('#share_btn').click(function(){
    $('#share_panel').toggle('slide');
    $(this).toggleClass('active');
  })
  // for search api
  var obj = {
    start : `<div id="people_block"><h5>Peoples</h5><div class="list-group">`,
    middle: `</div><a href="#" class="d-block text-center">view all people</a><div id="post_block"><h5>Posts</h5><div class="list-group list-group-flush">`,
    end:`</div><a href="#" class="d-block text-center">view all</a>`
    }
    $("#search_bar").on('keydown paste change focus', function(e){

      $('#search_sync').show();
      $(document).click(function(e){
        if (e.target.nodeName != "A") {
          $('#search_sync').hide();
        } 
      })


      $.ajax({
        url: '/api/search',
        method: 'GET',
        data: {'data':$(this).val()},
        beforeSend: function() {
          $('div#search_sync').html('<i class="fas fa-spinner fa-spin d-block text-center"></i>');
        },
        success: function(result){
          let ppl = '', pst = '';
          for(let i=0;i < result.peoples.length; i++) {
            ppl += `<a href="/user/${result.peoples[i].id}" class="list-group-item list-group-item-action py-1" >
                      <div class="row" >
                          <div class="col-3 col-lg-1 p-0 text-center"><img src="${result.peoples[i].profile_pic}" alt="" class="img-fluid" style="max-height:40px;"></div>
                          <div class="col-9 col-lg-11 p-0 d-flex flex-column">
                              <small class="lead" style="font-size:16px"><b>${result.peoples[i].name}</b> (${result.peoples[i].username})</small>
                              <small>programmer with passion</small>
                          </div>
                      </div>
                  </a>`;
          }
          for(let i=0;i < result.posts.length; i++) {
            pst += `<a href="/user/post/${result.posts[i].id}" class="list-group-item list-group-item-action py-1" >
                      <div class="row" >
                          <div class="col-3 col-lg-1 p-0 text-center"><img src="${result.posts[i].img}" alt="" class="img-fluid" style="max-height:40px;"></div>
                          <div class="col-9 col-lg-11 p-0 d-flex flex-column">
                              <small class="lead" style="font-size:16px"><b>${result.posts[i].title}</b></small>
                              <small>(${result.posts[i].subtitle})</small>
                          </div>
                      </div>
                  </a>`;
          }

          if(!result.peoples) {
            ppl = '<p class="text-center" > No Result Found! </p>'
          }
          if (!result.posts) {
            pst = '<p class="text-center" > No Result Found! </p>'
          }

          $('div#search_sync').html('');
          $('div#search_sync').append(obj.start + ppl + obj.middle + pst + obj.end);
        },
        error: function(result) {
          $('div#search_sync').html('<p class="text-center" > No Result Found! </p>');
        }
      })
    });
})

// for follow api
function follow(id, csrf) {
  $.ajax({
    url: '/api/follow',
    method:'POST',
    data:{'csrfmiddlewaretoken':csrf,'user_id':id},
    success: function(result) {
      result.status ? $('#follow_btn').val('Unfollow') : $('#follow_btn').val('Follow');
      location.reload();
      console.log(result);
    },
    error: function(result) {
        console.log('connection problem!');
    }
})
}


// for bookmark api
function bookmark(id) {
  $.ajax({
    url: '/api/bookmark',
    method:'GET',
    data:{'post_id':id},
    beforeSend: function(re){
      $(`#bookmark_${id}`).html('<i class="fas fa-spin fa-spinner"></i>')
    },
    success: function(re) {
      $(`#bookmark_${id}`).html('<i class="far fa-bookmark"></i>')
      re.status ? $(`#bookmark_${id}`).addClass('active').attr('title','Remove Bookmark') : $(`#bookmark_${id}`).removeClass('active').attr('title','add Bookmark');
      console.log(re)
    },
    error: function(re) {
        console.log('connection problem!');
    }
})
}