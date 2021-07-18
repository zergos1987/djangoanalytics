from django.template import Library
from custom_script_extensions.custom_permissions_check import check_user_content_request_permission

register = Library()

@register.filter()
def is_false(arg): 
    return arg is False

@register.filter()
def to_int(value):
    value = float(value)
    return int(value)

@register.filter()
def get_item(dictionary, key):
    val = key
    return val

@register.filter()
def to_upper(value):
    value = value.upper()
    return value

@register.simple_tag
def check_url_permission(content_obj, check_perm_type, menu_type, obj_id, user_id):
	if check_perm_type == 'has_item_perm':
		user_content_has_permission = check_user_content_request_permission(
			content_obj=content_obj,
			obj_id=obj_id,
			user_id=user_id)
	if check_perm_type == 'has_menu_perm':
		print(menu_type, 'QQQQQQQQQQ')
		user_content_has_permission = False
	return user_content_has_permission