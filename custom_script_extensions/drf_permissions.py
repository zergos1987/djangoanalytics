from rest_framework.permissions import BasePermission


class CheckGroupPermissions__dynamic__ORM(BasePermission):
	def has_permission(self, request, view):
		if request.user.groups.filter(name='app_zs_examples__genericTable__drf__get').exists() and request.method in ['GET', 'OPTIONS']:
			return True
		elif request.user.groups.filter(name='app_zs_examples__genericTable__drf__post').exists() and request.method in ['POST']:
			return True
		elif request.user.groups.filter(name='app_zs_examples__genericTable__drf__put').exists() and request.method in ['PUT', 'UPDATE']:
			return True
		elif request.user.groups.filter(name='app_zs_examples__genericTable__drf__delete').exists() and request.method in ['DELETE']:
			return True
		elif request.user.groups.filter(name='app_zs_examples__genericTable__drf__export').exists() and request.method in ['GET']:
			return True
		elif request.user.groups.filter(name='app_zs_examples__genericTable__drf__import').exists() and request.method in ['POST']:
			return True
		return False


class CheckGroupPermissions__ORM(BasePermission):
	def has_permission(self, request, view):
		user_model_name = view.__class__.__name__
		user_model_name = user_model_name[:user_model_name.find('__')]
		if request.user.groups.filter(name=f'app_zs_examples__{user_model_name}__drf__get').exists() and request.method in ['GET', 'OPTIONS']:
			return True
		elif request.user.groups.filter(name=f'app_zs_examples__{user_model_name}__drf__post').exists() and request.method in ['POST']:
			return True
		elif request.user.groups.filter(name=f'app_zs_examples__{user_model_name}__drf__put').exists() and request.method in ['PUT', 'UPDATE']:
			return True
		elif request.user.groups.filter(name=f'app_zs_examples__{user_model_name}__drf__delete').exists() and request.method in ['DELETE']:
			return True
		elif request.user.groups.filter(name=f'app_zs_examples__{user_model_name}__drf__export').exists() and request.method in ['GET']:
			return True
		elif request.user.groups.filter(name=f'app_zs_examples__{user_model_name}__drf__import').exists() and request.method in ['POST']:
			return True
		return False
