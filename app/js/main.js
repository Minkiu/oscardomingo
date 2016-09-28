
$(".block__works").each(function() {
  var imageUrl = $(this).attr("data-image-src");

  if (typeof imageUrl !== typeof undefined && imageUrl !== false) {
    $(this).css('background', 'url('+imageUrl+') center no-repeat');
    $(this).css('background-size', 'cover');
  }


});