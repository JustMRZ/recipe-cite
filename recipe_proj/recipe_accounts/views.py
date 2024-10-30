from django.shortcuts import render
from django.views.generic import CreateView
from recipe_accounts.forms import CreateUserForm
from django.urls import reverse_lazy

# Create your views here.


class CreateUserView(CreateView):
	"""
	Классовое представление регистрации пользователя
	"""
	form_class = CreateUserForm
	success_url = reverse_lazy('login')
	template_name = 'registration/singup.html'