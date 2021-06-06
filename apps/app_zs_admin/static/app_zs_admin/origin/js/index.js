$(document).ready(function(){

	// Burger-menu
	const container = document.querySelector('#container');

	document.querySelector('#button-menu').addEventListener('click', () => {
		container.classList.toggle('active');
		removeActiveClass('all');

	});

	const containerSize = () => {
		if (window.innerWidth > 968) {
			container.classList.add('active');
		}
		if(window.innerWidth > 768 && window.innerWidth <= 968) {
			container.classList.remove('active');
		}
		if(window.innerWidth <= 768) {
			container.classList.add('active');
		}	
	}

	containerSize();
	window.addEventListener('resize', () => {
		containerSize();
		removeActiveClass('all');
	});

	//sidebar-left > MENU
	$('.sidebar-left .item-group a').off('click').click(function () {
		removeActiveClass('sidebar-left');
		// nested items by level
		var items = $(this).parent().find('a');
		var clickedItem_index = $(this).index();
		var stopIter = 0;

		if($(this).hasClass('level-1')) {
			var lvl_inner = 'level-2'
			console.log(items.eq($(this).index()+1))
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
			console.log(items.eq($(this).index()+1))
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
			console.log(items.eq($(this).index()+1))
		 	for (var i = 1; i < 15; i++) {
		 		if ($(items.eq($(this).index()+i)).hasClass(lvl_inner)) {
					if($(items.eq($(this).index()+i)).hasClass("displayBlock")) {
						$(items.eq($(this).index()+i)).removeClass("displayBlock");
					} else {
						$(items.eq($(this).index()+i)).addClass("displayBlock");
					}
		 		}
		 		if ($(items.eq($(this).index()+i)).hasClass('level-3')) {
		 			break
		 		}
		 	}
		}


		// container.active
		if($('.container').hasClass('active') === true) {
			// sidebar-left > item-group > items > a
			if($(this).parent().hasClass('items')) {
				$('.sidebar-left a').removeClass('selected');
				$(this).addClass('selected');
			}
			// sidebar-left > item-group > items-header > a
			if($(this).parent().hasClass('item-group')) {
				if($(this).parent().has('.items').length === 0) {
					$('.sidebar-left a').removeClass('selected');
					$(this).addClass('selected');
					// sidebar-left > item-group > items-header > a
				} else {
					// sidebar-left > item-group > items > a
				}
			}	
		} else {
			// sidebar-left > item-group > items > a
			if($(this).parent().hasClass('items')) {
				$('.sidebar-left a').removeClass('selected');
				$(this).addClass('selected');
			}
			// sidebar-left > item-group > items-header > a
			if($(this).parent().hasClass('item-group')) {
				if($(this).parent().has('.items').length === 0) {
					$('.sidebar-left a').removeClass('selected');
					$(this).addClass('selected');
					// sidebar-left > item-group > items-header > a
				} else {
					// sidebar-left > item-group > items > a
					if($(this).parent().hasClass('active') === false) {
						$('.sidebar-left .item-group').removeClass('active');
						$(this).parent().toggleClass('active');
					} else {
						$(this).parent().toggleClass('active');
					}
				}
			}
		}

	});
	//header-right-items > MENU
	$('.header-right-items .item-group .items-header').off('click').click(function () {
		removeActiveClass('header-right-items');
		// header-right-items > item-group > items-header
		if($(this).parent().hasClass('item-group')) {
			if($(this).parent().hasClass('active') === false) {
				$('.header-right-items .item-group').removeClass('active');
				$(this).parent().toggleClass('active');
			} else {
				$(this).parent().toggleClass('active');
			}
		}

		if($(this).children().attr('id') === 'search-active') {
			$('.container').addClass('active');
			if($(this).parent().hasClass('active')) {
				$('.header-center-items').toggleClass('active');
			}

		}
		// header-right-items > item-group > items > a.row.link
	});
	// main content
	$('.container .main').off('click').click(function () {
		if ($('.container .main').hasClass('fade-bg') === true) {
			$('.container').addClass('active');
			$('.container .main ').removeClass('fade-bg');
		}
	});
	//REMOVE ACTIVE
	function removeActiveClass(notLike) {
		if(notLike !== 'sidebar-left') {
			// sidebar-left  > item-group
			$('.sidebar-left .item-group').removeClass('active');
		}
		if(notLike !== 'header-right-items') {
			// header-right-items > item-group
			$('.header-right-items .item-group').removeClass('active');
		}
		if(notLike !== 'header-center-items') {
			// header-center-items
			$('.header-center-items').removeClass('active');
		}

		if(window.innerWidth <= 768) {
			if ($('.container').hasClass('active') === false) {
				$('.container .main ').addClass('fade-bg');
			} else {
				$('.container .main ').removeClass('fade-bg');
			}
		} else {
			$('.container .main ').removeClass('fade-bg');
		}
	};
	//REMOVE SELECTED
	function removeSelectedClass() {
		// sidebar-left  > item-group
		// header-right-items > item-group
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



	$(document).mouseup(function (e) {
	    var querySelector1 = $(".item-group, .header-right-items button, .header-center-items");
	    if (!querySelector1.is(e.target)
	        && querySelector1.has(e.target).length === 0)
	    {
			removeActiveClass('all');
	    }

	});
});