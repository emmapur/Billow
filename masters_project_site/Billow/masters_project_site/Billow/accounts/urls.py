from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls import url, include

app_name = 'accounts'

urlpatterns = [
    url(r'^login/$', auth_views.LoginView.as_view(template_name="accounts/login.html"),name='login'), #default view
    url(r'^logout/$', auth_views.LogoutView.as_view(), name="logout"),
    url(r'^create_project/$', views.ProjectPage.as_view(), name='create_project'),


    #url(r'^create_project/$', views.create_project, name='create_project')

]
