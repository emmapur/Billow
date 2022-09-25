from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView
from . import forms
from django.views.generic import TemplateView

# Create your views here.
class Login(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/login.html"

class ProjectPage(TemplateView):
    template_name = 'create_project.html'
