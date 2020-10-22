$(function() {
	$(".menu a").on('click', function() {
		$('html, body').animate({
			scrollTop: $($.attr(this, 'href')).offset().top
		}, 800); // 500 = 0.5 secs
	});
});