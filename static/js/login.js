$('.toggle-register').click(function(){
  $(this).addClass('active');
  $('.toggle-login').removeClass('active');
  $('.login-body').slideUp("slow");
  $('.register-body').delay(625).slideDown("slow");
});

$('.toggle-login').click(function(){
  $(this).addClass('active');
  $('.toggle-register').removeClass('active');
  $('.register-body').slideUp("slow");
  $('.login-body').delay(625).slideDown("slow");
});

$('#registered').click(function(){
  $('.toggle-login').click();
});

$('#btn-login, #btn-register').click(function(e){
  e.preventDefault();
});