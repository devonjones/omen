var i = 0;

$(function() {
  window.setInterval(function() { $("#timer-content").text(++i); }, 1000);
});

$(function() {

  var win = $(window),
      fullscreen = $('#full'),
      image = fullscreen.find('img'),
      imageWidth = image.width(),
      imageHeight = image.height(),
      imageRatio = imageWidth / imageHeight;

  function resizeImage() {
    var winWidth = win.width(),
        winHeight = win.height(),
        winRatio = winWidth / winHeight;
  
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
  }

  win.bind({
    load: function() {
      resizeImage();
    },
    resize: function() {
      resizeImage();
    }
  });

});
