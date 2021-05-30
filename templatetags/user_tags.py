from django
from django import template
import six

from django.core.exceptions import PermissinonDenied
from django.contrib.auth.decorators import user_passes_test

register = template.Library()

@register.filter('in_group')
def in_group(user, group_name):
	return user.groups.filter(name=group_name).exists()

@register.filter('group_required')
def group_required(group, raise_exception=False):
	def check_perms(user):
		if isinstance(group, six.string_types):
			groups = (group, )
		else:
			groups = group

		if user.groups.filter(name__in=groups).exists():
			return True

		if raise_exception:
			raise PermissinonDenied

		return False
	return user_passes_test(check_perms)