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
from django.contrib import messages
from .decorators import users_allowed




# Create your views here.
class Login(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/login.html"


@csrf_exempt
def instance_list(request):
   
   
    team_name = UserProfile.objects.get(user_name = request.user).team_name
    program_name = UserProfile.objects.get(user_name = request.user).program_name



    allowed_roles = ['admin']
    program_roles = ['program_manager']

    if request.user.groups.exists():
        group = request.user.groups.all()[0].name

    if group in allowed_roles:
       context = {"columns": ['Cloud Provider', 'Program', 'Team', 'Flavor',
                               'CPU (Total)', 'RAM (GiB)',
                               'Storage (GiB)', 'State', 'Created At']}

       instance_list = Instance.objects.values('cloud_provider__cloud_prov_name', 'flavor__CPU', 'flavor__Ram', 'flavor__Storage', 'team__team_name', 'program__program_name', 'instance_name','flavor__flavor_name', 'launch_time')
       context['data'] = instance_list
    elif group in program_roles:
        context = {"columns": ['Cloud Provider', 'Program', 'Team', 'Flavor',
                               'CPU (Total)', 'RAM (GiB)',
                               'Storage (GiB)', 'State', 'Created At']}
        instance_list = Instance.objects.filter(program__program_name = program_name).values('cloud_provider__cloud_prov_name', 'flavor__CPU', 'flavor__Ram', 'flavor__Storage', 'team__team_name', 'program__program_name', 'instance_name','flavor__flavor_name', 'launch_time')
        context['data'] = instance_list
    else:
        context = {"columns": ['Cloud Provider', 'Program', 'Team', 'Flavor',
                               'CPU (Total)', 'RAM (GiB)',
                               'Storage (GiB)', 'State', 'Created At']}
        instance_list = Instance.objects.filter(team__team_name = team_name).values('cloud_provider__cloud_prov_name', 'flavor__CPU', 'flavor__Ram', 'flavor__Storage', 'team__team_name', 'program__program_name', 'instance_name','flavor__flavor_name', 'launch_time')
        context['data'] = instance_list

    #if group in program_roles = ['program1']

















    return render(request, 'instance_list.html', context)



@csrf_exempt
def instance_details(request):
    instance_name = request.GET.get('instance_details')

    context = {"columns": ['Instance Name', 'Cloud Provider', 'Program', 'Team', 'Flavor',
                               'CPU (Total)', 'RAM (GiB)',
                               'Storage (GiB)', 'State', 'Created At']}

    instance_list = Instance.objects.filter(instance_name=instance_name).values('id_instance', 'flavor__flavor_name', 'flavor__CPU', 'instance_name', 'users', 'contact', 'cloud_provider','team', 'program', 'instance_name','Image', 'KeyName')


    context={

        'data' : instance_list,
    }
    
    return render(request, 'instance_details.html', context)



@csrf_exempt
def delete_instance(request):
  
    cloud_provider = request.GET.get('cloud_prov_name')
    instance_id = request.GET.get('id_instance')

    
    print(cloud_provider)

    params = {
        'aws_instance_id':instance_id,
        'id_instance':instance_id
    }

    take_snapshot_instance()
    get_snapshots()


    if (cloud_provider == 'OpenStack'):
        delete_openstack_instance(params)
    else:
        delete_an_instance(params)

  #  delete_an_instance(params)

    return HttpResponseRedirect(reverse('accounts:instance_list'))




@csrf_exempt
@users_allowed(allowed_roles=['admin'])
def create_new_instance_form(request):
    cloud_providers_list = Cloud_Provider.objects.all()
    flavor_list = Flavor.objects.all()
    ImageID_list = Image.objects.all()
    KeyName_list = Key.objects.all()
    instance_name_list = Instance.objects.all()
    team_name_list = Team.objects.all()
    program_name_list = Program.objects.all()
    users_list = UserProfile.objects.all()

    Openstack_image_list = Openstack_image.objects.all()

    context = {
        'cloud_providers_list' : cloud_providers_list,
        'flavor_list': flavor_list,
        'ImageID_list': ImageID_list,
        'KeyName_list': KeyName_list,
        'instance_name': instance_name_list,
        'team_name_list' : team_name_list,
        'program_name_list' : program_name_list,
        'users_list' : users_list,
    
        'Openstack_image_list': Openstack_image_list,

    }

    #print(request.POST)
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
    users =  request.POST.get('username')
 
    Openstack_image = request.POST.get('Image_ID')
    flavor_name = request.POST.get('flavor_name') 
    flavor_id = Flavor.objects.values_list('id_flavor', flat=True).get(flavor_name=flavor_name)

 #   instance_list = Instance.objects.filter(instance_name=instance_name).values('id_instance', '
    
   

    params = {
        'cloud_provider':cloud_provider,
        'aws_instance_type':flavor,
        'aws_image_id':Image,
        'aws_key_name':KeyName,
        'instance_name':instance_name,
        'team':team,
        'program':program,
        'users':users,
        'contact':contact,
        'flavor':flavor_name,
        'Image': Image,
        'openstack_flavor_id' : flavor_id,
    
        'openstack_image_id' : Openstack_image
    }

  #  try:
    if (cloud_provider == 'OpenStack'):
             create_openstack_instance(params)
    else:
            create_aws_instance(params)


   # except Exception as e:
     #   print ("||view||create_new_instance error:" + str(e))
     #   messages.error(request, "Instance request failed to submit. Error: " + str(e))
     #   return HttpResponseRedirect(reverse('accounts:create_instance_form'))

   # messages.success(request, "Instance created successfully!")
    return HttpResponseRedirect(reverse('accounts:instance_list'))





@csrf_exempt
def create_bill_form(request):
    team_name_list = Team.objects.all()
    program_name_list = Program.objects.all()


    context = {
       
        'team_name_list' : team_name_list,
        'program_name_list' : program_name_list,
    }



    return render(request, 'billing.html', context)


@csrf_exempt
def create_bill(request):
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    team  = request.POST.get('team_name')
    program = request.POST.get('program_name')


    params = {
        'team':team,
        'program':program,
        'start_date':start_date,
        'end_date':end_date,
       
    }

    create_bill_aws(params)



    return HttpResponseRedirect(reverse('accounts:created_bill'))






@csrf_exempt
def created_bill(request):

    team_name = UserProfile.objects.get(user_name = request.user).team_name
    program_name = UserProfile.objects.get(user_name = request.user).program_name

    allowed_roles = ['admin']
    program_roles = ['program_manager']

    if request.user.groups.exists():
        group = request.user.groups.all()[0].name

    if group in allowed_roles:
        
        bill = {}

        created_bill = Bill.objects.values('program__program_name', 'team__team_name', 'start_date', 'end_date', 'total_cost', 'Unit', 'bill_name__instance_name')
        bill['data'] = created_bill

        total = 0
        for cost in bill['data']:
            
            total += int(cost['total_cost'])
        new_total = total

        context={
            'total_cost': new_total,
            'data': created_bill,
            "columns": ['Program',  'Team', 'Start Date',
                               'End Date', 'Total Cost', 'Unit']
        }

    elif group in program_roles:
        
        bill = {}
        created_bill = Bill.objects.filter(program__program_name =program_name ).values('program__program_name', 'team__team_name', 'start_date', 'end_date', 'total_cost', 'Unit', 'bill_name__instance_name')
        bill['data'] = created_bill

        total = 0
        for cost in bill['data']:
            
            total += int(cost['total_cost'])
        new_total = total

        context={
            'total_cost': new_total,
            'data': created_bill,
            "columns": ['Program',  'Team', 'Start Date',
                               'End Date', 'Total Cost', 'Unit']
        }

    else:
       
        bill = {}
        created_bill = Bill.objects.filter(team__team_name = team_name ).values('program__program_name', 'team__team_name', 'start_date', 'end_date', 'total_cost', 'Unit', 'bill_name__instance_name')
        bill['data'] =  created_bill
        #context[]
      
        total = 0
        for cost in bill['data']:
            
            total += int(cost['total_cost'])
        new_total = total

        context={
            'total_cost': new_total,
            'data': created_bill,
            "columns": ['Program',  'Team', 'Start Date',
                               'End Date', 'Total Cost', 'Unit']
        }






    return render(request, 'created_bill.html', context)















@csrf_exempt
def created_bill_program_man(request):

    context = {"columns": ['Program',  'Team', 'Start Date',
                               'End Date', 'Total Cost', ]}

    created_bill = Bill.objects.values('program', 'team' 'end_date', 'total_cost', 'Unit')
    context['data'] = created_bill



    

    return render(request, 'created_bill.html', context)