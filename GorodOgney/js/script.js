function ShowForm () {
	var posx=($(window).width()-$('.u-form').width())/2;
	var heightBlur=$(window).height();
	$('.blur').css({
		"opacity": "0.6",
		"width": "100%",
		"height":heightBlur+"px"
	});
	$('.u-form').css({
		"opacity": "1",
		"pointer-events": "all",
		"left":posx+"px"
	});
	}

	function HideForm () {
	$('.blur').css({
		"opacity": "0",
		"width": "0",
		"height":"0"
	});
	$('.u-form').css({
		"opacity": "0",
		"pointer-events": "none"
	});
	}