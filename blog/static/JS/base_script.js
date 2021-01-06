$(function() {
	$(".menu a").on('click', function() {
		$('html, body').animate({
			scrollTop: $($.attr(this, 'href')).offset().top
		}, 800); // 800 = 0.8 secs
	});
});