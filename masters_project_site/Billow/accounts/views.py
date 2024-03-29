from django.urls import reverse_lazy
from django.views.generic import CreateView
from . import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .Cloud_utils import*
from django.contrib import messages
from .decorators import users_allowed
import logging


# Create your views here.+
class Login(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/login.html"


## showing the list of instances in the db 
@csrf_exempt
def instance_list(request):
    print('USER', request.user.username)
    team_name = UserProfile.objects.get(user_name = request.user).team_name
    program_name = UserProfile.objects.get(user_name = request.user).program_name
    allowed_roles = ['admin']
    program_roles = ['program_manager']
    context = {"columns": ['Cloud Provider', 'Program', 'Team', 'Flavor',
                               'CPU (Total)', 'RAM (GB)',
                               'Storage (GB)', 'State', 'Created At', 'Total Cost to Date']}

    if request.user.groups.exists():
        group = request.user.groups.all()[0].name
    if group in allowed_roles:
       instance_list = Instance.objects.values('State','cloud_provider__cloud_prov_name', 'flavor__CPU', 'flavor__Ram_GB', 'flavor__Storage_GB', 'team__team_name', 'program__program_name', 'instance_name','flavor__flavor_name', 'launch_time', 'total_cost')
       context['data'] = instance_list
    elif group in program_roles:

        instance_list = Instance.objects.filter(program__program_name = program_name).values('State','cloud_provider__cloud_prov_name', 'flavor__CPU', 'flavor__Ram_GB', 'flavor__Storage_GB', 'team__team_name', 'program__program_name', 'instance_name','flavor__flavor_name', 'launch_time', 'total_cost')
        context['data'] = instance_list
    else:

        instance_list = Instance.objects.filter(team__team_name = team_name).values('State', 'cloud_provider__cloud_prov_name', 'flavor__CPU', 'flavor__Ram_GB', 'flavor__Storage_GB', 'team__team_name', 'program__program_name', 'instance_name','flavor__flavor_name', 'launch_time', 'total_cost')
        context['data'] = instance_list

    return render(request, 'instance_list.html', context)


## showing more details of the instance based on url selected
@csrf_exempt
def instance_details(request):
    instance_name = request.GET.get('instance_details')
    context = {"columns": ['Instance Name', 'Cloud Provider', 'Program', 'Team', 'Flavor',
                               'CPU (Total)', 'RAM (GiB)',
                               'Storage (GiB)', 'State', 'Created At']}

    instance_list = Instance.objects.filter(instance_name=instance_name).values('id_instance', 'Image_op__image_name', 'flavor__Ram_GB', 'flavor__flavor_name', 'flavor__CPU', 'instance_name', 'users__user_name', 'contact', 'cloud_provider__cloud_prov_name','team__team_name', 'program__program_name', 'instance_name','KeyName__key_name', 'Image_aws__Image_name', 'State', 'flavor__Storage_GB')
    context={

        'data' : instance_list,
    }
    
    return render(request, 'instance_details.html', context)


##  start, stop, delete and depending on user logged in 
@csrf_exempt
def instance_actions(request):
    user = request.user.username
    print(user)
    allowed_roles = ['admin', 'program_manager']


    logger = logging.getLogger(__name__)


    cloud_provider = request.POST.get('cloud_prov_name')
    instance_id = request.POST.get('id_instance')
    state = request.POST.get('state')

    print(f"cloud_provider: {cloud_provider}")
    print(f"instance_id: {instance_id}")

    print(cloud_provider)

    params = {
        'aws_instance_id':instance_id,
        'id_instance':instance_id
     }
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name
    if group in allowed_roles:

        if 'delete' in request.POST:
                try:
                    
                    if (cloud_provider == 'OpenStack'):
                        delete_openstack_instance(instance_id)
                    else:
                        delete_an_instance(params)

                except Exception as e:
                    print ("||view||delete_instance error:" + str(e))
                    messages.error(request, "Instance request failed to delete. Error: " + str(e))
                    return HttpResponseRedirect(reverse('accounts:instance_list'))
                messages.success(request, "Instance deleted successfully!")
                logger.info('Instance Deleted {} || By User {} || Time {}' .format(instance_id, user, datetime.now()))
                return HttpResponseRedirect(reverse('accounts:instance_list'))

        
            
        if 'stop' in request.POST:
           on_states = ['ACTIVE', 'running']
           if state in on_states:
                try:
                    if (cloud_provider == 'OpenStack'):
                            stop_openstack_instance(instance_id)
                    else:
                        stop_an_instance(params)

                except Exception as e:
                        print ("||view||delete_instance error:" + str(e))
                        messages.error(request, "Instance request failed to stop. Error: " + str(e))
                        return HttpResponseRedirect(reverse('accounts:instance_list'))
                messages.success(request, "Instance stopped successfully!")
                logger.info('Instance Stopped {} || By User {} || Time {}' .format(instance_id, user, datetime.now()))
                return HttpResponseRedirect(reverse('accounts:instance_list'))
           else:
                messages.success(request, "Instance already stopped!")
                
                return HttpResponseRedirect(reverse('accounts:instance_list'))

        if 'start' in request.POST:
            off_states =['stopped', 'SHUTOFF']
            if state in off_states:
                try:

                    if (cloud_provider == 'OpenStack'):
                            start_openstack_instance(instance_id)
                    else:
                    
                        start_an_instance(params)


                except Exception as e:
                        print ("||view||delete_instance error:" + str(e))
                        messages.error(request, "Instance failed to start. Error: " + str(e))
                        return HttpResponseRedirect(reverse('accounts:instance_list'))
                messages.success(request, "Instance started successfully!")
                logger.info('Instance Started {} || By User {} || Time {}' .format(instance_id, user, datetime.now()))
                return HttpResponseRedirect(reverse('accounts:instance_list'))
            else:
                 messages.success(request, "Instance is already running!")
                 return HttpResponseRedirect(reverse('accounts:instance_list'))


    else:
        messages.error(request, "You do not have permissions for this action instance")
        return HttpResponseRedirect(reverse('accounts:instance_list'))



## rendering the conetent the form 
@csrf_exempt
@users_allowed(allowed_roles=['admin', 'program_manager'])
def create_new_instance_form(request):
    cloud_providers_list = Cloud_Provider.objects.all()
    flavor_list = Flavor.objects.all()
    Image_aws_list = aws_image.objects.all()
    Image_op_list = Op_image.objects.all()
    KeyName_list = Key.objects.all()
    instance_name_list = Instance.objects.all()
    team_name_list = Team.objects.all()
    program_name_list = Program.objects.all()
    users_list = UserProfile.objects.all()
    Openstack_image_list = Op_image.objects.all()

    context = {
        'cloud_providers_list' : cloud_providers_list,
        'flavor_list': flavor_list,
        'Image_aws_list': Image_aws_list,
        'Image_op_list': Image_op_list,
        'KeyName_list': KeyName_list,
        'instance_name': instance_name_list,
        'team_name_list' : team_name_list,
        'program_name_list' : program_name_list,
        'users_list' : users_list,
        'Openstack_image_list': Openstack_image_list,

    }

    return render(request, 'create_instance_form.html', context)


## getting user inputted values and passing into other functions 
@csrf_exempt
def create_new_instance(request):

    user = request.user.username
    print(user)
    logger = logging.getLogger(__name__)

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
    storage = Flavor.objects.values_list('Storage_GB', flat=True).get(flavor_name=flavor_name)

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
        'storage': storage,
        'openstack_image_id' : Openstack_image_id
    }

    try:
        if (cloud_provider == 'OpenStack'):
                create_openstack_instance(params)
        else:
                create_aws_instance(params)


    except Exception as e:
     print ("||view||create_new_instance error:" + str(e))
     messages.error(request, "Instance request failed to submit. Error: " + str(e))
     return HttpResponseRedirect(reverse('accounts:create_instance_form'))
    logger.info('Instance Created {} || By User {} || Time {}' .format(instance_name, user, datetime.now()))
    messages.success(request, "Instance created successfully!")
    return HttpResponseRedirect(reverse('accounts:instance_list'))



def user_instances(request):

    print('USER', request.user.username)
    team_name = UserProfile.objects.get(user_name = request.user).team_name ## getting the users team
    program_name = UserProfile.objects.get(user_name = request.user).program_name  ## getting the users program

    allowed_roles = ['admin']
    program_roles = ['program_manager']

    if request.user.groups.exists():
        group = request.user.groups.all()[0].name

    if group in allowed_roles:
         instances_name = snapshot_instance.objects.values('instance_name').distinct()
    elif group in program_roles:
        instances_name = snapshot_instance.objects.filter(program =program_name ).values('instance_name').distinct()
    else:
        instances_name = snapshot_instance.objects.filter(team =team_name ).values('instance_name').distinct()
    return instances_name



def create_bill_form(request):
    return render(request, 'billing.html')



@csrf_exempt
def create_bill(request):
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
  

    user_insatnces = user_instances(request)  ## get only the instance associated with user logged in
   

    params = {
       
        'start_date':start_date,
        'end_date':end_date,
        'instances_names': user_insatnces
       
    }


    try:
            bill_details = create_time_bill(params)
    except Exception as e:
            print ("||view||billing form error:" + str(e))
            messages.error(request, "Billng request failed Error: " + str(e))
            return render(request, 'billing.html')

    bill = {}
    total = 0
    created_bill = bill_details
    bill['data'] = created_bill
    for instance_name in bill['data']:
        instance_total_cost = bill_details[instance_name]['total_cost']

        total += float(instance_total_cost) ## adding up the costs
    new_total = round(total, 2)

    context={
            'total_cost': new_total,
            'data': created_bill,
            "columns": ['Program',  'Team', 'Start Date',
                                'End Date', 'Total Cost', 'Unit']
    }

    return render(request, 'created_bill.html', context)



@csrf_exempt
def sync_state_view(request):

    sync_aws_state()
    sync_state()

    return HttpResponse('states synced')


## dev purposes 
@csrf_exempt
def sync_cloud(request):

    sync_aws_cloud()
    synch_op_cloud()

    return HttpResponseRedirect(reverse('accounts:instance_list'))


