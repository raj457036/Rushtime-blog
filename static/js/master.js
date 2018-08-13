window.addEventListener( "pageshow", function ( event ) {
  var historyTraversal = event.persisted || 
                         ( typeof window.performance != "undefined" && 
                              window.performance.navigation.type === 2 );
  if ( historyTraversal ) {
    // Handle page restore.
    window.location.reload();
  }
});

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
  $('[data-toggle="popover"]').popover();
})

// like api
function likeit(id) {
  $.ajax({
      url: '/user/post/api/like/',
      method:'GET',
      data:{'post_id':id},
      beforeSend: function(re){
        $(`#like_${id}`).html('<i class="fas fa-spin fa-spinner"></i>')
      },
      success: function(re) {
        $(`#like_${id}`).html(`<i class="far fa-heart" title="Love it"></i> ${re.likes>0 ? re.likes : ''} `)
        re.status ? $(`#like_${id}`).addClass('active') : $(`#like_${id}`).removeClass('active');
      },
      error: function(re) {
          console.log('connection problem!');
      }
  })
}

function showShare(id) {
  $(`${id} div[data-network="sharethis"]`).click();
}

function get_template(name, since,about, img_url, top_stories, followers_num) {
  let date = new Date(since)
  date = date.toDateString().split(' ')
  
  let temp1 = `<div class="card border-0">
                <div class="card-body p-2">
                    <div class="row no-gutters">
                        <div class="col-8">
                            <h6 class="card-title font-weight-bold">${name}</h6>
                            <h6 class="card-subtitle mb-2 text-info text-sm">Member since ${date[1]+" "+date[3]}</h6>
                            <h6 class="card-subtitle mb-2 text-xs text-muted">${about}</h6>
                        </div>
                        <div class="col-4 p-0">
                            <img src="${img_url}" class="pop-img img-fluid rounded-circle float-right border-info border-top border-bottom" style="width:60px;height:60px;" alt="" srcset="">
                        </div>
                    </div>`
                    
  let list ='';                
  if (top_stories.length > 0) {
    list = `<div class="dropdown-divider"></div>
    <p class="card-text text-sm text-muted m-0 lead" style="font-size:16px;">Top Stories</p>
    <ol class="text-sm pl-3 mt-0 text-muted">`
    for(let i of top_stories) {
      list+=`<li><a class="text-dark hover-line" href='/user/post/${i[0]}'>${i[1].slice(0,40)}</a></li>`
    }       
    list+='</ol>' 
  }             
  let temp3 = `<div class="dropdown-divider"></div>
                <p class="text-info mb-0 text-center font-weight-bold">Followed by ${followers_num} people</p></div></div>`       

  return temp1+list+temp3;
}

$(document).ready(function(){
  $('#left-toggle').click(function(){
    $('#left-bar').toggle('fast','linear');
    if (window.innerWidth < 400) {$(".navbar-toggler").toggle();}
  });
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

function pop(e) {
  $('[data-user]').not(this).popover('hide');
  $('.container-fluid, .container').click(function(ev){$('#'+e.id).popover('hide')});
  let obj;
  $.ajax({
    url:'/api/userdetail',
    method:'GET',
    data:{'username':$('#'+e.id).attr('data-user')},
    success: function(re) {
      console.log(re)
      obj = { 
        html:true,
        content: get_template(re.name, re.joined, re.about, re.profile_pic, re["top-posts"], re.followers),
        placement:'bottom',
        trigger:'focus',
        // title:'hurr hurr dabang dabang',
        template:`<div class="popover" role="tooltip">
                    <div class="arrow"></div>
                    <h3 class="popover-header"></h3>
                    <div class="popover-body"></div>
                  </div>`
        }
        $('#'+e.id).popover(obj);
      $('#'+e.id).popover('show');
    },
    error: function(re) {
      console.log('Connection Problem');
    }
  });
}

// for follow api
function follow(id, csrf) {
  $.ajax({
    url: '/api/follow',
    method:'POST',
    data:{'csrfmiddlewaretoken':csrf,'user_id':id},
    success: function(re) {
      re.status ? $('#follow_btn').val('Unfollow') : $('#follow_btn').val('Follow');
      location.reload();
    },
    error: function(re) {
        console.log('connection problem!');
    }
})
}

// for bookmark api
function bookmark(id,status) {
  $.ajax({
    url: '/api/bookmark',
    method:'GET',
    data:{'post_id':id},
    beforeSend: function(re){
      $(`#bookmark_${id}`).html('<i class="fas fa-spin fa-spinner"></i>')
    },
    success: function(re) {
      re.status ? $(`#bookmark_${id}`).html('<i class="fas fa-bookmark"></i>').attr('title','Remove Bookmark') : $(`#bookmark_${id}`).html('<i class="far fa-bookmark"></i>').attr('title','add Bookmark');
      if(status) {location.reload();}
    },
    error: function(re) {
        console.log('connection problem!');
    }
})
}

// for draft api
function draft(id, csrf) {
  $.ajax({
    url: '/api/draft',
    method:'POST',
    data:{'csrfmiddlewaretoken':csrf, 'post_id':id},
    beforeSend: function(re){
      $(`#draft_${id}`).html('<i class="fas fa-spin fa-spinner"></i>')
    },
    success: function(re) {
      $(`#draft_${id}`).html('')
      re.status ? $(`#draft_${id}`).html('<i class="fas fa-lock"></i> Draft') : $(`#draft_${id}`).html('<i class="fas fa-unlock"></i> Live');
    },
    error: function(re) {
        console.log('connection problem!');
    }
})
}

// reply api
function reply(id) {
  r = $("#reply_box").val();
  $.ajax({
    url:'/api/reply',
    method:"POST",
    data: {'reply':r, 'comment_id':id},
    success:function(re) {
      $(re).insertAfter('#reply_form');
      $('#reply_form').remove();
    },
    error: function() {
      console.log('problem')
    }
  })
  
}

// comment api
function comment(id) {
  c = $("#comment-area").val();
  console.log(c)
  $.ajax({
    url:'/api/comment',
    method:"POST",
    data: {'comment':c, 'post':id},
    success:function(re) {
      if (typeof(re)=='string') {
        $('#comments_container').prepend(re);
      }
      else {
        alert('There is some problem. we are checking...')
      }
      
    },
    error: function() {
      console.log('problem')
    }
  })
  $("#comment-area").val('');
}


// remove comment api
function remove_comment(id) {
  $.ajax({
    url:'/api/comment_remove',
    method:'POST',
    data:{'id':id},
    success: function(re){
      if (re.status==true) {
        $('#c_'+id).remove();
      }
    },
  })
}

// remove reply api
function remove_reply(id) {
  $.ajax({
    url:'/api/reply_remove',
    method:'POST',
    data:{'id':id},
    success: function(re){
      console.log(re)
      if (re.status==true) {
        $('#r_'+id).remove();
      }
    },
    error:function(){
      console.log('problem')
    }
  })
}