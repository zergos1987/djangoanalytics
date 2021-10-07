from django.http import HttpResponse, FileResponse, Http404, HttpResponseRedirect, HttpResponseForbidden, HttpResponsePermanentRedirect
import random, string
from django.db.models import Q
from django.db.models.functions import Lower
from django.db.models import FloatField, CharField
from django.db.models.functions import Cast
from django.db.models import Max, Case, Value, When
from django.db.models import Aggregate, CharField, Value
import re

from django.contrib.contenttypes.models import ContentType 
from django.apps import apps

from django.core.serializers import serialize
from django.http.response import JsonResponse
import json



def dynamic_datagrid(
	fathgrid_initialize_settings=None,
	request=None,
	request_table=None,
	request_table_title=None,
	request_table_as_dict=False,
	request_table_columns_id=None,
	request_table_columns_props={},
	request_table_filters={},
	request_table_excludes={},
	request_table_secure_values_hide=[],
	request_table_max_limit_rows=20,
	request_m2m_join_columns=[],
	textarea_select_options=[],
	add_row_default={},
	get_media=False):

	def request_table_secure_values_hide_func(value):
		if len(request_table_secure_values_hide) > 0:
			if value in request_table_secure_values_hide:
				value = '*'*len(str(value))
		return value


	if request_table is None:
		request_table = request.GET.get("request_table", request.POST.get("request_table", None))
	request_table_string = request_table
	request_table_obj = ContentType.objects.get(model=request_table_string)
	request_table = apps.get_model(request_table_obj.app_label, request_table)
	

	for col in request_table_columns_props:
		if col.get('db_name', '') == '':
			for col2 in request_table_columns_props:
				col2['db_name'] = ''
		break

	request_table_columns = [col.get('db_name') for col in request_table_columns_props if col.get('db_name') != '']
	request_table_columns_label = [col.get('grid_header_name') for col in request_table_columns_props]
	request_table_columns_props = [col.get('grid_column_props') for col in request_table_columns_props]

	if fathgrid_initialize_settings is not None and request_table_columns == []: fathgrid_initialize_settings['columns_properties'] = ''

	dynamic_table = request_table.objects.all()
	dynamic_columns = []
	for f in ContentType.objects.get(model=request_table_string).model_class()._meta.get_fields():
		column_name = f.name
		if f.__class__.__name__ in ['OneToOneRel', 'ManyToOneRel', 'ManyToManyRel']:
			column_name = None
		if request_table_columns == [] and f.__class__.__name__ in ['ManyToManyField', 'OneToOneField', 'ForeignKey']:
			column_name = None
		if column_name is not None: 
			dynamic_columns.append(column_name)
	if request_table_columns == []: request_table_columns = dynamic_columns


	
	if fathgrid_initialize_settings is not None:
		grid_id = ''.join(random.choices(string.ascii_letters, k=16))
		js_object_html = {}

		columns_data = """{"""
		for idx in range(0, len(request_table_columns)):
			column_name = request_table_columns[idx]
			column_label = column_name
			if len(request_table_columns_label) > 0 and idx < len(request_table_columns_label):
				column_label = request_table_columns_label[idx]
			if len(request_table_columns_props) > 0 and idx < len(request_table_columns_props):
				column_props = request_table_columns_props[idx]
			else:
				column_props = {}

			listOfValues = ''
			if column_props.get('listOfValues', []) != []:
				listOfValues = f"listOfValues: {column_props.get('listOfValues', '')},"
			html = ''
			if column_props.get('html', '') != '':
				html = f"html: {column_props.get('html', '')},".replace('$$$COLUMN$$$', column_name)
			else:
				html = """html: x => `<div class="table-tbody-td-div"><div>${x.$$$COLUMN$$$}</div></div>`""".replace('$$$COLUMN$$$', column_name)
			footer = ''
			if column_props.get('footer', '') != '':
				footer = f"footer: {column_props.get('footer', '')},".replace('$$$COLUMN$$$', column_name)

			columns_data += """},{""" + f"""
				name: '{column_name}', 
				label: '{column_name.upper()}',
				header: '{column_label}',
				class: '{column_props.get('class', '')}',
				disabled: {column_props.get('disabled', 'true')},
				pattern: '{column_props.get('pattern', '')}',
				editable: {column_props.get('editable', 'false')},
				filterable: {column_props.get('filterable', 'false')},
				type: '{column_props.get('type', '')}',
				{listOfValues}
				{footer}
				{html}
			""" 
		if request_table_columns_id is not None:
			columns_data += """
				},{
					name: 'remove', 
					label: 'REMOVE',
					header: ' ', 
					class: 'text-center',
					disabled: true,
					pattern: '',
					editable: false,
					filterable: false,
					type: '',
					footer: '',
					html: x => `<a href="#" class="remove-item" title="удалить строку" onclick="table_$$$grid_id$$$.deleteRow(${ x.$$$request_table_columns_id$$$});return false;"></a>`,
			""".replace('$$$request_table_columns_id$$$', request_table_columns_id)
		columns_data += """}"""

		columns_data = columns_data.replace("{},{", '{')
		fathgrid_initialize_settings['columns_properties'] = columns_data


		js_object_html['js'] = """<script type="text/javascript">
			let table_$$$grid_id$$$, form_$$$grid_id$$$, table_$$$grid_id$$$_data, table_$$$grid_id$$$_dicts;


			function call_table_selector_for_column(from_grid_id, selected_key, item) {
				//console.log('call_table_selector_for_column', selected_key, item);

				let formatted_selected_key = get_formatted_key_value(selected_key);

				function get_formatted_key_value(key) {
					if (key.includes('__')) {
						key = key.slice(key.indexOf('__')+2)
					}
					return key;
				}

				if (item === '-') {
					item = [];
					item.push({id: 0, [formatted_selected_key]: '-'})
				}


				let grid_list = $('.table-grid.fathgrid').not('#' + from_grid_id.id);
				let grid, grid_data;
				let _break = false;
				for (i=0; i < grid_list.length; i++) {
					if (_break === true) {break}
					grid = eval(grid_list[i].id);
					grid_data = grid.getData();
					if (grid_data.length > 0) {
						for (let [key, val] of Object.entries(grid_data[0])) {
							key = get_formatted_key_value(key);
							if (formatted_selected_key === key) {
								//console.log(grid.id, selected_key, formatted_selected_key, `${key}: ${val}`);
								_break = true;
								if (_break === true) {break}
							}
						}
					}
				}


				grid.table_caller = from_grid_id
				grid.table_caller.merge_item = item
				//console.log('1', from_grid_id, '---', grid)
				//console.log('2', grid.id, '---', grid.table_caller, '---')
				//console.log('3', grid.id, '---', grid.table_caller.merge_item)



				let grid_container = $('#'+grid.id).closest('.table-grid-container');
				if (grid_container.length > 0) {
					let grid_showhide_btn = grid_container.find('.grid-display-button');
					let grid_header_btn = grid_container.find('.header-display-button');
					let grid_title_btn = grid_container.find('.title-display-button');
					grid_container.removeClass('displayNone')

					process_dict_items_selection(grid, grid.table_caller.merge_item)

					if (grid_container.hasClass('grid-closed')) {
						if (grid_showhide_btn.length > 0) {
							grid_showhide_btn.off('click').click();
						}
					}
					if (!grid_header_btn.hasClass('displayNone')) {
						grid_header_btn.addClass('displayNone');
						if (grid_header_btn.length > 0) {
							grid_header_btn.off('click').click();
						}
					}
					if (grid_title_btn.length > 0) {
						grid_title_btn.off('click').click();
					}
				}
				return item;
			}

			
			function process_dict_items_selection(_this, item, selected_item) {
				if ($('#'+_this.id).closest('.table-grid-container').hasClass('dict_table') === true && $('#'+_this.id).closest('.table-grid-container').hasClass('displayNone') === false) {
					//console.log('MMMMMMMMMMMMM', _this, item, selected_item)
					let click_items_tbody = $('#'+_this.id+' tbody').find('tr');
					let tmp_merge_item = item;
					let tmp_merge_item_keys = Object.keys(tmp_merge_item[0]);
					if (tmp_merge_item.length > 0) {
						for (h=0; h < tmp_merge_item.length; h++) {
							let row_keys_values = []
							let row_vals = tmp_merge_item[h]
							for (i=0; i < tmp_merge_item_keys.length; i++) {
								let k = tmp_merge_item_keys[i]
								row_keys_values.push(row_vals[k])
							}
							
							for (r=0; r < click_items_tbody.length; r++) {
								let _tr = click_items_tbody.eq(r);       
								if (row_keys_values.length === 1) {
									if ((_tr).is(':contains(' + row_keys_values[0] +')')) {
										(_tr).addClass('dict-selected-item');
										//console.log('1111111111111111111')
									}
								}
								if (row_keys_values.length === 2) {
									if ((_tr).is(':contains(' + row_keys_values[0] +'):contains(' + row_keys_values[1] +')')) {
										(_tr).addClass('dict-selected-item');
										//console.log('1111111111111111111')
									}
								}
							}
						} 
					}
					if (typeof selected_item !== 'undefined') {
						let click_item = selected_item.parent();
						if (click_item.hasClass('dict-selected-item')) {
							let id_item = click_item.find('td').eq(0).text();
							let text_item = click_item.find('td').eq(1).text() || '-';
							click_item.removeClass('dict-selected-item');
							//console.log('remove===', click_item, click_item.find('td').eq(0).text(), click_item.find('td').eq(1).text())
							item = $.grep(item, function(e){ return e.id != id_item; });
						} else {
							let id_item = click_item.find('td').eq(0).text();
							let text_item = click_item.find('td').eq(1).text();
							let id_key = tmp_merge_item_keys[0];
							let text_key = tmp_merge_item_keys[1];
							click_item.addClass('dict-selected-item');
							//console.log('add===', click_item)
							if(tmp_merge_item_keys.length === 2) {
								//console.log('2=======', id_key, parseInt(id_item), text_key, text_item)
								item.push({[id_key]: parseInt(id_item), [text_key]: text_item})
							}
							if(tmp_merge_item_keys.length === 1) {
								//console.log('1=======', id_key, parseInt(id_item), text_key, text_item)
								item.push({[id_key]: parseInt(id_item)})
							}
						}

						return item;
					}
				}
			}
			

			function RenderRow(value, return_id) {
				let value_tmp = value;
				if (typeof(value_tmp) !== undefined) {
					if (Array.isArray(value_tmp)) {
						let id_values_list = '', field_values_list = '';
						for (i=0; i < value_tmp.length; i++) {
							k_id = Object.keys(value_tmp[i])[0]
							k_field = Object.keys(value[i])[1]
							id_values_list += value_tmp[i][k_id] + ', '

							if (k_field !== undefined) {
								field_values_list += value_tmp[i][k_field] + ', '
							}
							//console.log(value_tmp[i])
						}
						if (field_values_list.length > 0 && return_id === false) {
							value_tmp = field_values_list.slice(0,field_values_list.length-2)
						} else {
							value_tmp = id_values_list.slice(0,id_values_list.length-2)
						}
					}
					if (value_tmp === '-') {

					} else {

					}
				}
				return value_tmp;
			}

			function addRow_$$$grid_id$$$(grid_object) {
				$.ajax({
					url: grid_object.wrapperEl.baseURI,
					type: 'POST',
					headers: {
						"X-CSRFToken": 'csrf_token'
					},
					data: {'request_type': 'datagrid', 'event': 'add', 'grid_id': '$$$grid_id$$$', 'request_table': '$$$request_table$$$'},
					cache: true,
					success: function (msg) {
						//console.log('item was created: ', msg, typeof(msg));
						table_$$$grid_id$$$.setData(table_$$$grid_id$$$.getData())
						table_$$$grid_id$$$.setSort([-1])
						// if (msg.toString().includes('DOCTYPE')) {
						// 	$('.header-item.create-item').remove();
						// 	window.alert("500. Ошибка сервера.");
						// 	window.location.reload(true);
						// } else {
						// 	table_$$$grid_id$$$.setData(table_$$$grid_id$$$.getData())
						// }
					}
				});
			}


			function toggleDisplayContent_$$$grid_id$$$(header_object, target) {
				if (target === 'header') {
					$('.table-grid-header.'+header_object).toggleClass('displayNone');
					$('#groupingtable_'+header_object).toggleClass('displayNone');
					$('#graphstable_'+header_object).toggleClass('displayNone');
					$('#columnstable_'+header_object).toggleClass('displayNone');
					$('#exportertable_'+header_object).toggleClass('displayNone');
					$('.printgridtable_'+header_object).toggleClass('displayNone');
				}
				if (target === 'grid') {
					$('.table-grid-header.'+header_object).not('.displayNone').toggleClass('displayNone');
					$('#groupingtable_'+header_object).not('.displayNone').toggleClass('displayNone');
					$('#graphstable_'+header_object).not('.displayNone').toggleClass('displayNone');
					$('#columnstable_'+header_object).not('.displayNone').toggleClass('displayNone');
					$('#exportertable_'+header_object).not('.displayNone').toggleClass('displayNone');
					$('.printgridtable_'+header_object).not('.displayNone').toggleClass('displayNone');

					$('#table_' + header_object + ' .grid-title-header').not('.displayNone').toggleClass('displayNone');

					$('#table-containertable_' + header_object + ' .grid-display-button').toggleClass('active');
					$('#table_' + header_object).closest('.table-grid-container').toggleClass('grid-closed');
					$('#table-containertable_' + header_object + ' .header-display-button').toggleClass('displayNone');
					$('#table-containertable_' + header_object + ' .title-display-button').toggleClass('displayNone');
					$('#table_' + header_object + ' thead').toggleClass('displayNone');
					$('#table_' + header_object + ' tbody').toggleClass('displayNone');
					$('#table_' + header_object + ' tfoot').toggleClass('displayNone');

					if ($('#table_' + header_object).closest('.table-grid-container').hasClass('grid-closed')) {
						$('#table_' + header_object).closest('.table-grid-container').attr('data-content', '$$$request_table_title$$$');
						if ($('#table_' + header_object).closest('.table-grid-container').hasClass('dict_table')) {
							$('.grid-item-display-button').off('click').click()
						}
					} else {
						$('#table_' + header_object).closest('.table-grid-container').removeAttr('data-content');
					}

				}
				if (target === 'title') {
					$('#table_' + header_object + ' .grid-title-header').toggleClass('displayNone');
					if ($('#table_' + header_object + ' .grid-title-header').length === 0) {
						$('#table_' + header_object).prepend('<div class="grid-title-header">$$$request_table_title$$$</div>');
					}
				}
			}

			function close_edit_item(selector) {
				$(selector).parent().addClass('grid-item-close');
			}

			function updateValue(_this) {
				$('[data-originalvalue]').attr('data-originalvalue', _this.value);
				$('[data-originalvalue]').val(_this.value);
				$('.grid-item-display-button').off('click').click();
			}

			function ShowTextareaSelectOptions(colname, colval, textarea_select_options) {
				if (textarea_select_options.length > 0) {
					let item_options = textarea_select_options.map(o => o[colname]).filter(function (el) {return el != null;})[0];
					if (item_options) {
						if (item_options.length > 0) {
							$('.selected [data-originalvalue]').parent().prepend(`<a href="javascript:void(0);" class="textarea_select_options_container"><select onchange="updateValue(this)"></select><a>`);
							$.each(item_options, function (i, item) {
								$('.textarea_select_options_container > select').append($('<option>', { 
									value: item,
									text : item 
								}));
							});
							$(".textarea_select_options_container > select").val(colval);
							$(".textarea_select_options_container").click(function(e) {
								e.stopPropagation();
							});
						}
					}
				}
			}

			$$$request_m2m_join_columns$$$
			$$$textarea_select_options$$$

		 	table_$$$grid_id$$$ = FathGrid("table_$$$grid_id$$$", {
				// // ########## GRID CONFIG SETTINGS ###################
				$$$base_properties$$$
				columns: [
					$$$columns_properties$$$
				],
				// // templated string URL for data retrieval 
				serverURL: '$$$serverURL$$$?request_type=datagrid&request_table=$$$request_table$$$&grid_id=$$$grid_id$$$&_page=${page}&_limit=${size}&_sort=${sort}&_order=${order}&_q=${search}&${filters}',
				// // custom function which converts received JSON object into data array
				prepareData: function(json) {

					table_$$$grid_id$$$_data = json['table_data']
					return table_$$$grid_id$$$_data;
				},
				onInitTable: function(d) {
					process_dict_items_selection(this, table_$$$grid_id$$$.table_caller.merge_item)
				},
				loading: 'Loading...',
				template: '{tools}{info}{graph}{table}{pager}',
				lang: {
					yes: "да",
					export: "Экспорт",
					previous: "Предыдущая",
					next: "Следующая",
					last: "Последняя",
					first: "Первая",
					gotoPage: "Перейти к странице",
					loading: 'Загрузка...',
					selectRow: 'Выбрать строку',
					showSelectedOnly: 'Показать только выбранные строки',
					groupby: 'Группировка колонок',
					avg: 'Avg',
					count: 'Count',
					min: 'Min',
					max: 'Max',
					sum: 'Sum',
					show_grouping_controls: 'Показать настройки группировки колонок',
					show_graph: 'Показать график',
					select_columns: 'Выбрать колонки',
					type: 'Тип',
					none: 'Пусто',
					line: 'Линия',
					bar: 'Столбцы',
					pie: 'Круговая',
				},
				onClick: function(item,col,el) {
					console.log('onClick:', item,col,el);

					
					if ($('#'+this.id).closest('.table-grid-container').hasClass('dict_table') === true) {
						let event_col_name = $('#table_$$$grid_id$$$ > thead > tr:first-child th').eq(col-1).text();
						if(event_col_name === ' ') {
							//console.log('remove row:', item, col)
							item['request_type'] = 'datagrid';
							item['request_table'] = '$$$request_table$$$';
							item['grid_id'] = '$$$grid_id$$$';
							item['event'] = 'remove';
							//example ajax
							$.ajax({
								url: '$$$serverURL$$$',
								type: 'POST',
								headers: {
									"X-CSRFToken": 'csrf_token'
								},
								data: item,
								cache: true,
								success: function (msg) {
									// console.log('item was removed: ', msg, item, typeof(msg));
									if (msg.toString().includes('DOCTYPE')) {
										window.alert("500. Ошибка сервера.");
										window.location.reload(true);
									} else {
										table_$$$grid_id$$$.deleteRow(item.rownum);
									}
								}
							});
						}
						if ($('#' + this.id + ' .grid-item-close').length > 0) {
							//console.log('b')
							table_$$$grid_id$$$.editCell(-1, -1);
						} else {
							//console.log('a')
							table_$$$grid_id$$$.editCell(item.rownum, col);
							$('.selected [data-originalvalue]').parent().prepend('<a href="javascript:void(0);" onclick="close_edit_item(this);" class="grid-item-display-button">S</a>');
						}
						//console.log('old =====', table_$$$grid_id$$$.id, table_$$$grid_id$$$.table_caller, table_$$$grid_id$$$.table_caller.merge_item)
						//console.log('old =====', table_$$$grid_id$$$.table_caller.merge_item)
						table_$$$grid_id$$$.table_caller.merge_item = process_dict_items_selection(this, table_$$$grid_id$$$.table_caller.merge_item, $(el));
						//console.log('new =====', table_$$$grid_id$$$.id, table_$$$grid_id$$$.table_caller, table_$$$grid_id$$$.table_caller.merge_item)
						//console.log('new =====', table_$$$grid_id$$$.table_caller.merge_item) 
					} else {
						if (Array.isArray(table_$$$grid_id$$$.merge_item)) {
							if (table_$$$grid_id$$$.merge_item.length === 0) {
								let selected_item_key_origin = Object.keys(item).filter((key) => key != 'rownum')[col-1];
								let selected_item_key_text = selected_item_key_origin;
								item[selected_item_key_origin] = [{id: 0}]
								table_$$$grid_id$$$.table_caller = '';
								table_$$$grid_id$$$.merge_item = '';
							}
						}
						if (table_$$$grid_id$$$.merge_item != '') {
							let selected_item_key_origin = Object.keys(item).filter((key) => key != 'rownum')[col-1];
							let selected_item_key_text = selected_item_key_origin;
							let selected_item_value = item[selected_item_key_text]
							if (selected_item_key_text.includes('__')) {
								selected_item_key_text = selected_item_key_text.substr(selected_item_key_text.indexOf('__')+2)
							}
							let new_selected_item_value = $.grep(table_$$$grid_id$$$.merge_item, function(e){ return e.id != 0; });
							let new_selected_item_key_text = '-';
							if (new_selected_item_value.length > 0) { new_selected_item_key_text = Object.keys(new_selected_item_value[0]).filter((key) => key === selected_item_key_text)[0]}

							if (selected_item_key_text === new_selected_item_key_text) {
								item[selected_item_key_origin] = new_selected_item_value;
							}
							table_$$$grid_id$$$.table_caller = '';
							table_$$$grid_id$$$.merge_item = '';
							console.log(new_selected_item_value, 'RRRRRRRRRRRRRRRRRRRRRRRRR', item, selected_item_key_text, selected_item_value, new_selected_item_key_text )
						}


						let event_col_name = $('#table_$$$grid_id$$$ > thead > tr:first-child th').eq(col-1).text();
						if(event_col_name === ' ') {
							//console.log('remove row:', item, col)
							item['request_type'] = 'datagrid';
							item['request_table'] = '$$$request_table$$$';
							item['grid_id'] = '$$$grid_id$$$';
							item['event'] = 'remove';
							//example ajax
							$.ajax({
								url: '$$$serverURL$$$',
								type: 'POST',
								headers: {
									"X-CSRFToken": 'csrf_token'
								},
								data: item,
								cache: true,
								success: function (msg) {
									// console.log('item was removed: ', msg, item, typeof(msg));
									if (msg.toString().includes('DOCTYPE')) {
										window.alert("500. Ошибка сервера.");
										window.location.reload(true);
									} else {
										table_$$$grid_id$$$.deleteRow(item.rownum);
									}
								}
							});
						} else {
							if ($('#' + this.id + ' .grid-item-close').length > 0) {
								console.log('b')
								table_$$$grid_id$$$.editCell(-1, -1);
							} else {
								table_$$$grid_id$$$.editCell(item.rownum, col);
								if ($(el).hasClass('textarea_select_options')) {
									let _thisColval = $('.selected [data-originalvalue]').attr('data-originalvalue');
									if (_thisColval.length > 1) {
										let _thisColname = Object.keys(item).find(key => item[key] === _thisColval);
										ShowTextareaSelectOptions(_thisColname, _thisColval, $$$grid_id$$$_textarea_select_options);
									}
								}
								$('.selected [data-originalvalue]').parent().prepend('<button onclick="close_edit_item(this);" class="grid-item-display-button">S</button>');
							}
						}
					}	
				},
				onInitInput: function(item,selected_key,el) {
					//console.log('onInitInput:', item, selected_key, el);

					let init_val = $(el).children().attr('data-originalvalue');
					if ($$$grid_id$$$_request_m2m_join_columns.includes(selected_key) === true) {
						$('.dict-selected-item').removeClass('dict-selected-item')
						let column_id = $(el).children().attr('data-col');
						let selected_value = item[Object.keys(item)[column_id-1]];
						call_table_selector_for_column(table_$$$grid_id$$$, selected_key, selected_value);
						let origin_format_selected_value = RenderRow(selected_value, false);
						$(el).children().attr('data-originalvalue', origin_format_selected_value)
						$(el).children().val(origin_format_selected_value);
					}
					return item;
				},
				onChange: function(item, col, old, value) {
					//console.log("onChange:", item, col, old, value);
					
					let event_col_name = $('#table_$$$grid_id$$$ > thead > tr:first-child th').eq(col-1).text();
					if(event_col_name !== ' ') {
						let tmp_item = item;
						let column_id, selected_key, selected_value;
						if (typeof(old) === 'object') {
							selected_key = Object.keys(item)[col-1];
							selected_value = item[selected_key];
							tmp_item[selected_key] = RenderRow(old, true).replace(/ /g, '');
						}

						//console.log('edit row:', item, col, old, value, typeof(old))
						item['request_type'] = 'datagrid';
						item['request_table'] = '$$$request_table$$$';
						item['grid_id'] = '$$$grid_id$$$';
						item['event'] = 'edit';
						$.ajax({
							url: '$$$serverURL$$$',
							type: 'POST',
							headers: {
								"X-CSRFToken": 'csrf_token'
							},
							data: tmp_item,
							cache: true,
							success: function (msg) {
								// console.log('item was edited: ', msg, item, typeof(msg));
								if (msg.toString().includes('DOCTYPE')) {
									window.location.reload(true);
								} else {
									table_$$$grid_id$$$.setData(table_$$$grid_id$$$.getData())
								}
							}
						});
						/*
						if (selected_key) {
							item[selected_key] = selected_value;
						}
						*/
					}
					return value == '' ? false:true;
				},
				// onInitFilter: function(el){},
			});
			table_$$$grid_id$$$.table_caller = '';
			table_$$$grid_id$$$.merge_item = '';
			setTimeout(document.querySelector("#table_$$$grid_id$$$_size").value = table_$$$grid_id$$$.getPageSize(), 1000);
			setTimeout(document.getElementById("table-containertable_$$$grid_id$$$").prepend(document.querySelectorAll(".header-display-button.$$$grid_id$$$")[0]), 1000);
			setTimeout(document.getElementById("table-containertable_$$$grid_id$$$").prepend(document.querySelectorAll(".grid-display-button.$$$grid_id$$$")[0]), 1000);
			setTimeout(document.getElementById("table-containertable_$$$grid_id$$$").prepend(document.querySelectorAll(".title-display-button.$$$grid_id$$$")[0]), 1000);
			</script>""".replace('$$$base_properties$$$',fathgrid_initialize_settings.get('grid_properties', {}).get('base_properties', '')
				).replace('$$$serverURL$$$',fathgrid_initialize_settings.get('grid_properties', {}).get('serverURL', '')
				).replace('$$$request_table$$$', request_table_string
				).replace('$$$request_table_title$$$', request_table_title
				).replace('$$$columns_properties$$$',fathgrid_initialize_settings.get('columns_properties', '')
				).replace('$$$request_m2m_join_columns$$$', f'let $$$grid_id$$$_request_m2m_join_columns={request_m2m_join_columns}'
				).replace('$$$textarea_select_options$$$', f'let $$$grid_id$$$_textarea_select_options={textarea_select_options}'
				).replace('csrf_token', request.META.get('CSRF_COOKIE', '')
				).replace('$$$grid_id$$$', grid_id)


		js_object_html['html'] = """<div class="table-grid-container $$$dict_table$$$">
				<div class="box-shadow"></div>
				<div class="table-grid-header $$$grid_id$$$">
					<div class="header-item pages-limit">
						<div style="flex-grow: 1">Показать на странице:<select id="table_$$$grid_id$$$_size" onchange="table_$$$grid_id$$$.setPageSize(this.value)">
							<option value="5">5</option>
							<option selected value="10">10</option>
							<option value="20">20</option>
							<option value="50">50</option>
							<option value="100">100</option>
							<option value="0">Все</option>
							</select>
						</div>
					</div>
					$$$addRow$$$
					<div class="header-item search">
						<div class="item-label table-grid-full-text-search">Поиск</div>
						<input onchange="table_$$$grid_id$$$.search(this.value)" type="text" class="form-control" aria-label="Default" aria-describedby="inputGroup-sizing-default">
					</div>
				</div> 

				<table class="table-grid" id="table_$$$grid_id$$$">
					<thead></thead>
					<tbody></tbody>
				</table>

				<button onclick="toggleDisplayContent_$$$grid_id$$$('$$$grid_id$$$', 'header');" class="header-display-button $$$grid_id$$$" title="Скрыть/Отобразить настройки">F</button>
				<button onclick="toggleDisplayContent_$$$grid_id$$$('$$$grid_id$$$', 'grid');" class="grid-display-button $$$grid_id$$$" title="Скрыть/Отобразить таблицу">G</button>
				<button onclick="toggleDisplayContent_$$$grid_id$$$('$$$grid_id$$$', 'title');" class="title-display-button $$$grid_id$$$" title="Скрыть/Отобразить заголовок">T</button>

				<div class="table-grid-form" id="form_$$$grid_id$$$">
					<div class="modal-content" style="background: #aaa;">
						<div class="modal-header">
							<h5 class="modal-title">form_$$$grid_id$$$</h5>
							<button type="button" class="close" onclick="document.querySelector('#form_$$$grid_id$$$').style.width=0">&times;</button>
						</div>
						<div class="modal-body">
							<div id="form_$$$grid_id$$$-container">(select record)</div>
						</div>
						<div class="modal-footer">
							<button type="button" class="btn btn-secondary" onclick="form_$$$grid_id$$$.reset()">Reset</button>
							<button type="button" class="btn btn-primary" onclick="form_$$$grid_id$$$.save()">Save</button>
						</div>
					</div>
				</div>
			</div>""".replace('$$$grid_id$$$', grid_id)

		html_addRow = """
			<div class="header-item create-item">
				<!-- <div class="item-label table-grid-add-row-form">+</div> -->
				<!-- <button onclick="table_$$$grid_id$$$.search(this.value)" class="form-button"></button> -->
				<button onclick="addRow_$$$grid_id$$$(table_$$$grid_id$$$);" class="add-row-button" title="Добавить новую строку">+</button>
			</div>
		""".replace('$$$grid_id$$$', grid_id)

		if add_row_default != {}:
			js_object_html['html'] = js_object_html.get('html').replace("$$$addRow$$$", html_addRow)
		else:
			js_object_html['html'] = js_object_html.get('html').replace("$$$addRow$$$", '')

		if request_table_as_dict == True:
			js_object_html['html'] = js_object_html.get('html').replace("$$$dict_table$$$", 'dict_table displayNone')
		else:
			js_object_html['html'] = js_object_html.get('html').replace("$$$dict_table$$$", '')		

		if get_media:
			path = '/static/app_zs_admin/vendor/FathGrid-master/dist/'
			js_object_html['media'] = {
					'css': [
						# path + 'fathgrid.css', 
						# path + 'fathform.css' 
					], 
					'js': [
						# path + 'fathform.js',
						path + 'jspdf.umd.min.js', 
						path + 'Chart.bundle.min.js', 
						path + 'FathGrid.js', 
						path + 'fathform.js', 
					],
				}

		return js_object_html


	try:
		request_GET = request.GET
		request_POST = request.POST
		_request_type = request_GET.get("request_type", request_POST.get("request_type", None))
		_page = request_GET.get("_page", '')
		_limit = request_GET.get("_limit", '')
		_sort = request_GET.get("_sort", None)
		_order = request_GET.get("_order", None)
		_q = request_GET.get("_q", None)
		_search = request_GET.get("_search", None)
		_id = request_GET.get(request_table_columns_id, request_POST.get(request_table_columns_id, None))
		_event = request_POST.get('event', None)

		request_filter_columns = []
		request_filter_dict = {}
		request_sort_columns = []
		request_limit_rows = []
		# print(dynamic_columns)
		# print('=====================================')
		# print(request_table_columns)

		def get_clear_val(val):
			if val.lower() == 'true':
				val = True
			elif val.lower() == 'false':
				val = False
			elif val.isnumeric():
				val = int(val)
			elif val.replace(',','.',1).replace('.','',1).isdigit():
				val = float(val.replace(',','.',1))
			else:
				val = f"'{val}'"
			return val

		def get_filter(values):
			name,condition,value = values
			if name.endswith('__'): name = name[0:len(name)-2]
			if condition != '':
				key = f"{name}__{condition}"
			else:
				key = f"{name}"
			return key, value

		class GroupConcat(Aggregate):
			function = 'GROUP_CONCAT'
			template = '%(function)s(%(expressions)s)'

			def __init__(self, expression, delimiter, **extra):
				output_field = extra.pop('output_field', CharField())
				delimiter = Value(delimiter)
				super(GroupConcat, self).__init__(
					expression, delimiter, output_field=output_field, **extra)

			def as_postgresql(self, compiler, connection):
				self.function = 'STRING_AGG'
				return super(GroupConcat, self).as_sql(compiler, connection)


		# processing request dynamic grid events
		if _event == 'add':
			tmp_add_row_default = add_row_default.copy()
			m2m_list_of_dicts = []
			column_types = ContentType.objects.get(model=request_table_string).model_class()._meta.get_fields()
			for k,v in add_row_default.items():
				m2m = [i.name for i in column_types if i.name == k and i.__class__.__name__ == 'ManyToManyField']
				if len(m2m) > 0:
					tmp_add_row_default.pop(k, None)
					m2m_list_of_dicts.append({k:v})
			instance = dynamic_table.create(**tmp_add_row_default)
			#print(instance)
			#print(m2m_list_of_dicts)
			if instance and len(m2m_list_of_dicts) > 0:
				for col in m2m_list_of_dicts:
					for k,v in col.items():
						eval(f'instance.{k}.set(v)')

			return HttpResponse(status=200)

		if _event == 'edit' and _id is not None:
			COLS = ''
			update_query = f"request_table.objects.filter({request_table_columns_id}={_id})"
			for i in request_POST:
				if i in request_table_columns:
					val = request_POST.get(i, None)
					if val and val != '-':
						if '__' in i:
							fk_field_name = i[:i.index('__')]
							if ContentType.objects.get(model=request_table_string).model_class()._meta.get_field(fk_field_name).many_to_many:
								val = [int(i.replace(' ', '')) for i in val.split(',') if i != '']
								#print('ZZZZZZZZZZZZZZZZZZZZZZ', i, fk_field_name, val, 'VAL MUST ID !!!!!!!!!!!!')
								eval(f'{update_query}.first().{fk_field_name}.clear()')
								if val[0] != 0:
									eval(f'{update_query}.first().{fk_field_name}.add(*val)')
							else:
								field_name = i[i.index('__')+2:]
								obj = f"request_table.objects.filter({field_name}={get_clear_val(val)}).first()"
								upd = f"request_table.objects.filter({request_table_columns_id}={_id}).update({fk_field_name}={obj})"
								eval(upd)
						elif i != 'id':
							if ContentType.objects.get(model=request_table_string).model_class()._meta.get_field(i).many_to_many:
								val = [int(i.replace(' ', '')) for i in val.split(',') if i != '']
								eval(f'{update_query}.first().{i}.clear()')
								eval(f'{update_query}.first().{i}.add(*val)')
							else:
								COLS += f"{i}={get_clear_val(val)},"
					else:
						if '__' in i:
							pass
						elif i != 'id':
							if ContentType.objects.get(model=request_table_string).model_class()._meta.get_field(i).many_to_many:
								eval(f'{update_query}.first().{i}.clear()')
							else:
								eval(f'{update_query}.update({i}=None)')

			if COLS != '':
				update_query2 = update_query + ".update(COLS)".replace('COLS', COLS)
			eval(update_query2)
			update_query = eval(update_query+".first()")
			update_query.save()
			return HttpResponse(status=200)

		if _event == 'remove' and _id is not None:
			instance = ContentType.objects.get(model=request_table_string).model_class().objects.filter(**{request_table_columns_id: _id}).first()
			instance.delete()
			return HttpResponse(status=200)


		# init request dynamic grid: filter_columns, sort_columns, limit_rows
		for i in request_GET:
			ii = i
			if '__' in i: ii = i[:i.index('__')]

			if ii in dynamic_columns:
				request_filter_columns.append(i)
				v = re.sub('\s+',' ',request_GET.get(i, None)).rsplit(' ')
				request_filter_dict[i] = v
			if i == '_sort':
				v = request_GET.get(i, None).split(',')
				v2 = _order.split(',')
				if len(v) == len(v2):
					for idx, kk in enumerate(v):
						vv = v2[idx]
						if '__' in kk: kk = kk[:kk.index('__')]
						if kk in dynamic_columns:  
							if not ContentType.objects.get(model=request_table_string).model_class()._meta.get_field(kk).many_to_many:
								if vv == 'desc': kk = '-'+kk
								request_sort_columns.append(kk)
			if i == '_limit':
				v = request_GET.get(i, None)
				v2 = _page
				if v.isnumeric() and v2.isnumeric():
					v = int(v)
					v2 = int(v2)
					if v >= 0 and v2 >=	0:
						if v == 0: v = request_table_max_limit_rows
						request_limit_rows.append(0)
						if v < request_table_max_limit_rows:
							request_limit_rows.append(v)
						else:
							request_limit_rows.append(request_table_max_limit_rows)
		if _q:
			request_filter_dict = {}
			request_filter_columns = request_table_columns
			for i in request_filter_columns:
				v = re.sub('\s+',' ',_q).rsplit(' ')
				request_filter_dict[i] = v


		# processing request dynamic grid: filter_columns, sort_columns, limit_rows
		if _request_type == 'datagrid':
			filters = dict(map(get_filter,request_table_filters))
			table_list = dynamic_table.filter(**filters)
			excludes = dict(map(get_filter,request_table_excludes))
			table_list = table_list.exclude(**excludes)

			if len(request_sort_columns) > 0: table_list = table_list.order_by(*request_sort_columns)

			if len(request_filter_columns) > 0:
				case_4 = Q()
				for k,v in request_filter_dict.items():
					kk = k
					if '__' in kk: kk = kk[:kk.index('__')]
					if ContentType.objects.get(model=request_table_string).model_class()._meta.get_field(kk).many_to_many:
						case_1 = {f'{k}_toString': GroupConcat(kk, ',')}
					else:
						case_1 = {f'{k}_toString': Cast(k, CharField())}
					case_2 = {f'{k}_toString_lower': Lower(f'{k}_toString')}
					table_list = table_list.annotate(**case_1).annotate(**case_2)
					if len(request_filter_columns) == len(request_table_columns):
						case_4.add(Q(**{f'{k}_toString_lower__iregex': r'(' + '|'.join(v) + ')'}), Q.OR)
					else:
						case_3 = {f'{k}_toString_lower__iregex': r'(' + '|'.join(v) + ')'}
						table_list = table_list.filter(**case_3)
				if len(request_filter_columns) == len(request_table_columns):
					table_list = table_list.filter(case_4)


			tmp_table_list = []
			for i in table_list:
				row = {}
				for col_name in request_table_columns:
					col_val = ''
					root_col_name = col_name
					if '__' in col_name: root_col_name = col_name[:col_name.index('__')]
					m2m_exists_check = type(eval(f'i.{root_col_name}')).__name__
					if m2m_exists_check  == 'ManyRelatedManager':
						if '__' in col_name:
							col_name_tmp = col_name[col_name.index('__')+2:]
							col_val = eval(f'i.{root_col_name}')
							m2m_list_of_dicts = []
							for z in col_val.all():
								v = eval(f'z.{col_name_tmp}')
								if v == '' or v is None: v = '-'
								m2m_list_of_dicts.append({'id': z.id, col_name_tmp: request_table_secure_values_hide_func(v)})
							col_val = m2m_list_of_dicts
						else:
							col_val = eval(f'i.{col_name}')
							id_list = list(col_val.values_list('id', flat=True))
							m2m_list_of_dicts = []

							for j in id_list:
								m2m_list_of_dicts.append({'id': j})
							col_val = m2m_list_of_dicts
						if col_val == []: col_val = '-'
					else:
						if '__' in col_name:
							col_name = col_name.replace('__', '.')
							isNone = eval(f'i.{root_col_name}')
							if isNone != None: col_val = request_table_secure_values_hide_func(eval(f'i.{col_name}'))
							col_name = col_name.replace('.', '__')
						else:
							col_val = request_table_secure_values_hide_func(eval(f'i.{col_name}'))

					if col_val is None or col_val == '': col_val = '-'
					row[col_name] = col_val

				tmp_table_list.append(row)

			table_list = tmp_table_list[request_limit_rows[0]:request_limit_rows[1]]

			return JsonResponse({'table_data': table_list}, content_type="application/json", json_dumps_params={'ensure_ascii':False}, status = 200)

	except Exception as e:
		print('dynamic grid error: ', str(e))
		return 'dynamic grid error'   	


