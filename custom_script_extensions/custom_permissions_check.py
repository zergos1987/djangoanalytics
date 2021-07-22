def check_user_content_request_permission(content_obj, obj_id, user_id, menu_type=None):
	from django.contrib.auth.models import User

	content_access = False

	required_user_check = []
	required_groups_check = []
	user_matches = []
	groups_matches = []

	user = User.objects.get(id=user_id)
	if content_obj == 'aside_left_menu_includes':
		from apps.app_zs_admin.models import aside_left_menu_includes
		if menu_type == 'settings':
			obj_items = aside_left_menu_includes.objects.filter(
				name__in=['Приложения'], 
				menu_level='level-1')
			for obj in obj_items:
				obj_id = obj.id
				content_access = check_user_content_request_permission(content_obj, obj_id, user_id, menu_type=None)
				if content_access: break
			return content_access
		if menu_type == 'dashboards':
			obj_items = aside_left_menu_includes.objects.filter(
				menu_level='level-1').exclude(
				name__in=['Приложения'])
			for obj in obj_items:
				obj_id = obj.id
				content_access = check_user_content_request_permission(content_obj, obj_id, user_id, menu_type=None)
				if content_access: break
			return content_access
		user_selected_content = aside_left_menu_includes.objects.get(id=obj_id)
		required_user_check = user_selected_content.url_access_via_users.all()
		required_groups_check = user_selected_content.url_access_via_groups.all()


	if len(required_user_check) > 0:
		user_matches = [val for val in required_user_check if val.username in [user.username]]
		if len(user_matches) > 0:
			content_access = True
	if len(required_groups_check) > 0:
		groups_matches = [val for val in required_groups_check if val in user.groups.all()]
		if len(groups_matches) > 0:
			content_access = True

	if len(required_user_check) == 0 and len(required_groups_check) == 0:
		content_access = True

	#print(required_user_check, required_groups_check, '00000000000000', len(required_user_check), len(required_groups_check))
	#print(user_matches, groups_matches, '111111111111111', len(user_matches), len(groups_matches))

	return content_access