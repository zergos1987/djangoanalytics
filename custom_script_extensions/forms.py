from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.admin.widgets import FilteredSelectMultiple
from apps.app_zs_admin.models import app, aside_left_menu_includes
from easy_select2 import Select2Multiple



class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
    	super(SignUpForm, self).__init__(*args, **kwargs)



class UserZsAdminForm(forms.Form):
	username = forms.ModelMultipleChoiceField(
		queryset=User.objects.filter(is_staff=False).exclude(username__startswith='TEST_USER'), 
		label=u"UserZsAdminForm",
		widget=Select2Multiple(select2attrs={'width': 'auto'}))
	# username = forms.ModelMultipleChoiceField(
	# 	label=u"UserZsAdminForm",
	# 	queryset=User.objects.filter(is_staff=False).exclude(username__startswith='TEST_USER'),)
	can_access_dashboards = forms.BooleanField(
		label=u"доступ к разделу - дашборды (просмотр)",
		required=False, 
		initial=False)
	can_edit_dashboards = forms.BooleanField(
		label=u"доступ к разделу - дашборды (редактирование)",
		required=False, 
		initial=False)
	can_edit_users_access = forms.BooleanField(
		label=u"доступ к разделу - пользователи (редактирование)",
		required=False, 
		initial=False)

	class Meta:
		model = User
		fields = ('username', 'can_access_dashboards', 'can_edit_dashboards', 'can_edit_users_access',)
	
	class Media:
		css = {
			'all': [],
		}
		js = []



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
			return option_name
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
		selected_items = app.objects.filter(is_actual=True).first().app_settings_container_aside_left_menu_items_includes.filter(is_actual=True, menu_icon_type='folder', source_app_name_translate__name='Дашборды').all()
		selected_ids_list = list(selected_items.values_list('id', flat=True))
		all_items = aside_left_menu_includes.objects.filter(is_actual=True, menu_icon_type='folder', source_app_name_translate__name='Дашборды').all()
		self.fields['content_m2m'].queryset = all_items
		#self.fields['content_m2m'].queryset = all_items.exclude(id__in=selected_ids_list)
		#self.fields['content_m2m'].initial = all_items.filter(id__in=selected_ids_list)
		if self.instance: self.fields["content_m2m"].initial = (selected_ids_list)
		#print(self.fields['content_m2m'].initial, 'QQQQQQQQQQQQQQQQQQQQQQQQQQ')
		#№self.fields['content_m2m'].help_text = "Открыть доступ к контенту для пользователей."
		#self.fields['content_m2m'].label = "Выбрать контент"

	def save(self, commit=False, *args, **kwargs):
		app__container_aside_left_menu_items_includes = super(ContentpublicationsForm, self).save(commit=False, *args, **kwargs)

		current_items = app.objects.filter(is_actual=True).first().app_settings_container_aside_left_menu_items_includes.filter(is_actual=True, menu_icon_type='folder', source_app_name_translate__name='Дашборды').all()
		current_items_ids_list = list(current_items.values_list('id', flat=True))
		
		selected_items_ids_list = []
		for val in self.cleaned_data.get('content_m2m'):
			selected_items_ids_list.append(val.id)

		remove_items_ids_list = aside_left_menu_includes.objects.filter(is_actual=True, menu_icon_type='folder', source_app_name_translate__name='Дашборды', id__in=[i for i in current_items_ids_list if i not in selected_items_ids_list]).all()
		add_items_ids_list = aside_left_menu_includes.objects.filter(is_actual=True, menu_icon_type='folder', source_app_name_translate__name='Дашборды', id__in=[i for i in selected_items_ids_list if i not in current_items_ids_list]).all()

		# print(current_items_ids_list)
		# print(selected_items_ids_list)
		# print(remove_items_ids_list)
		# print(add_items_ids_list)

		app.objects.filter(is_actual=True).first().app_settings_container_aside_left_menu_items_includes.remove(*remove_items_ids_list)
		app.objects.filter(is_actual=True).first().app_settings_container_aside_left_menu_items_includes.add(*add_items_ids_list)

		return app__container_aside_left_menu_items_includes
