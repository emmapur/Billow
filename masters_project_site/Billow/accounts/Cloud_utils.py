import boto3
from botocore.config import Config
from .models import *
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import sys
import keystoneauth1
import neutron
from decimal import Decimal

import hashlib
# sys.path.append('/home/epuremm/meteo') 
# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meteo.settings') 
# if 'setup' in dir(django):

#     django.setup() 
#from typhoon.models import *
from django.core.exceptions import MultipleObjectsReturned
#from typhoon.services import projectservice as ps
from keystoneauth1.identity import v2,v3
from keystoneauth1 import session
from keystoneclient import client as ksClient, utils, exceptions as keystoneExceptions
from novaclient import client as novaClient, exceptions as novaExceptions
from cinderclient import client as cinderClient, exceptions as cinderExceptions, utils as cinderUtils

from neutronclient.v2_0 import client as neutronClient
from heatclient import client as heatClient
from glanceclient import client as glanceClient
from datetime import timedelta,date,datetime

# create code for creating instance


# creating aws instance
def create_aws_instance(params):


    resource = boto3.resource(
        'ec2',
        aws_access_key_id='AKIAQAS2UWXQJQVWZRSC',
        aws_secret_access_key='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',
        region_name = 'us-east-1'
    )

    my_config = Config(
        region_name = 'us-east-1',)

    instances = resource.create_instances(
            ImageId=params['aws_image_id'],
            MinCount=1,
            MaxCount=1,
            InstanceType=params['aws_instance_type'],
            KeyName=params['aws_key_name'],
            TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': params['instance_name']
                },
            ]
        },
    ],
        )

    instance_id = instances[0].instance_id
    launch_time = instances[0].launch_time

    Instance_object = Instance(
        cloud_provider= Cloud_Provider.objects.get(cloud_prov_name=params['cloud_provider']),
        flavor=Flavor.objects.get(flavor_name=params['flavor']),
        Image=params['Image'],
        KeyName=Key.objects.get(key_name=params['aws_key_name']),
        instance_name=params['instance_name'],
        team=Team.objects.get(team_name=params['team']),
        program=Program.objects.get(program_name=params['program']),
        users=UserProfile.objects.get(user_name=params['users']),
        contact=params['contact'],
        id_instance=instance_id,
        launch_time=launch_time
    )

    #Instance_object.flavor = Flavor.objects.get(flavor_name=params['flavor'])
    Instance_object.save()



def delete_an_instance(params):

    client = boto3.client(
        'ec2',
        aws_access_key_id='AKIAQAS2UWXQJQVWZRSC',
        aws_secret_access_key='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',
        region_name = 'us-east-1'
        )

    response = client.terminate_instances(
	    InstanceIds=[params['aws_instance_id']],
)

    delete_db_instance(params['aws_instance_id'])

def delete_db_instance(instance_id):
    print(instance_id)
    Instance_obj = Instance.objects.get(id_instance=instance_id)
    Instance_obj.delete()






def stop_an_instance(params):

    client = boto3.client(
        'ec2',
        aws_access_key_id='AKIAQAS2UWXQJQVWZRSC',
        aws_secret_access_key='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',
        region_name = 'us-east-1'
        )

    response = client.stop_instances(
	    InstanceIds=[params['aws_instance_id']],
)

def start_an_instance(params):

    client = boto3.client(
        'ec2',
        aws_access_key_id='AKIAQAS2UWXQJQVWZRSC',
        aws_secret_access_key='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',
        region_name = 'us-east-1'
        )

    response = client.start_instances(
	    InstanceIds=[params['aws_instance_id']],
)



# create openstack instnace



def get_clients(project_name):
    
    #     cloud = Cloud.objects.get(cloud_name="6b")
    auth_url = 'http://192.168.1.23/identity/v3'
    username='admin'
    password='secret'
    project_name=project_name

    auth = v3.Password(username=username, password=password, project_name=project_name, auth_url=auth_url, project_domain_name='default', user_domain_name='default')
    sess = session.Session(auth=auth, verify=False)

    keystone = ksClient.Client(session=sess, interface='public')
    nova = novaClient.Client(2, session=sess)
    cinder = cinderClient.Client(3, session=sess)
    neutron = neutronClient.Client(session=sess)
    heat = heatClient.Client(1,session=sess)
    glance = glanceClient.Client('2', session=sess)

    return {"nova":nova, "keystone":keystone, "cinder":cinder,"heat":heat,"glance":glance,"neutron":neutron}


def create_openstack_instance(params):

    clients = get_clients('admin')
    
    nova = clients['nova']
    cinder = clients['cinder']
    glance = clients['glance']
    neutron = clients['neutron']
    keystone = clients['keystone']


    nova.servers.create(name = params['instance_name'], image = params['openstack_image_id'], flavor = params['openstack_flavor_id'],  nics = [{'net-id': '028ec515-365c-418d-b026-66760088fad5'}])
    instance_list = []
    instances = (nova.servers.list())
    for server in instances:
        instances = server.id
        li = (instances.split(" "))
    #print(li.append)
        instance_list.append(li)    
    Instance_id = instance_list[0][0]

    Instance_object = Instance(
    cloud_provider= Cloud_Provider.objects.get(cloud_prov_name = params['cloud_provider']),
    flavor=Flavor.objects.get(flavor_name=params['flavor']),
    Image=params['openstack_image_id'],
    KeyName=Key.objects.get(key_name="N/A"),
    instance_name=params['instance_name'],
    team=Team.objects.get(team_name = params['team']),
    program=Program.objects.get(program_name = params['program']),
    users=UserProfile.objects.get(user_name= params['users']),
    contact=params['contact'],
    id_instance = Instance_id
    
    #id_instance=instance_id,
   # launch_time=launch_time
)



#Instance_object.flavor = Flavor.objects.get(flavor_name=params['flavor'])
    Instance_object.save()


#def delete_openstack_instance(params):


def delete_openstack_instance(params):

  clients = get_clients('admin')
    
  nova = clients['nova']
  nova.servers.delete(params['id_instance'])

  delete_db_instance_op(params['id_instance'])

def delete_db_instance_op(instance_id):
    print(instance_id)
    Instance_obj = Instance.objects.get(id_instance=instance_id)
    Instance_obj.delete()



def synch_op_cloud():
    #Cloud_Provider=OpenStack
    instance_db = Instance.objects.filter(cloud_provider='OpenStack').values_list('instance_name', flat=True)

    
    clients = get_clients('admin')
    
    nova = clients['nova']

    instance_list = []
    instances = (nova.servers.list())
    for server in instances:
         instance = server.name
         instance_list.append(instance)

   

    list_to_add = list(set(instance_list) - set(instance_db))
    instance_name_add = list_to_add[0]

    instance_list = []
    instances = (nova.servers.list(instance_name_add))
    for server in instances:
        instance = server.name
        instance_flavor = server.flavor['id']
        instance_image = server.image['id']
        instance_id = server.id

    
    flavor_name = Flavor.objects.filter(id_flavor = instance_flavor).values_list('flavor_name', flat=True)
    print(flavor_name)
    Instance_object = Instance(
        cloud_provider= 'Openstack',
        flavor=flavor_name,
        Image= instance_image,
        instance_name= instance_name_add,
        id_instance=instance_id
    )
    
    Instance_object.save()
      

    

def create_bill_aws(params):
    client = boto3.client(
    'ce', 
    aws_access_key_id='AKIAQAS2UWXQJQVWZRSC',
    aws_secret_access_key='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',
    #aws_session_token=SESSION_TOKEN
    region_name = 'us-east-1')


    response = client.get_cost_and_usage(
        TimePeriod={
            'Start': params['start_date'],
            'End': params['end_date'],
        },
        Granularity='MONTHLY',

        Metrics=[
            'NetAmortizedCost',
        ]
)

    print(response['ResultsByTime'])

    for cost in response['ResultsByTime']:
    #print(cost)
        Total = (cost['Total'])
        all_cost  = Total['NetAmortizedCost']
        total_cost = all_cost['Amount']
        Unit = all_cost['Unit']


    bill_object = Bill(
    program = params['program'],
    team= params['team'],
    start_date=params['start_date'],
    end_date=params['end_date'],
    total_cost = total_cost,
    Unit = Unit
    )
  
    bill_object.save()
    

def take_snapshot_instance():

    timestamp = django.utils.timezone.now()
    hash = hashlib.sha1()
    timestamp = (str(timestamp))
    encode_timestamp = timestamp.encode(encoding='UTF-8', errors ='strict')
    hash.update((encode_timestamp))
    new_instance_snap_index = Instance_snap_ind(
        timestamp=timestamp,
        hash_key=hash.hexdigest()
        )

    new_instance_snap_index.save()

    instances = Instance.objects.filter()
    #for flavor in flavors:
    for instance in instances:
            new_instance_snap = snapshot_instance(
            
            instance_snap_index_obj=new_instance_snap_index,
            instance_name = instance.instance_name,
            cloud_provider = instance.cloud_provider,
            team = instance.team,
            program = instance.program,
            contact = instance.contact,
            Image = instance.Image,
            KeyName =  instance.KeyName,
            flavor = instance.flavor,
            users = instance.users,
            id_instance = instance.id_instance,
            launch_time = instance.launch_time,
            CPU = instance.flavor.CPU,
            id_flavour = instance.id_flavour,
            total_cost = instance.total_cost,
          
            )

            new_instance_snap.save()

def get_snapshots():

    end_date = '2023-02-16' ##time now
    start_date = '2023-02-09' ##time - 24
    snapped_instances_dict = {}
    current_ind = Instance_snap_ind.objects.last()
    print(current_ind)
    
    snapped_instances = snapshot_instance.objects.filter(instance_snap_index_obj=current_ind, cloud_provider = 'OpenStack')
    print(snapped_instances)
    snapped_instances_aws = snapshot_instance.objects.filter(instance_snap_index_obj=current_ind, cloud_provider = 'AWS')


    for instance_aws in snapped_instances_aws:
        
        client = boto3.client(
        'ce', 
        aws_access_key_id='AKIAQAS2UWXQJQVWZRSC',
        aws_secret_access_key='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',
        region_name = 'us-east-1')


        response = client.get_cost_and_usage(
            TimePeriod={
                'Start': '2023-02-11',
                'End': '2023-02-12'
            },
            Granularity='MONTHLY',
            Filter={

                    
                'Tags': {
                    'Key': 'Name',
                    'Values':[ str(instance_aws),]
                    }
            },

            Metrics=[
                'UNBLENDED_COST',
            ]
        )

        print(response['ResultsByTime'])

        for cost in response['ResultsByTime']:
   
            Total = (cost['Total'])
            all_cost  = Total['UnblendedCost']
            daily_cost = all_cost['Amount']
            Unit = all_cost['Unit']

            print(daily_cost)
        daily_cost = Decimal(daily_cost)
        instance_aws.daily_cost = daily_cost
        instance_aws.save()

        
        current_instance = Instance.objects.get(instance_name = instance_aws.instance_name)
        print(type(daily_cost))
        current_instance.total_cost += daily_cost
        current_instance.save()


    for instance in snapped_instances:
            allocated_cpu = 0
            allocated_cpu += instance.CPU
            daily_cost = allocated_cpu*Decimal(.69)

       
            instance.daily_cost = daily_cost
            instance.save()

        
            current_instance = Instance.objects.get(instance_name = instance.instance_name)
            print(type(daily_cost))
            current_instance.total_cost += daily_cost
            current_instance.save()


    






  #  for index in snapped_instances:
    
     #   print(index)
      
   #     snapped_instances_dict[index.timestamp] = snapped_instances
      #  print(snapped_instances)



    #for name in snapped_instances:
     #   Instances = snapshot_instance.objects.filter(instance_name=name)
      #  total_cpu = 0 
     #   instance_name = 0
      #  print(Instances)


        
       # total_cost = total_cpu*0.69
      #  print(total_cost)
       # name_of_instance = instance.CPU
       # print(name_of_instance)
       # instances_dict[instance.nam: total_cost]









