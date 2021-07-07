from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, reverse
from custom_script_extensions.forms import SignUpForm
from custom_script_extensions.form_tags import *
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.utils.decorators import method_decorator

# Create your views here.
#@method_decorator([login_required, permission_required("accounts.view_app")], name="dispatch")
@login_required
@permission_required('accounts.view_app')
def index(request):

	template = 'accounts/index.html'

	return render(request, template)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            #user.user_extra_details.email_signup_confirmed = True
            user.save()
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def signout(request):
    logout(request)
    return redirect(reverse('admin:index')) # or wherever you want
