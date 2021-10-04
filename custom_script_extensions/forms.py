from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User, Group, Permission, ContentType
from django.db.models import Case, Value, When
from django.db.models.functions import Concat
from django.db.models import CharField
from django.contrib.admin.widgets import FilteredSelectMultiple
from apps.app_zs_admin.models import app, aside_left_menu_includes, notification_events
from apps.accounts.models import user_extra_details
from easy_select2 import Select2Multiple, Select2
from django.utils.safestring import mark_safe
from ckeditor.widgets import CKEditorWidget
 

# UTIL FUNCTIONS ##################################
def user_groups_update(user, role, add=False):
	groups = []
	if role == 'can_access_dashboards':
		groups = ['app_zs_admin_viewer_group', 'app_opensource_dashboards_viewer_group', 'app_zs_dashboards_viewer_group']
	if role == 'can_edit_dashboards':
		groups = ['app_opensource_dashboards_editor_group', 'app_zs_dashboards_editor_group', 'app_opensource_dashboards_creator_group', 'app_zs_dashboards_creator_group']
	if role == 'can_edit_users_access':
		groups = ['app_zs_admin_editor_group']

	for g in groups:
		group = Group.objects.get(name=g)
		if add == True:
			user.groups.add(group)
		if add == False:
			user.groups.remove(group)
		user.save()

def user_groups_check(user, role):
	check = True
	groups = []
	if role == 'can_access_dashboards':
		groups = ['app_zs_admin_viewer_group', 'app_opensource_dashboards_viewer_group', 'app_zs_dashboards_viewer_group']
	if role == 'can_edit_dashboards':
		groups = ['app_opensource_dashboards_editor_group', 'app_zs_dashboards_editor_group']
	if role == 'can_edit_users_access':
		groups = ['app_zs_admin_editor_group']

	for g in groups:
		check = user.groups.filter(name=g).exists()
		if check == False: break

	return check


# FORMS ################################################
class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
    	super(SignUpForm, self).__init__(*args, **kwargs)


class UserZsAdminForm(forms.ModelForm):
	the_user = forms.ChoiceField(
		choices=(),
		label=u"UserZsAdminForm",
		widget=Select2(select2attrs={'width': '100%'}))
	can_access_dashboards = forms.BooleanField(
		label=u"доступ к разделу: дашборды (просмотр)",
		required=False, 
		initial=False,
		widget=forms.CheckboxInput(attrs={
            'id': 'CheckboxInput_can_access_dashboards'
        }),)
	can_edit_dashboards = forms.BooleanField(
		label=u"доступ к разделу: дашборды (редактирование)",
		required=False, 
		initial=False,
		widget=forms.CheckboxInput(attrs={
            'id': 'CheckboxInput_can_edit_dashboards'
        }),)
	can_edit_users_access = forms.BooleanField(
		label=u"доступ к разделу: настройки > администрирование > пользователи (редактирование)",
		required=False, 
		initial=False,
		widget=forms.CheckboxInput(attrs={
            'id': 'CheckboxInput_can_edit_users_access'
        }),)
	user_is_active = forms.BooleanField(
		label=u"доступ к сайту",
		required=False, 
		initial=False,
		widget=forms.CheckboxInput(attrs={
            'id': 'CheckboxInput_user_is_active'
        }),)


	class Meta:
		model = user_extra_details
		fields = ('the_user', 'can_access_dashboards', 'can_edit_dashboards', 'can_edit_users_access', 'user_is_active', )
	
	class Media:
		css = {
			'all': [],
		}
		js = []


	def get_form_kwargs(self):
		kwargs = super(UserZsAdminForm, self).get_form_kwargs()
		if self.request.method in ('POST', 'PUT'):
			kwargs.update({
				'data': self.request.POST,
				'files': self.request.FILES,
				})
		elif self.request.method in ('GET'):
			kwargs.update({'get_data': self.request.GET})

		return kwargs


	def __init__(self, *args, **kwargs):
		super(UserZsAdminForm, self).__init__(*args,**kwargs)
		selected_the_user = args[0].get('user_id', None)

		self.fields['the_user'].choices = [(c, c) for c in user_extra_details.objects.filter(user__is_staff=False
			).exclude(user__username__startswith='TEST_USER'
			).annotate(full_names=Case(When(full_name__exact='', then=Value('н/д')), When(full_name__isnull=False, then='full_name'), default=None, output_field=CharField())
			).annotate(full_names2=Concat('user__id', Value(' | '), 'user__username', Value(' | '), 'full_names', Value(' | '), 'department', Value(' | '), 'center', Value(' | '), 'position', output_field=CharField())
			).values_list('full_names2', flat=True)]
			
		if selected_the_user and selected_the_user != '-' and selected_the_user.isnumeric():
			u = User.objects.filter(id=selected_the_user).first()
			if u:
				sorted_choices = []
				selected_choice = None
				for i in self.fields['the_user'].choices:
					if selected_the_user != i[0].rsplit('|')[0].replace(' ', ''):
						sorted_choices.append(i)
					else:
						selected_choice = i
				if selected_choice:
					self.fields['the_user'].choices = [selected_choice] + sorted_choices + [('-','не выбрано')] 
				else:
					self.fields['the_user'].choices = [('-','не выбрано')] + self.fields['the_user'].choices
					self.fields['can_access_dashboards'].widget = forms.HiddenInput()
					self.fields['can_edit_dashboards'].widget = forms.HiddenInput()
					self.fields['can_edit_users_access'].widget = forms.HiddenInput()
					self.fields['user_is_active'].widget = forms.HiddenInput()

				if user_groups_check(u, 'can_access_dashboards'):
					self.fields['can_access_dashboards'].widget.attrs['checked'] = 'checked'

				if user_groups_check(u, 'can_edit_dashboards'):
					self.fields['can_edit_dashboards'].widget.attrs['checked'] = 'checked'

				if user_groups_check(u, 'can_edit_users_access'):
					self.fields['can_edit_users_access'].widget.attrs['checked'] = 'checked'

				if u.is_active:
					self.fields['user_is_active'].widget.attrs['checked'] = 'checked'
			else:
				self.fields['the_user'].choices = [('-','не выбрано')] + self.fields['the_user'].choices
				self.fields['can_access_dashboards'].widget = forms.HiddenInput()
				self.fields['can_edit_dashboards'].widget = forms.HiddenInput()
				self.fields['can_edit_users_access'].widget = forms.HiddenInput()
				self.fields['user_is_active'].widget = forms.HiddenInput()
		else:
			self.fields['the_user'].choices = [('-','не выбрано')] + self.fields['the_user'].choices
			self.fields['can_access_dashboards'].widget = forms.HiddenInput()
			self.fields['can_edit_dashboards'].widget = forms.HiddenInput()
			self.fields['can_edit_users_access'].widget = forms.HiddenInput()
			self.fields['user_is_active'].widget = forms.HiddenInput()

		self.onchange_the_user = mark_safe("""
			<script>
			$(document.body).on("change","#id_COLUMN_EVENT_NAME_1",function(){
				location.href = location.protocol + '//' + location.host + location.pathname + '?user_id=' + $('#select2-id_the_user-container')[0].title.split(' | ')[0];
			});
			function hide_submit_input_for_None_selection() {
				if ($('.select2-selection__rendered').text() === 'не выбрано') {
					$('#form-app fieldset > input').addClass('displayNone');
				} else {
					$('#form-app fieldset > input').removeClass('displayNone');
				}
			}
			setTimeout(hide_submit_input_for_None_selection, 200);
			function select2_get_formatted_choice_menu(is_onclick) {
				if (!$('.select2-container ul li').eq(0).find('.row-part-header').text().includes('id')) {
					let li_items = $('.select2-container ul li');
					for (i=0; i < li_items.length; i++) {
						let li_item = li_items.eq(i);
						let count_parts = li_item.text().split('|');
						let row_headers = ['id:', 'учётная запись:', 'ФИО:', 'Департамент:', 'Центр:', 'Должность:'];
						let textParts = [];
						for (var n = 0; n < count_parts.length; n++) {
							if(count_parts[n].trim() !== "") {
								textParts.push('<div class="row-part"><div class="row-part-header">' + row_headers[n] + '</div><div class="row-part-text">' + count_parts[n].trim() + '</div></div>')
							}
						}

						li_items.eq(i).text('');
						let formatted_lines = '';
						for (var j = 0; j < textParts.length; j++) {
							formatted_lines += textParts[j]
						}
						li_items.eq(i).html(formatted_lines)
					}
				}
			};
			function click_select2_choice_menu() { 
				let selected_text = $('#select2-id_the_user-container').text();
				selected_text = selected_text.replace('|  |', '').replace('|  |', '').replace('|  |', '').replace('|  |', '')
				$('#select2-id_the_user-container').text(selected_text);
				$('.select2-selection__rendered').off('click').click(function(){

				select2_get_formatted_choice_menu();
					if(('.select2-container').length > 0) {
						$(".select2-search input[type='search']").off('change').off('keydown').off('paste').off('input').on('change keydown paste input', function(){
							select2_get_formatted_choice_menu();
							setTimeout(select2_get_formatted_choice_menu, 100);
						});
					}
				})
			};
			setTimeout(click_select2_choice_menu, 200);
			function removeAlertContainer() {
				$('.user-creation-alert-container').remove();
				$('.user-creation-button').removeClass('displayNone');
			}
			function create_new_user(_this, job_type) {
				if (job_type === 'init') {
					if ($(_this).text() === '+') {
						$(_this).text('-')
						$('#form-app fieldset .items-container > .form-items-group:not(:first-child)').fadeOut(0);
						$('#form-app fieldset .items-container > .form-items-group:first-child > .select2.select2-container').fadeOut(0);
						$('#form-app fieldset > input').fadeOut(0);
						$('#form-app fieldset .items-container > .form-items-group:first-child').prepend(`<div class="user-creation-container"><input type="text" id="username" name="username" pattern="[a-zA-Z0-9]+" required></div>`);
						$('#form-app fieldset').append(`<button type="button" onclick="create_new_user(this, 'create');" class="user-creation-button">Создать</button>`);
						$('#form-app fieldset > legend').text('создать пользователя');
						$('.user-creation-alert-container').remove();
					} else {
						$(_this).text('+')
						$('#form-app fieldset .items-container > .form-items-group:not(:first-child)').fadeIn(300);
						$('#form-app fieldset .items-container > .form-items-group:first-child > .select2.select2-container').fadeIn(300);
						$('#form-app fieldset > input').fadeIn(300);
						$('.user-creation-container').remove();
						$('.user-creation-button').remove();
						$('#form-app fieldset > legend').text('доступ');
						$('.user-creation-alert-container').remove();
					}
				}
				if (job_type === 'create') {
					if($('#username').val().length <= 3) {
						$('#form-app fieldset .items-container > .form-items-group:first-child').prepend(`<div class="user-creation-alert-container"><button type="button" onclick="removeAlertContainer();" class="creation-alert-confirm">OK</button></div>`);
						$('.user-creation-alert-container').prepend('<div>Минимальное значение букв >3 !</div>');
						$('.user-creation-button').addClass('displayNone');
					} else {
						if($('#username').val().match(/\W/)) {
							$('#form-app fieldset .items-container > .form-items-group:first-child').prepend(`<div class="user-creation-alert-container"><button type="button" onclick="removeAlertContainer();" class="creation-alert-confirm">OK</button></div>`);
							$('.user-creation-alert-container').prepend('<div>Только буквы и цифры допустимы!</div>');
							$('.user-creation-button').addClass('displayNone');
						} else {
							console.log('create', $('#username').val());
							let new_user = $('#username').val();
							let submit = window.location.origin + `/zs_admin/users_profile/create/${new_user}/`
							window.location = submit;
						}
					}
				}
			}
			function addCreateButton() {
				$('#form-app fieldset .items-container > .form-items-group:first-child').prepend(`<button type="button" onclick="create_new_user(this, 'init');" class="add-new-user-button" title="Создать учётную запись пользователя">+</button>`);
			}
			setTimeout(addCreateButton, 200);
			/*
			let checkbox2 = $('#UserZsAdminForm input#CheckboxInput_can_access_dashboards');
			let checkbox3 = $('#UserZsAdminForm input#CheckboxInput_can_edit_dashboards');
			let checkbox4 = $('#UserZsAdminForm input#CheckboxInput_can_edit_users_access');
			if(checkbox2) {
				if (checkbox2.prop('checked') === false) {
					$(checkbox3).parent().addClass('disabled');
					$(checkbox4).parent().addClass('disabled');
				}
			}
			$(document.body).on("change","#COLUMN_EVENT_NAME_2",function(){
				//console.log('CheckboxInput_can_access_dashboards');
				if (checkbox2.prop('checked') === true) {
					$(checkbox3).parent().removeClass('disabled');
					$(checkbox4).parent().removeClass('disabled');
				} else {
					$(checkbox3).parent().addClass('disabled');
					$(checkbox4).parent().addClass('disabled');
					$(checkbox3).prop('checked', false);
					$(checkbox4).prop('checked', false);
				}
			});
			$(document.body).on("change","#COLUMN_EVENT_NAME_3",function(){
				//console.log('CheckboxInput_can_edit_dashboards');
			});
			$(document.body).on("change","#COLUMN_EVENT_NAME_4",function(){
				//console.log('CheckboxInput_can_edit_users_access');
			});
			$(document.body).on("change","#COLUMN_EVENT_NAME_5",function(){
				//console.log('CheckboxInput_user_is_active');
			});
			*/
			</script>""".replace('FORM_EVENT_NAME', 'UserZsAdminForm'
				).replace('COLUMN_EVENT_NAME_1', 'the_user' 
				).replace('COLUMN_EVENT_NAME_2', 'CheckboxInput_can_access_dashboards'
				).replace('COLUMN_EVENT_NAME_3', 'CheckboxInput_can_edit_dashboards'
				).replace('COLUMN_EVENT_NAME_4', 'CheckboxInput_can_edit_users_access'
				).replace('COLUMN_EVENT_NAME_5', 'CheckboxInput_user_is_active'))

	def clean(self):
		cleaned_data = super(UserZsAdminForm, self).clean()
		clean_user = self.cleaned_data.get('the_user')
		if clean_user and clean_user != '-' and clean_user.isnumeric():
			self.cleaned_data['the_user'] = self.cleaned_data.get('the_user').rsplit('|')[0].replace(' ', '')
		else:
			self.cleaned_data['the_user'] = self.cleaned_data.get('the_user').rsplit('|')[0].replace(' ', '')


	def save(self, commit=False, *args, **kwargs):
		saved_data = super(UserZsAdminForm, self).save(commit=False, *args, **kwargs)
		if self.cleaned_data.get('the_user') != '-':
			u = User.objects.get(id=self.cleaned_data.get('the_user'))

			if self.cleaned_data.get('can_access_dashboards') == True:
				user_groups_update(u, 'can_access_dashboards', True)
			else:
				user_groups_update(u, 'can_access_dashboards', False)

			if self.cleaned_data.get('can_edit_dashboards') == True:
				user_groups_update( u, 'can_edit_dashboards',True)
			else:
				user_groups_update(u, 'can_edit_dashboards', False)

			if self.cleaned_data.get('can_edit_users_access') == True:
				user_groups_update(u, 'can_edit_users_access', True)
			else:
				user_groups_update(u, 'can_edit_users_access', False)

			if self.cleaned_data.get('user_is_active') == True:
				u.is_active = True
			else:
				u.is_active = False
			u.save()

		return saved_data



class custom_ModelMultipleChoiceField(forms.ModelMultipleChoiceField):
	def label_from_instance(self, obj):
		model_name = obj.__class__.__name__
		if model_name == 'aside_left_menu_includes':
			parent_name = ''
			# if obj.name:
			# 	if obj.parent_name:
			# 		parent_name = str(obj.parent_name.name) + ' | '
			if obj.source_app_name_translate:
				parent_name = str(obj.source_app_name_translate.name) + ' | ' 
			option_name = parent_name + obj.name
			if obj.menu_icon_type == 'arrow':
				option_name = 'Раздел меню | ' + obj.name
			return option_name
		if model_name == 'notification_events':
			pass
		return obj



class ContentpublicationsForm(forms.ModelForm):
	content_m2m = custom_ModelMultipleChoiceField(
		queryset=None,#aside_left_menu_includes.objects.filter(is_actual=True, menu_icon_type='folder', source_app_name_translate__name='Дашборды').all(),
		label = "ContentpublicationsForm",
		#choices = [i.id for i in app.objects.filter(is_actual=True).first().app_settings_container_aside_left_menu_items_includes.all() if i.menu_icon_type == 'folder'],
		widget=FilteredSelectMultiple(u"", is_stacked=False),
		required=False)

	class Meta:
		model = app
		fields = ('content_m2m', )
	
	class Media:
		css = {
			'all': [],
		}
		js = []

	def __init__(self, *args, **kwargs):
		super(ContentpublicationsForm, self).__init__(*args, **kwargs)
		selected_items = app.objects.filter(is_actual=True).first().app_settings_container_aside_left_menu_items_includes.filter(is_actual=True, menu_icon_type__in=['folder', 'arrow'], source_app_name_translate__name='Дашборды').all()
		selected_ids_list = list(selected_items.values_list('id', flat=True))
		all_items = aside_left_menu_includes.objects.filter(is_actual=True, menu_icon_type__in=['folder', 'arrow'], source_app_name_translate__name='Дашборды').all()
		self.fields['content_m2m'].queryset = all_items
		#self.fields['content_m2m'].queryset = all_items.exclude(id__in=selected_ids_list)
		#self.fields['content_m2m'].initial = all_items.filter(id__in=selected_ids_list)
		if self.instance: self.fields["content_m2m"].initial = (selected_ids_list)
		#№self.fields['content_m2m'].help_text = "Открыть доступ к контенту для пользователей."
		#self.fields['content_m2m'].label = "Выбрать контент"

	def save(self, commit=False, *args, **kwargs):
		app__container_aside_left_menu_items_includes = super(ContentpublicationsForm, self).save(commit=False, *args, **kwargs)

		current_items = app.objects.filter(is_actual=True).first().app_settings_container_aside_left_menu_items_includes.filter(is_actual=True, menu_icon_type__in=['folder', 'arrow'], source_app_name_translate__name='Дашборды').all()
		current_items_ids_list = list(current_items.values_list('id', flat=True))
		
		selected_items_ids_list = []
		for val in self.cleaned_data.get('content_m2m'):
			selected_items_ids_list.append(val.id)

		remove_items_ids_list = aside_left_menu_includes.objects.filter(is_actual=True, menu_icon_type__in=['folder', 'arrow'], source_app_name_translate__name='Дашборды', id__in=[i for i in current_items_ids_list if i not in selected_items_ids_list]).all()
		add_items_ids_list = aside_left_menu_includes.objects.filter(is_actual=True, menu_icon_type__in=['folder', 'arrow'], source_app_name_translate__name='Дашборды', id__in=[i for i in selected_items_ids_list if i not in current_items_ids_list]).all()


		app.objects.filter(is_actual=True).first().app_settings_container_aside_left_menu_items_includes.remove(*remove_items_ids_list)
		app.objects.filter(is_actual=True).first().app_settings_container_aside_left_menu_items_includes.add(*add_items_ids_list)

		return app__container_aside_left_menu_items_includes



class notificationCreationForm(forms.ModelForm):
	title = forms.CharField(
		label=u"notificationCreationForm",
		max_length=254, 
		required=True)
	event_content = forms.CharField(
		label=u"Контент",
		required=False,
		widget=forms.Textarea)
	event_content2 = forms.CharField(
		label=u"Контент (расширенный формат)",
		required=False,
		widget=CKEditorWidget()
		)
	content_m2m = custom_ModelMultipleChoiceField(
		queryset=User.objects.filter(is_active=True).all(),
		label=u"Пользователи",
		widget=FilteredSelectMultiple(u"", is_stacked=False),
		required=False)
	is_actual = forms.BooleanField(
		label=u"Опубликовать",
		required=False, 
		initial=False,
		widget=forms.CheckboxInput(attrs={
            'id': 'CheckboxInput_is_actual'
        }),)

	class Meta:
		model = notification_events
		fields = ('title', 'event_content', 'event_content2', 'content_m2m', 'is_actual', )
	
	class Media:
		css = {
			'all': [],
		}
		js = []


	def __init__(self, *args, **kwargs):
		super(notificationCreationForm, self).__init__(*args, **kwargs)

	def save(self, commit=False, *args, **kwargs):
		form_obj = super(notificationCreationForm, self).save(commit=False, *args, **kwargs)
		print(self.cleaned_data.get('content_m2m'))
		obj = notification_events(
			title=form_obj.title,
			event_content=form_obj.event_content,
			event_content2=form_obj.event_content2,
			is_actual=form_obj.is_actual
			)
		obj.save()
		obj.users_list.clear()
		obj.users_list.add(*self.cleaned_data.get('content_m2m'))
		obj.save()


		return form_obj
