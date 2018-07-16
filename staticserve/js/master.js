$(function () {
    if(window.innerWidth > 992) {
      $('[data-toggle="popover"]').popover();
    }
  })

$('.popover-dismiss').popover({
  trigger: 'focus'
})