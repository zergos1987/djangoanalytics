from functools import wraps
from django.http import HttpResponse, FileResponse, Http404, HttpResponseRedirect, HttpResponseForbidden, HttpResponsePermanentRedirect
from django.core.exceptions import PermissionDenied

def user_group_access_check(*groups):
    def inner(view_func):
        @wraps(view_func)
        def wrapper_func(request, *args, **kwargs):
            if request.user.groups.filter(name__in=groups).exists():
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied()#HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return inner
