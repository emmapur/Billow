from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls import include

app_name = 'accounts'

urlpatterns = [
    re_path(r'^login/$', auth_views.LoginView.as_view(template_name="accounts/login.html"),name='login'), #default view
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name="logout"),
    re_path(r'^create_instance_form/$', views.create_new_instance_form, name='create_instance_form'),
    re_path(r'^create_new_instance/$', views.create_new_instance, name='create_new_instance')

    #url(r'^create_project/$', views.create_project, name='create_project')

]
