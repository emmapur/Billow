from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView
from . import forms
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, Http404, HttpResponseRedirect, \
    JsonResponse, StreamingHttpResponse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404, reverse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .Cloud_utils import*
# Create your views here.
class Login(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/login.html"

@csrf_exempt
def create_new_instance_form(request):
    cloud_providers_list = Cloud_Provider.objects.all()
    flavor_list = Flavor.objects.all()
    ImageID_list = Image.objects.all()
    KeyName_list = Key.objects.all()
    instance_name_list = Instance.objects.all()
    team_name_list = Team.objects.all()
    program_name_list = Program.objects.all()
    users_list = User.objects.all()


    context = {
        'cloud_providers_list' : cloud_providers_list,
        'flavor_list': flavor_list,
        'ImageID_list': ImageID_list,
        'KeyName_list': KeyName_list,
        'instance_name': instance_name_list,
        'team_name_list' : team_name_list,
        'program_name_list' : program_name_list,
        'users_list' : users_list

    }

    print(request.POST)
    return render(request, 'create_instance_form.html', context)
@csrf_exempt
def create_new_instance(request):

    cloud_provider = request.POST.get('cloud_prov_name')
    flavor = request.POST.get('flavor_name')
    Image  = request.POST.get('Image_name')
    KeyName = request.POST.get('key_name')
    instance_name = request.POST.get('instance_name')
    team = request.POST.get('team_name')
    program  = request.POST.get('program_name')
    contact = request.POST.get('contact_name')
    users = request.POST.get('username')

    params = {
        'cloud_provider':cloud_provider,
        'aws_instance_type':flavor,
        'aws_image_id':Image,
        'aws_key_name':KeyName,
        'instance_name':instance_name,
        'team':team,
        'program':program,
        'users':users,
        'contact':contact
    }

    create_aws_instance(params)

    Instance_object = Instance(
        cloud_provider= cloud_provider,
        flavor=flavor,
        Image=Image,
        KeyName=KeyName,
        instance_name=instance_name,
        team=team,
        program=program,
        users=users,
        contact=contact
        )
    Instance_object.save()
    return render(request, 'create_instance_form.html', params)
