$(document).ready(function(){
	
	//if load self in iframe
    function inIframe () {
        try {
            return window.self !== window.top;
        } catch (e) {
            return true;
        }
    }
    if(inIframe()) {
		window.location.href="about:blank";
    }

	// Burger-menu
	const container = document.querySelector('#container');
		if($('#button-menu').length > 0) {
		document.querySelector('#button-menu').addEventListener('click', () => {
			container.classList.toggle('active');
			removeActiveClass('all');
		});
	}

	const containerSize = () => {
		if (window.innerWidth > 968) {
			container.classList.add('active');
		}
		if(window.innerWidth > 768 && window.innerWidth <= 968) {
			container.classList.remove('active');
		}
		if(window.innerWidth <= 768) {
			container.classList.add('active');
			if(scrollContainer !== null) {
				scrollContainer.addEventListener("wheel", horizontal_scroll);
			}
		} else {
			if(scrollContainer !== null) {
				scrollContainer.removeEventListener("wheel", horizontal_scroll);
			}
		}
	}

	//containerSize();
	window.addEventListener('resize', () => {
		containerSize();
		removeActiveClass('all');
	});

	//container-aside-left > MENU
	$('.container-aside-left .item-group a').off('click').click(function () {
		removeActiveClass('container-aside-left');
		// nested items by level
		var items = $(this).parent().find('a');
		var clickedItem_index = $(this).index();
		var stopIter = 0;

		if($(this).hasClass('level-1')) {
			var lvl_inner = 'level-2'
			//console.log(items.eq($(this).index()+1))
		 	for (var i = 1; i < 15; i++) {
		 		if ($(items.eq($(this).index()+i)).hasClass(lvl_inner)) {
					if($(items.eq($(this).index()+i)).hasClass("displayBlock")) {
						$(items.eq($(this).index()+i)).removeClass("displayBlock");
					} else {
						$(items.eq($(this).index()+i)).addClass("displayBlock");
					}
		 		} else {
		 			if ($(items.eq($(this).index()+i)).hasClass('level-3') || $(items.eq($(this).index()+i)).hasClass('level-4')) {
						$(items.eq($(this).index()+i)).removeClass("displayBlock");
		 			}
		 		}
		 		if ($(items.eq($(this).index()+i)).hasClass('level-1')) {
		 			break
		 		}
		 	}
		}

		if($(this).hasClass('level-2')) {
			var lvl_inner = 'level-3'
			//console.log(items.eq($(this).index()+1))
		 	for (var i = 1; i < 15; i++) {
		 		if ($(items.eq($(this).index()+i)).hasClass(lvl_inner)) {
					if($(items.eq($(this).index()+i)).hasClass("displayBlock")) {
						$(items.eq($(this).index()+i)).removeClass("displayBlock");
					} else {
						$(items.eq($(this).index()+i)).addClass("displayBlock");
					}
		 		} else {
		 			if ($(items.eq($(this).index()+i)).hasClass('level-4')) {
						$(items.eq($(this).index()+i)).removeClass("displayBlock");
		 			}
		 		}
		 		if ($(items.eq($(this).index()+i)).hasClass('level-2')) {
		 			break
		 		}
		 	}
		}

		if($(this).hasClass('level-3')) {
			var lvl_inner = 'level-4'
			//console.log(items.eq($(this).index()+1))
		 	for (var i = 1; i < 15; i++) {
		 		if ($(items.eq($(this).index()+i)).hasClass(lvl_inner)) {
					if($(items.eq($(this).index()+i)).hasClass("displayBlock")) {
						$(items.eq($(this).index()+i)).removeClass("displayBlock");
					} else {
						$(items.eq($(this).index()+i)).addClass("displayBlock");
					}
		 		} else {
		 			if ($(items.eq($(this).index()+i)).hasClass('level-5')) {
						$(items.eq($(this).index()+i)).removeClass("displayBlock");
		 			}
		 		}
		 		if ($(items.eq($(this).index()+i)).hasClass('level-3')) {
		 			break
		 		}
		 	}
		}

		if($(this).hasClass('level-4')) {
			var lvl_inner = 'level-5'
			//console.log(items.eq($(this).index()+1))
		 	for (var i = 1; i < 15; i++) {
		 		if ($(items.eq($(this).index()+i)).hasClass(lvl_inner)) {
					if($(items.eq($(this).index()+i)).hasClass("displayBlock")) {
						$(items.eq($(this).index()+i)).removeClass("displayBlock");
					} else {
						$(items.eq($(this).index()+i)).addClass("displayBlock");
					}
		 		}
		 		if ($(items.eq($(this).index()+i)).hasClass('level-4')) {
		 			break
		 		}
		 	}
		}


		function toggle_arrows_for_items(_$this) {
			$('.container-aside-left a').not(_$this).removeClass('selected');
			if (_$this.is('.level-1, .level-2, .level-3, .level-4, .level-5')) {
				let closest_lvl_1 = 0;
				let closest_lvl_2 = 0;
				let closest_lvl_3 = 0;
				let closest_lvl_4 = 0;
				let closest_lvl_5 = 0;
				for (let i = _$this.index(); i > -1; i--) { 
					if(_$this.parent().find('a').eq(i).hasClass('level-1')) {closest_lvl_1 = _$this.parent().find('a').eq(i);}
					if(closest_lvl_1 != 0) { 
						break
					}
				}
	
				if(_$this.parent().find('.level-1.tl54321').length > 0) {
					if(closest_lvl_1.index() !== _$this.parent().find('.level-1.tl54321').index()) {
						_$this.parent().find('.level-5.arrow-selected, .level-5.tl54321').removeClass(['arrow-selected', 'tl54321', 'displayBlock']);
						_$this.parent().find('.level-4.arrow-selected, .level-4.tl54321').removeClass(['arrow-selected', 'tl54321', 'displayBlock']);
						_$this.parent().find('.level-3.arrow-selected, .level-3.tl54321').removeClass(['arrow-selected', 'tl54321', 'displayBlock']);
						_$this.parent().find('.level-2.arrow-selected, .level-2.tl54321').removeClass(['arrow-selected', 'tl54321', 'displayBlock']);
						_$this.parent().find('.level-1.arrow-selected, .level-1.tl54321').removeClass(['arrow-selected', 'tl54321', 'displayBlock']);
					}
				}
				for (let i = closest_lvl_1.index() + 1; i < closest_lvl_1.parent().find('a').length + 1; i++) {
					if(closest_lvl_1.parent().find('a').eq(i).hasClass('level-2')) {closest_lvl_2 = closest_lvl_1.parent().find('a').eq(i).addClass('tl54321');}
					if(closest_lvl_1.parent().find('a').eq(i).hasClass('level-3')) {closest_lvl_3 = closest_lvl_1.parent().find('a').eq(i).addClass('tl54321');}
					if(closest_lvl_1.parent().find('a').eq(i).hasClass('level-4')) {closest_lvl_4 = closest_lvl_1.parent().find('a').eq(i).addClass('tl54321');}
					if(closest_lvl_1.parent().find('a').eq(i).hasClass('level-5')) {closest_lvl_5 = closest_lvl_1.parent().find('a').eq(i).addClass('tl54321');}
					if(closest_lvl_1.parent().find('a').eq(i).hasClass('level-1')) { 
						break
					}
				}

				closest_lvl_1.addClass('tl54321')

				if(_$this.hasClass('level-1')) {				
					if(_$this.find('i.fas').hasClass('arrow')) {
						_$this.toggleClass('arrow-selected');
						if(!_$this.hasClass('arrow-selected')) {
							_$this.parent().find('.level-5.arrow-selected, .level-5.tl54321').removeClass(['arrow-selected', 'tl54321', 'displayBlock']);
							_$this.parent().find('.level-4.arrow-selected, .level-4.tl54321').removeClass(['arrow-selected', 'tl54321', 'displayBlock']);
							_$this.parent().find('.level-3.arrow-selected, .level-3.tl54321').removeClass(['arrow-selected', 'tl54321', 'displayBlock']);
							_$this.parent().find('.level-2.arrow-selected, .level-2.tl54321').removeClass(['arrow-selected', 'tl54321', 'displayBlock']);
							_$this.parent().find('.level-1.arrow-selected, .level-1.tl54321').removeClass(['arrow-selected', 'tl54321', 'displayBlock']);
						}
					}
				}
				if(_$this.hasClass('level-2')) {
					if(_$this.find('i.fas').hasClass('arrow')) {
						_$this.toggleClass('arrow-selected');
						if(!_$this.hasClass('arrow-selected')) {
							_$this.parent().find('.level-5.arrow-selected').removeClass('arrow-selected');
							_$this.parent().find('.level-4.arrow-selected').removeClass('arrow-selected');
							_$this.parent().find('.level-3.arrow-selected').removeClass('arrow-selected');
						}
					}
				}	
				if(_$this.hasClass('level-3')) {
					if(_$this.find('i.fas').hasClass('arrow')) {
						_$this.toggleClass('arrow-selected');
						if(!_$this.hasClass('arrow-selected')) {
							_$this.parent().find('.level-5.arrow-selected').removeClass('arrow-selected');
							_$this.parent().find('.level-4.arrow-selected').removeClass('arrow-selected');
						}
					}
				}	
				if(_$this.hasClass('level-4')) {
					if(_$this.find('i.fas').hasClass('arrow')) {
						_$this.toggleClass('arrow-selected');
						if(!_$this.hasClass('arrow-selected')) {
							_$this.parent().find('.level-5.arrow-selected').removeClass('arrow-selected');
						}
					}
				}		
				if(_$this.hasClass('level-5')) {
					if(_$this.find('i.fas').hasClass('arrow')) {
						_$this.toggleClass('arrow-selected');
					}
				}	
			} else {
				_$this.parent().find('.level-5').removeClass(['arrow-selected', 'tl54321', 'displayBlock']);
				_$this.parent().find('.level-4').removeClass(['arrow-selected', 'tl54321', 'displayBlock']);
				_$this.parent().find('.level-3').removeClass(['arrow-selected', 'tl54321', 'displayBlock']);
				_$this.parent().find('.level-2').removeClass(['arrow-selected', 'tl54321', 'displayBlock']);
				_$this.parent().find('.level-1').removeClass(['arrow-selected', 'tl54321', 'displayBlock']);
			}


			//$('.container-aside-left a').removeClass('selected');
			if(_$this.find('i.fas').hasClass('folder')) {
				_$this.toggleClass('selected');
			}
		}
		// container.active
		if($('.container').hasClass('active') === true) {
			// container-aside-left > item-group > items > a
			if($(this).parent().hasClass('items')) {
				toggle_arrows_for_items($(this))
			}
			// container-aside-left > item-group > items-header > a
			if($(this).parent().hasClass('item-group')) {
				if($(this).parent().has('.items').length === 0) {
					$('.container-aside-left a').removeClass('selected');
					$('.container-aside-left').find('.level-5.arrow-selected, .level-5.tl54321').removeClass(['arrow-selected', 'tl54321', 'displayBlock']);
					$('.container-aside-left').find('.level-4.arrow-selected, .level-4.tl54321').removeClass(['arrow-selected', 'tl54321', 'displayBlock']);
					$('.container-aside-left').find('.level-3.arrow-selected, .level-3.tl54321').removeClass(['arrow-selected', 'tl54321', 'displayBlock']);
					$('.container-aside-left').find('.level-2.arrow-selected, .level-2.tl54321').removeClass(['arrow-selected', 'tl54321', 'displayBlock']);
					$('.container-aside-left').find('.level-1.arrow-selected, .level-1.tl54321').removeClass(['arrow-selected', 'tl54321', 'displayBlock']);
					
					$(this).addClass('selected');
					// container-aside-left > item-group > items-header > a
				} else {
					// container-aside-left > item-group > items > a
				}
			}	
		} else {
			// container-aside-left > item-group > items > a
			if($(this).parent().hasClass('items')) {
				toggle_arrows_for_items($(this))
			}
			// container-aside-left > item-group > items-header > a
			if($(this).parent().hasClass('item-group')) {
				if($(this).parent().has('.items').length === 0) {
					$('.container-aside-left a').removeClass('selected');
					$('.container-aside-left').find('.level-5.arrow-selected, .level-5.tl54321').removeClass(['arrow-selected', 'tl54321', 'displayBlock']);
					$('.container-aside-left').find('.level-4.arrow-selected, .level-4.tl54321').removeClass(['arrow-selected', 'tl54321', 'displayBlock']);
					$('.container-aside-left').find('.level-3.arrow-selected, .level-3.tl54321').removeClass(['arrow-selected', 'tl54321', 'displayBlock']);
					$('.container-aside-left').find('.level-2.arrow-selected, .level-2.tl54321').removeClass(['arrow-selected', 'tl54321', 'displayBlock']);
					$('.container-aside-left').find('.level-1.arrow-selected, .level-1.tl54321').removeClass(['arrow-selected', 'tl54321', 'displayBlock']);
					
					$(this).addClass('selected');
					// container-aside-left > item-group > items-header > a
				} else {
					// container-aside-left > item-group > items > a
					if($(this).parent().hasClass('active') === false) {
						$('.container-aside-left .item-group').removeClass('active');
						$(this).parent().toggleClass('active');
					} else {
						$(this).parent().toggleClass('active');
					}
				}
			}
		}

	});
	//header-section-right > MENU
	//mouse wheel horizontal scroll
	const scrollContainer = document.querySelector(".header-section-right");
	function horizontal_scroll(evt) {
		evt.preventDefault();
		scrollContainer.scrollLeft += evt.deltaY;

	}


	$('.header-section-right .item-group .items-header').off('click').click(function () {
		removeActiveClass('header-section-right');
		// header-section-right > item-group > items-header
		if($(this).parent().hasClass('item-group')) {
			if($(this).parent().hasClass('active') === false) {
				$('.header-section-right .item-group').removeClass('active');
				$(this).parent().toggleClass('active');
			} else {
				$(this).parent().toggleClass('active');
			}
		}

		if($(this).children().attr('id') === 'search-extra-button') {
			$('.container').addClass('active');
			if($(this).parent().hasClass('active')) {
				$('.header-section-center').toggleClass('active');
			}

		}
		// header-section-right > item-group > items > a.row.link
	});
	
	// container-main full screen mode on/off
	if(document.getElementsByClassName('full-screen-button').length > 0) {
		[].forEach.call(document.getElementsByClassName('full-screen-button'),function(el){
		    el.addEventListener("click", toggle_fullscreen_mode, false);
		});

		let prev_classlist_names = [];
		function prev_classlist_names_clear() {
			prev_classlist_names = [];
		}

		function prev_classlist_names_update(classlist) {
			if(classlist.length > 0) {
				for (let i = 1; i < classlist.length; i++) {
					prev_classlist_names.push(classlist[i]);
				}
			}
		};

		function prev_classlist_names_set(classlist, prev_classlist) {
			if(prev_classlist_names.length > 0) {
				for (let i = 0; i < prev_classlist_names.length; i++) {
					if (prev_classlist_names[i] !== 'container' || prev_classlist_names[i] !== 'container-aside-left-disabled' || prev_classlist_names[i] !== 'container-header-disabled' || prev_classlist_names[i] !== 'container-main-padding-off') {
						classlist.add(prev_classlist_names[i]);
					}
				}
			}
		};

		prev_classlist_names_update(container.classList);
		function toggle_fullscreen_mode(ele) {
			if (document.querySelectorAll('#container.container-aside-left-disabled.container-header-disabled.container-main-padding-off').length === 1) {
				container.classList.remove('container-aside-left-disabled');
				container.classList.remove('container-header-disabled');
				container.classList.remove('container-main-padding-off');
				prev_classlist_names_set(container.classList, prev_classlist_names);
			} else {
				prev_classlist_names_clear();
				prev_classlist_names_update(container.classList);
				container.classList.remove('fixed');
				container.classList.add('container-aside-left-disabled');
				container.classList.add('container-header-disabled');
				container.classList.add('container-main-padding-off');
			}
		}	
	}
	
	// container-main
	$('.container .container-main').off('click').click(function () {
		if ($('.container .container-main').hasClass('fade-bg') === true) {
			$('.container').addClass('active');
			$('.container .container-main ').removeClass('fade-bg');
		}
	});
	//REMOVE ACTIVE
	function removeActiveClass(notLike) {
		if(notLike !== 'container-aside-left') {
			// container-aside-left  > item-group
			$('.container-aside-left .item-group').removeClass('active');
		}
		if(notLike !== 'header-section-right') {
			// header-section-right > item-group
			$('.header-section-right .item-group').removeClass('active');
		}
		if(notLike !== 'header-section-center') {
			// header-section-center
			$('.header-section-center').removeClass('active');
		}

		if(window.innerWidth <= 768) {
			if ($('.container').hasClass('active') === false) {
				$('.container .container-main ').addClass('fade-bg');
			} else {
				$('.container .container-main ').removeClass('fade-bg');
			}
		} else {
			$('.container .container-main ').removeClass('fade-bg');
		}
	};
	//REMOVE SELECTED
	function removeSelectedClass() {
		// container-aside-left  > item-group
		// header-section-right > item-group
	};

	//Tooltip position
	let tooltip_position;
	$('[data-tooltip]').mouseenter(function(){
		tooltip_position = $(this).attr('data-tooltip-position');
		if(tooltip_position !== undefined) {
			if(!$(this).hasClass(tooltip_position)) {
				$(this).addClass(tooltip_position);
			}
		}
	});


	$('#external-container').contents().click(function(){
	    $('.item-group.active').removeClass('active');
	});

	$(document).mouseup(function (e) {
	    var querySelector1 = $(".item-group, .header-section-right button, .header-section-center");
	    if (!querySelector1.is(e.target)
	        && querySelector1.has(e.target).length === 0)
	    {
			removeActiveClass('all');
	    }

	});

	//notification_events_confirm
	let notification_container = $('#notification').parent().parent();
	if (notification_container.length > 0) {
		notification_container.on('click', function() {
			if (notification_event_confirm === 0) {
				notification_event_confirm = 1;
				$('.notification-count').css('visibility', 'hidden');
				if (notification_container.hasClass('active')) {
					$.ajax({
						url: `/zs_admin/notification_events_confirm/${request_user_id}/`,
						dataType: 'json',
						headers: {
							'csrf_token':'{% csrf_token %}'
						},
						success:function(data){
							console.log('event notification confirm status: ', data);
						}
					});
				}
			}
		});
	}

	let message_container = document.querySelector('.message-container');
	let message_data;
	function update_message_container() {
		if(message_container.classList.contains('active')) { 

			message_container.querySelector('.groups-header').remove();
			message_container.querySelector('.groups-data > .item').remove();

			async function load() {
				let url = '/zs_admin/get_user_message/?type=registration_info';
				let obj = await (await fetch(url)).json();
				message_data = {}
				if (obj.response_detais !== '200') {
					message_data["header"] = obj.response_detais
					message_data["items"] = []
				} else {
					message_data["header"] = obj.header
					message_data["items"] = obj.items
				}


				let json_headers = message_data.header;
				function render_html_message_headers(header) {
					let html_items = []
					const div = document.createElement('div');
					div.className = 'groups-header';
					div.innerText = header
					html_items.push(div)
					return html_items
				}

				let json_items = message_data.items;
				function render_html_message_items(json_items) {
					function get_html_item(name, email) {
						const div = document.createElement('div');
						div.className = 'item';
						div.innerHTML = `<div class="groups-name">${name}</div><div class="groups-email">${email}</div>`
						return div
					}
					let html_items = []
					json_items.forEach((item) => html_items.push(get_html_item(item.name, item.email)))
					return html_items
				}

				render_html_message_headers(json_headers).forEach((item, i) => message_container.querySelector('.groups').prepend(item));
				render_html_message_items(json_items).forEach((item, i) => message_container.querySelector('.groups-data').appendChild(item));

				console.log('function update_message_container');
			}
			load();
		}
	}
	window.setTimeout(update_message_container, 500);
});
