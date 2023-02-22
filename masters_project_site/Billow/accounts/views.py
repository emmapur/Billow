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
from django.db.models import Exists, OuterRef




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
                               'CPU (Total)', 'RAM (MB)',
                               'Storage (GB)', 'State', 'Created At']}

       instance_list = Instance.objects.values('State','cloud_provider__cloud_prov_name', 'flavor__CPU', 'flavor__Ram_MB', 'flavor__Storage_GB', 'team__team_name', 'program__program_name', 'instance_name','flavor__flavor_name', 'launch_time')
       context['data'] = instance_list
    elif group in program_roles:
        context = {"columns": ['Cloud Provider', 'Program', 'Team', 'Flavor',
                               'CPU (Total)', 'RAM (GiB)',
                               'Storage (GiB)', 'State', 'Created At']}
        instance_list = Instance.objects.filter(program__program_name = program_name).values('State','cloud_provider__cloud_prov_name', 'flavor__CPU', 'flavor__Ram_MB', 'flavor__Storage_GB', 'team__team_name', 'program__program_name', 'instance_name','flavor__flavor_name', 'launch_time')
        context['data'] = instance_list
    else:
        context = {"columns": ['Cloud Provider', 'Program', 'Team', 'Flavor',
                               'CPU (Total)', 'RAM (GiB)',
                               'Storage (GiB)', 'State', 'Created At']}
        instance_list = Instance.objects.filter(team__team_name = team_name).values('State', 'cloud_provider__cloud_prov_name', 'flavor__CPU', 'flavor__Ram_MB', 'flavor__Storage_GB', 'team__team_name', 'program__program_name', 'instance_name','flavor__flavor_name', 'launch_time')
        context['data'] = instance_list

    return render(request, 'instance_list.html', context)



@csrf_exempt
def instance_details(request):
    instance_name = request.GET.get('instance_details')

    context = {"columns": ['Instance Name', 'Cloud Provider', 'Program', 'Team', 'Flavor',
                               'CPU (Total)', 'RAM (GiB)',
                               'Storage (GiB)', 'State', 'Created At']}

    instance_list = Instance.objects.filter(instance_name=instance_name).values('id_instance', 'Image_op__image_name', 'flavor__Ram_MB', 'flavor__flavor_name', 'flavor__CPU', 'instance_name', 'users__user_name', 'contact', 'cloud_provider__cloud_prov_name','team__team_name', 'program__program_name', 'instance_name','KeyName')


    context={

        'data' : instance_list,
    }
    
    return render(request, 'instance_details.html', context)



@csrf_exempt
def delete_instance(request):
  
    #cloud_provider = request.GET.get('cloud_prov_name')
    #instance_id = request.POST.get('id_instance')
    sync_aws_state()
  #  
   # print(cloud_provider)

    #params = {
       # 'aws_instance_id':instance_id,
       # 'id_instance':instance_id
   # }

  #  take_snapshot_instance()
  #  get_snapshots()


  #  if (cloud_provider == 'OpenStack'):
   # delete_openstack_instance(instance_id)
   # else:
      #  delete_an_instance(params)

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

    Openstack_image_list = Op_image.objects.all()

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
 
    Openstack_image_name = request.POST.get('Image_name_op')

    Openstack_image_id = Op_image.objects.values_list('Image_ID', flat=True).get(image_name=Openstack_image_name)

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
        'Openstack_image_name':  Openstack_image_name,
    
        'openstack_image_id' : Openstack_image_id
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







def user_instances(request):

    team_name = UserProfile.objects.get(user_name = request.user).team_name
    program_name = UserProfile.objects.get(user_name = request.user).program_name

    allowed_roles = ['admin']
    program_roles = ['program_manager']

    if request.user.groups.exists():
        group = request.user.groups.all()[0].name

    if group in allowed_roles:
         

         instances_name = snapshot_instance.objects.values('instance_name').distinct()
         print(instances_name)
         
         #for instance in instances_name:
         #   if instance not in instance_list:
         #       instance_list.append(instance)

       #  instances_name_list = instance_list 

       #  print(instances_name)

    elif group in program_roles:
        
        instances_name = Instance.objects.filter(program__program_name =program_name ).values('instance_name')
     
     
    else:
        instances_name = Instance.objects.filter(team__team_name =team_name ).values('instance_name')

    return instances_name

def create_bill_form(request):

    return render(request, 'billing.html')





@csrf_exempt
def create_bill(request):
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
  

    user_insatnces = user_instances(request)
   

    params = {
       
        'start_date':start_date,
        'end_date':end_date,
        'instances_names': user_insatnces
       
    }

    bill_details = create_time_bill(params)

    bill = {}
    total = 0 
    created_bill = bill_details
    print(created_bill)
    bill['data'] = created_bill

    for instance_name in bill['data']:
        instance_total_cost = bill_details[instance_name]['total_cost']

        total += float(instance_total_cost)
    new_total = total

    context={
            'total_cost': new_total,
            'data': created_bill,
            "columns": ['Program',  'Team', 'Start Date',
                                'End Date', 'Total Cost', 'Unit']
    }

    return render(request, 'created_bill.html', context)




