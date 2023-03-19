from django.urls import re_path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    re_path(r'^login/$', auth_views.LoginView.as_view(template_name="accounts/login.html"),name='login'), #default view
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name="logout"),
    re_path(r'^create_instance_form/$', views.create_new_instance_form, name='create_instance_form'),
    re_path(r'^create_new_instance/$', views.create_new_instance, name='create_new_instance'),
    re_path(r'^billing/$', views.create_bill_form, name='billing'),
    re_path(r'^create_bill/$', views.create_bill, name='create_bill'), 
    re_path(r'^created_bill/$', views.create_bill, name='create_bill'),
    re_path(r'^instance_list/$', views.instance_list, name='instance_list'),
    re_path(r'^instance_details/$', views.instance_details, name='instance_details'),
    re_path(r'^instance_actions/$', views.instance_actions, name='instance_actions'),
    re_path(r'sync-state/$', views.sync_state_view, name='sync_state_view'),

    

 
  
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


