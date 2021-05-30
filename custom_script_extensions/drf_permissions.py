from rest_framework.permissions import BasePermission

class CheckGroupPermissions(BasePermission):
	def has_permission(self, request, view):
		if request.user.groups.filter(name='examples_app__genericTable__drf__get').exists() and request.method in ['GET', 'OPTIONS']:
			return True
		elif request.user.groups.filter(name='examples_app__genericTable__drf__post').exists() and request.method in ['POST']:
			return True
		elif request.user.groups.filter(name='examples_app__genericTable__drf__put').exists() and request.method in ['PUT', 'UPDATE']:
			return True
		elif request.user.groups.filter(name='examples_app__genericTable__drf__delete').exists() and request.method in ['DELETE']:
			return True
		return False