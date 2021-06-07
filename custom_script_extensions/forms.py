from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
    	super(SignUpForm, self).__init__(*args, **kwargs)

    	for fieldname in ['username', 'email', 'password1', 'password2']:
    		self.fields[fieldname].help_text = self.fields[fieldname].help_text.replace(
    			"Your password can’t be too similar to your other personal information.", 
    			"Ваш пароль не должен быть схожим с другой персональной информацией.").replace(
    			"Your password can’t be a commonly used password.",
    			"Ваш пароль не должен быть распространенным.").replace(
    			"Your password can’t be entirely numeric.",
    			"Ваш пароль не может состоять только из цифр.")
