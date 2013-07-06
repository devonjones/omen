var i = 0;

$(function() {
	window.setInterval(
		function() {
			replace_image();
		}, 30000);
});

function replace_image() {
	$.ajax({ url: "/images/current"}).done(function(data) {
		if(data.image) {
			var url = "/content/" + data.image
			var win = $(window);
			var fullscreen = $('#full');
			var img = new Image();
			img.onload = function() {
				var imageWidth = this.width;
				var imageHeight = this.height;
				$("#display").fadeOut('slow', function() {
					image = fullscreen.find('img')[0];
					image.src = url;
					var imageRatio = imageWidth / imageHeight;
					var winWidth = win.width();
					var winHeight = win.height();
					var winRatio = winWidth / winHeight;
					image = fullscreen.find('img');
					if(winRatio < imageRatio) {
						image.css({
							width: winWidth,
							height: Math.round(winWidth / imageRatio)
						});
					} else {
						image.css({
							width: Math.round(winHeight * imageRatio),
							height: winHeight
						});
					}
					$("#display").fadeIn();
				});
			}
			img.src = url;
		}
	});
}

