from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from custom_script_extensions.forms import SignUpForm
from custom_script_extensions.tokens import account_activation_token
from custom_script_extensions.form_tags import *
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.utils.decorators import method_decorator
from apps.accounts.models import user_extra_details

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
        # if form.is_valid():
        #     user = form.save()
        #     user_details = user_extra_details.objects.filter(user__username=user.username).first()
        #     user_details.email_signup_confirmed = True
        #     user_details.save()
        #     user.save()
        #     auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        #     return redirect('/')
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # user_details = user_extra_details.objects.filter(user__username=user.username).first()
            # user_details.email_signup_confirmed = False
            # user_details.save()
            # print(user_details, user.username, 'ZZZZZZZZZZZZZZZZZZZZ')

            current_site = get_current_site(request)
            subject = 'DjangoAnalytics. Account activation.'
            message = render_to_string('registration/accounts_activation_email_sent.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('accounts:activation_email_confirm')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})




def activation_email_confirm(request):
    template = 'registration/accounts_activation_email_confirm.html'

    return render(request, template)




def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('/')
    else:
        return render(request, 'registration/accounts_activation_email_invalid.html')




def signout(request):
    logout(request)
    return redirect(reverse('admin:index')) # or wherever you want
