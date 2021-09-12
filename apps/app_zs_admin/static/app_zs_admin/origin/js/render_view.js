// iframe onload skeleton
function removeOnloadFrame() {
	$(".iframe-onloading").remove()
}
function removeOnloadFrame_type2() {
	$(".iframe-onloading.type2").remove()
}
function removeOnloadFrame_type3() {
	$(".iframe-onloading.type3").remove()
}

$('iframe').on('load', function () {
	removeOnloadFrame();
}).show();

if($('#external-container').contents().find('h1:contains("Empty content frame.")').length > 0) {
	setTimeout(removeOnloadFrame, 1000);
}

setTimeout(removeOnloadFrame_type2, 1000);
setTimeout(removeOnloadFrame_type3, 2000);