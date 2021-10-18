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
			var css = '@page { size: landscape; margin: 0 auto; }'
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
let menu_delete_row = `<button onclick="detail_table_events(this)" class="delete_row" title="удалить запись">
	<svg viewBox="0 0 330 330">
		<g id="XMLID_6_">
			<g id="XMLID_11_">
				<path d="M240,121.076H30V275c0,8.284,6.716,15,15,15h60h37.596c19.246,24.348,49.031,40,82.404,40c57.897,0,105-47.103,105-105
					C330,172.195,290.816,128.377,240,121.076z M225,300c-41.355,0-75-33.645-75-75s33.645-75,75-75s75,33.645,75,75
					S266.355,300,225,300z"/>
			</g>
			<g id="XMLID_18_">
				<path d="M240,90h15c8.284,0,15-6.716,15-15s-6.716-15-15-15h-30h-15V15c0-8.284-6.716-15-15-15H75c-8.284,0-15,6.716-15,15v45H45
					H15C6.716,60,0,66.716,0,75s6.716,15,15,15h15H240z M90,30h90v30h-15h-60H90V30z"/>
			</g>
			<g id="XMLID_23_">
				<path d="M256.819,193.181c-5.857-5.858-15.355-5.858-21.213,0L225,203.787l-10.606-10.606c-5.857-5.858-15.355-5.858-21.213,0
					c-5.858,5.858-5.858,15.355,0,21.213L203.787,225l-10.606,10.606c-5.858,5.858-5.858,15.355,0,21.213
					c2.929,2.929,6.768,4.394,10.606,4.394c3.839,0,7.678-1.465,10.607-4.394L225,246.213l10.606,10.606
					c2.929,2.929,6.768,4.394,10.607,4.394c3.839,0,7.678-1.465,10.606-4.394c5.858-5.858,5.858-15.355,0-21.213L246.213,225
					l10.606-10.606C262.678,208.535,262.678,199.039,256.819,193.181z"/>
			</g>
		</g>
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
		$('.extra_menu').append(menu_delete_row);
	}
}, function() {
	$('.extra_menu').off('hover').hover(function() {

	}, function() {
		$('.extra_menu').remove();
	})
})


function clear_m2m_field(id) {
	let element = $('#'+id)
	let selector_available = element.parent().parent().parent().find('.selector-available select')
	let options_for_unselected = element.parent().find('option');
	for (var i = 0; i < options_for_unselected.length; i++) {
		selector_available.append(options_for_unselected.eq(i));
	}
}


function add_m2m_field(id, index) {
	let element = $(`#${id} option`).eq(index);
	let selector_available = element.parent().parent().parent().find('.selector-chosen select')
	selector_available.append(element);
}


let clone_form_props;
$(document).on('submit', '.form_frame.edit_form', function(e){
	var frm = $(this).find('form');
	if ($(this).hasClass('edit_form') || $(this).hasClass('add_form')) {
		e.preventDefault();
	}
	if ($(this).hasClass('edit_form')) {
		$.ajax({ 
		    url: `/zs_admin/notification_events_publication/${_row_id}/edit_row/`, // the endpoint
		    type: "POST", // http method
			headers: {
				"X-CSRFToken": csrf_token
			},
		    data: {
		    	"event" : "edit_form"
		    }, // data sent with the post request
		    // handle a successful response
			headers: {
				"X-CSRFToken": csrf_token
			},
			data: frm.serialize(),
			success: function(data, status) {
				//console.log(_row_columns)
				console.log('success: edit_form');
				let updated_row, columns;
				for (var i = 0; i < data.length; i++) {
					updated_row = data[i]['fields'];
					columns = Object.keys(updated_row)
					let k;
					for (var j = 0; j < columns.length; j++) {
						k = columns[j]
						_row_columns.each(function() {
							if ($(this).data(k) != undefined ) {
								let v = updated_row[k];
								if (typeof(v) === 'boolean') {
									if(v) {
										v = 'True'
									} else {
										v = 'False'
									}
									$(this).find('div').text(v)
								} else {
									if (v.constructor === Array) {
										v = v.join(", ")
									} else {
										$(this).find('div').text(v)
									}
								}

								console.log(k, v, typeof(v), $(this).find('div').text());
							}
						})
					}
				}
			},
			// handle a non-successful response
			error: function(xhr,errmsg,err) {
				console.log('error: edit_form');
			}
		});
	}
	if ($(this).hasClass('add_form')) {
		console.log('add_form')
	}
	$(this).find('#form-app > fieldset > .items-container').remove();
	$(this).find('#form-app > fieldset').prepend(clone_form_props);
	$(this).removeClass('edit_form').removeClass('add_form');
});


function detail_table_events (selector) {
	_this = $(selector);
	_detail_table = _this.closest('.form-detail-table-container');
	_detail_form_id = $('#'+_detail_table.attr('id').replace('detail_', ''));
	_row_columns = _this.parent().parent().find('td');
	_row_id = _this.parent().parent().find('[data-id]').text();

	
	if (_this.hasClass('show_edit_form')) {
		clone_form_props = _detail_form_id.find('#form-app > fieldset > .items-container').clone();
		_data = []
		$(_detail_table).find('.t-header th').each(function(index) {
			let _k = (Object.keys($(this).data())[0])
			let _v = _row_columns.eq(index).text()
			if (_v === "None") {
				console.log("None", _k, _v)
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
								let clear_m2m_btn_id = _form_field.parent().parent().find('.selector-clearall').attr('id');
								setTimeout(clear_m2m_field(clear_m2m_btn_id), 1000);
								m2m_v = _v.split(';');
								m2m_v.forEach(function(val, idx) {
									val = val.trimLeft();
									_form_field.find('option').each(function(index) {
										if ($(this).text() === val) {
											let m2m_selected_index = $(this)[0].index;
											let m2m_selected_id = $(this).parent().attr('id');
											add_m2m_field(m2m_selected_id, m2m_selected_index);
											return false;
										}
									});
								});
							}
						}
					}
				}
			}
		});
		_detail_form_id.addClass('edit_form');
	}
	if (_this.hasClass('show_add_form')) {
		//console.log(_detail_form_id)
		// $(document).on('submit', '.login-form', function(){
		// 	$.ajax({ 
		// 		url: this.action, 
		// 		type: $(this).attr('method'), 
		// 		headers: {
		// 			"X-CSRFToken": csrf_token
		// 		},
		// 		data: $(this).serialize(),
		// 		context: this,
		// 		success: function(data, status) {
		// 			console.log('success: delete_row');
		// 		},
		// 		// handle a non-successful response
		// 		error: function(xhr,errmsg,err) {
		// 			console.log('error: delete_row');
		// 		}
		// 	});
		// 	return false;
		// });
	}
	if (_this.hasClass('delete_row')) {
		$.ajax({
		    url: `/zs_admin/notification_events_publication/${_row_id}/delete_row/`, // the endpoint
		    type: "POST", // http method
			headers: {
				"X-CSRFToken": csrf_token
			},
		    data: {
		    	"event" : "delete_row"
		    }, // data sent with the post request
		    // handle a successful response
		    success: function(json) {
		        //$('#post-text').val(''); // remove the value from the input
		        //console.log(json); // log the returned json to the console
		        if (json === '200') {
	    			//console.log('success: delete_row');  // another sanity check
		        	_this.parent().parent().remove();
		        }
		    },
		    // handle a non-successful response
		    error: function(xhr,errmsg,err) {
		    	//console.log('error: delete_row');
		        // $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+ " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
		        // console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
		    }
		});
	}
}
