var nav = document.querySelectorAll('.main nav a');
for (var num in nav) {
    try {
        var link = nav[num];
        if (link.getAttribute('href') == window.location.pathname) {
            link.classList.add('current');
        } else {
            link.classList.toggle('current', false);
        }
    } catch (e) {

    }
}
disTime(0);



$(document).ready(function(){
  $('#a4').change(function(){
  $('#gray').attr('disabled',!this.checked);
  $('#colored').attr('disabled',!this.checked);
  });
});
$(document).ready(function(){
   $('.item').click(function(){
   $('.active').removeClass('active');
   $(this).addClass('active');
   document.getElementById(".tab").addClass('active');
});

   $('#myTabs a').click(function (e) {
  e.preventDefault()
  $(this).tab('show')
})

$(document).ready(function(){
	$('#myTabs a').click(function (e) {
  	e.preventDefault()
  	$(this).tab('show')
	})
});
