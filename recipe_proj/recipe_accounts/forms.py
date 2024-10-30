from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CreateUserForm(UserCreationForm):
	email = forms.EmailField(required=True)
	first_name = forms.CharField(max_length=150)
	last_name = forms.CharField(max_length=150)
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']