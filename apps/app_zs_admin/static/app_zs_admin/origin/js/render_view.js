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
$('.print-mode').off('click').click(function() {	
	$('.full-screen-button').off('click').click();
	$('.full-screen-button').hide();
	$('.print-mode').hide();
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
		$('.print-mode').show();
		$('.full-screen-button').show();
		$('.full-screen-button').off('click').click();
	}
	setTimeout(waitResizeState, 1000);
})

let extra_menu = '<div class="extra_menu"></div>'
let menu_edit_row = `<button onclick="detail_table_events(this)" class="show_edit_form" title="редактировать запись">
	<svg viewBox="0 0 348.882 348.882">
	<g>
		<path d="M333.988,11.758l-0.42-0.383C325.538,4.04,315.129,0,304.258,0c-12.187,0-23.888,5.159-32.104,14.153L116.803,184.231
			c-1.416,1.55-2.49,3.379-3.154,5.37l-18.267,54.762c-2.112,6.331-1.052,13.333,2.835,18.729c3.918,5.438,10.23,8.685,16.886,8.685
			c0,0,0.001,0,0.001,0c2.879,0,5.693-0.592,8.362-1.76l52.89-23.138c1.923-0.841,3.648-2.076,5.063-3.626L336.771,73.176
			C352.937,55.479,351.69,27.929,333.988,11.758z M130.381,234.247l10.719-32.134l0.904-0.99l20.316,18.556l-0.904,0.99
			L130.381,234.247z M314.621,52.943L182.553,197.53l-20.316-18.556L294.305,34.386c2.583-2.828,6.118-4.386,9.954-4.386
			c3.365,0,6.588,1.252,9.082,3.53l0.419,0.383C319.244,38.922,319.63,47.459,314.621,52.943z"/>
		<path d="M303.85,138.388c-8.284,0-15,6.716-15,15v127.347c0,21.034-17.113,38.147-38.147,38.147H68.904
			c-21.035,0-38.147-17.113-38.147-38.147V100.413c0-21.034,17.113-38.147,38.147-38.147h131.587c8.284,0,15-6.716,15-15
			s-6.716-15-15-15H68.904c-37.577,0-68.147,30.571-68.147,68.147v180.321c0,37.576,30.571,68.147,68.147,68.147h181.798
			c37.576,0,68.147-30.571,68.147-68.147V153.388C318.85,145.104,312.134,138.388,303.85,138.388z"/>
	</svg>
</button>`
// detail form table - row menu
$('.detail-wrapper, .detail-wrapper tr td:not(:nth-child(1))').off('hover').hover(function() {
	$('.extra_menu').remove();
})
$('.form-detail-table-container tbody tr td:nth-child(1)').off('hover').hover(function() {
	$('.extra_menu').remove();
	if ($('.form-detail-table-container tbody tr extra_menu').length === 0) {
		$(this).parent().append(extra_menu);
		$('.extra_menu').append(menu_edit_row);
	}
}, function() {
	$('.extra_menu').off('hover').hover(function() {

	}, function() {
		$('.extra_menu').remove();
	})
})


function clear_m2m_field(id) {
	let element = document.getElementById(id);
	console.log(element)
	element.dispatchEvent(new Event("click"));
}


function append_all_m2m_field(id) {
	let element = document.getElementById(id);
	console.log(element)
	element.dispatchEvent(new Event("click"));
}


function add_m2m_field(id, index) {
	let element = document.querySelectorAll(`#${id} option`)[index];
	element.selected = true;
	document.getElementById('id_content_m2m_add_link').dispatchEvent(new Event("click"));
	console.log(element);
}


function detail_table_events (selector) {
	_this = $(selector);
	_detail_table = _this.closest('.form-detail-table-container');
	_detail_form_id = $('#'+_detail_table.attr('id').replace('detail_', ''));
	_row_columns = _this.parent().parent().find('td');
	_row_id = _this.parent().parent().find('[data-id]').text();

	_data = []
	$(_detail_table).find('.t-header th').each(function(index) {
		let _k = (Object.keys($(this).data())[0])
		let _v = _row_columns.eq(index).text()
		if (_v === '' || _v === null || _v === "None") {
		} else {
			_data.push({[_k]: _v});
			let _form_field = _detail_form_id.find(`[data-${_k}]`);
			if (_k === _form_field.data(_k)) {
				if (_form_field.data('externalPluginResources')) {
				} else {
					if (_form_field.prop("tagName") === 'INPUT') {
						if (_form_field.attr('type') === 'text') {
							_form_field.val(_v);
						}
						if (_form_field.attr('type') === 'checkbox') {
							if (_v === 'True') {
								_form_field.prop('checked', true);
							} else {
								_form_field.prop('checked', false);
							}
						}
					}
					if (_form_field.prop("tagName") === 'TEXTAREA') {
						_form_field.val(_v);
					}
					if (_form_field.prop("tagName") === 'SELECT') {
						if (_form_field.parent().hasClass('selector-available')) {
							// $('.selector-clearall').click(function() { console.log('AAAAAAAAAAAA') })
							let clear_m2m_btn_id = _form_field.parent().parent().find('.selector-clearall').attr('id');
							let append_all_m2m_btn_id = _form_field.parent().parent().find('.selector-add').attr('id');
							//setTimeout(clear_m2m_field(clear_m2m_btn_id), 1000);
							m2m_v = _v.split(';');
							m2m_v.forEach(function(val, idx) {
								val = val.trimLeft();
								_form_field.find('option').each(function(index) {
									if ($(this).text() === val) {
										let m2m_selected_index = $(this)[0].index;
										let m2m_selected_id = $(this).parent().attr('id');
										add_m2m_field(m2m_selected_id, m2m_selected_index);
										console.log(m2m_selected_id, $(this)[0].index, $(this).text(), _form_field.parent().parent().find('.selector-clearall'));
										return false;
									}
								});
							});
							setTimeout(append_all_m2m_field(append_all_m2m_btn_id), 1000);
						}
					}
					//console.log(_k, _form_field.data(_k), _form_field.prop("tagName"))
				}
			}
		}
	});


	if (_this.hasClass('show_edit_form')) {

	}
	if (_this.hasClass('show_add_form')) {
		
	}
	if (_this.hasClass('remove_row')) {
		
	}
}
