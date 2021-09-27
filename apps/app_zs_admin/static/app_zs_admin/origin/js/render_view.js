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


// load print button
$('[data-tooltip="Поиск"]').off('click').click(function() {	
	$('.full-screen-button').off('click').click();
	$('.full-screen-button').hide();
	function waitResizeState() {
		// mb print landscape
		if ($('.external-container.mb').length > 0) {
			$('.render_view').css('padding-left', '0px');
			$('.external-container.mb').css('height', 'calc(100vh + 200px)');
			var css = '@page { size: landscape; margin: 40px 40px; }',
			head = document.head || document.getElementsByTagName('head')[0],
			style = document.createElement('style');

			style.type = 'text/css';
			style.media = 'print';

			if (style.styleSheet){
			  style.styleSheet.cssText = css;
			} else {
			  style.appendChild(document.createTextNode(css));
			}

			head.appendChild(style);
		} else {
			$('.render_view').css('margin-left', '0px');
		}
		window.print();
		if ($('.external-container.mb').length > 0) {
			$('.render_view').css('padding-left', '');
			$('.external-container.mb').css('height', '');
		} else {
			$('.render_view').css('margin-left', '')
		}
		$('.full-screen-button').show();
		$('.full-screen-button').off('click').click();
	}
	setTimeout(waitResizeState, 1000);
})