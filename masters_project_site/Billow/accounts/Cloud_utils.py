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
    
import pytz

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
def get_client_aws():

    client = boto3.client(
        'ec2',
        aws_access_key_id='AKIAQAS2UWXQJQVWZRSC',
        aws_secret_access_key='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',
        region_name = 'us-east-1'
        )

    return(client)



def create_aws_instance(params):


    resource = boto3.resource(
        'ec2',
        aws_access_key_id='AKIAQAS2UWXQJQVWZRSC',
        aws_secret_access_key='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',
        region_name = 'us-east-1'
    )


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
    BlockDeviceMappings=[
            {
                'DeviceName': '/dev/xvda',
                'Ebs': {
                    'VolumeSize': int(params['storage']),
                    'VolumeType': 'standard'
                }
            }
        ]
    )

    instance_id = instances[0].instance_id
    launch_time = instances[0].launch_time
    sync_aws_state()
    
    Instance_object = Instance(
        cloud_provider= Cloud_Provider.objects.get(cloud_prov_name = params['cloud_provider']),
        flavor=Flavor.objects.get(flavor_name=params['flavor']),
        Image_op= Op_image.objects.get(image_name ="N/A"),
        Image_aws=aws_image.objects.get(Image_name=params['Image']),
        KeyName=Key.objects.get(key_name=params['aws_key_name']),
        instance_name=params['instance_name'],
        team=Team.objects.get(team_name = params['team']),
        program=Program.objects.get(program_name = params['program']),
        users=UserProfile.objects.get(user_name=params['users']),
        contact=params['contact'],
        id_instance=instance_id,
        launch_time=launch_time,
        total_cost = 0
    )

    #Instance_object.flavor = Flavor.objects.get(flavor_name=params['flavor'])
    Instance_object.save()
    sync_aws_state()



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
    instance_create = []
    instance_status = []
    instances = (nova.servers.list())
    for server in instances:
        instances = server.id
        instance_launch = server.created
        instance_state = server.status

        li = (instances.split(" "))
        li_created = (instance_launch.split(" "))
        li_state = (instance_state.split(" "))

        instance_create.append(li_created)
        instance_list.append(li)
        instance_status.append(li_state)

    launch_time = instance_create[0][0]
    Instance_id = instance_list[0][0]
    state = instance_status[0][0]
    
    Instance_object = Instance(
    cloud_provider= Cloud_Provider.objects.get(cloud_prov_name = params['cloud_provider']),
    flavor=Flavor.objects.get(flavor_name=params['flavor']),
    Image_op= Op_image.objects.get(image_name = params['Openstack_image_name']),
    KeyName=Key.objects.get(key_name="N/A"),
    Image_aws=aws_image.objects.get(Image_name="N/A"),
    instance_name=params['instance_name'],
    team=Team.objects.get(team_name = params['team']),
    program=Program.objects.get(program_name = params['program']),
    users=UserProfile.objects.get(user_name= params['users']),
    contact=params['contact'],
    id_instance = Instance_id,
    launch_time = launch_time,
    total_cost = 0,
    State = state
    
)

    Instance_object.save()


#def delete_openstack_instance(params):


def delete_openstack_instance(instance_id):

  clients = get_clients('admin')
    
  nova = clients['nova']
  nova.servers.delete(instance_id)

  delete_db_instance_op(instance_id)

def delete_db_instance_op(instance_id):
    print(instance_id)
    Instance_obj = Instance.objects.get(id_instance=instance_id)
    Instance_obj.delete()



def stop_openstack_instance(instance_id):

  clients = get_clients('admin')
    
  nova = clients['nova']
  nova.servers.stop(instance_id)


def start_openstack_instance(instance_id):

  clients = get_clients('admin')
    
  nova = clients['nova']
  nova.servers.start(instance_id)




def synch_op_cloud():
    #Cloud_Provider=OpenStack
    instance_db = Instance.objects.filter(cloud_provider__cloud_prov_name ='OpenStack').values_list('instance_name', flat=True)

    clients = get_clients('admin')
    nova = clients['nova']

    instances = nova.servers.list()
    

    # Add new instances to the local database
    instances_to_add = [server for server in instances if server.name not in instance_db]

    for server in instances_to_add:
        instance_name_add = server.name
        flavor_id = server.flavor['id']
        flavor_name = Flavor.objects.filter(id_flavor=flavor_id).values_list('flavor_name', flat=True).first()
     
        launch = server.created
        state = server.status
        image = server.image
        for id in image:
            image_id = image['id']


        print(image_id, launch, flavor_id)

        instance_id = server.id

        Instance_object = Instance(
            cloud_provider=Cloud_Provider.objects.get(cloud_prov_name ='OpenStack'),
            flavor=Flavor.objects.get(flavor_name =flavor_name),
            Image_op=Op_image.objects.get(Image_ID=image_id),
            instance_name=instance_name_add,
            id_instance=instance_id,
            launch_time = launch,
            State = state,
       
        )

        Instance_object.save()

    # Delete instances from the local database that are not found in OpenStack
    instances_to_delete = set(instance_db) - set(server.name for server in instances)
    for instance_name in instances_to_delete:
        Instance.objects.filter(instance_name=instance_name).delete()
      

def sync_aws_cloud():

        instance_db = Instance.objects.filter(cloud_provider__cloud_prov_name='AWS').values_list('instance_name', flat=True)



        resource = boto3.resource(
        'ec2',
        aws_access_key_id='AKIAQAS2UWXQJQVWZRSC',
        aws_secret_access_key='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',
        region_name = 'us-east-1'
        )

        instances = resource.instances.all()

        # Add new instances to the local database
        instances_to_add = []
    

        for instance in instances:
            if instance.tags is not None:
                for tag in instance.tags:
                    if tag['Key'] == 'Name' and tag['Value'] not in instance_db:
                        instances_to_add.append(instance)
                        break

        for instance in instances_to_add:
            instance_name_add = [tag['Value'] for tag in instance.tags if tag['Key'] == 'Name'][0]
            flavor_name = instance.instance_type
            image_id = instance.image_id
            instance_id = instance.id
            launch_time = instance.launch_time
            State = instance.state
            Key_name = instance.key_name

            Instance_object = Instance(
                cloud_provider=Cloud_Provider.objects.get(cloud_prov_name ='AWS'),
                flavor=Flavor.objects.get(flavor_name =flavor_name),
                Image_aws=aws_image.objects.get(Image_name =image_id),
                instance_name=instance_name_add,
                id_instance=instance_id,
                State = State,
                launch_time = launch_time,
                KeyName = Key.objects.get(key_name = Key_name)
            )

            Instance_object.save()

        # Delete instances from the local database that are not found in AWS
        instance_names = {tag['Value'] for instance in instances for tag in instance.tags if tag['Key'] == 'Name'}
        instances_to_delete = set(instance_db) - instance_names
        for instance_name in instances_to_delete:
            Instance.objects.filter(instance_name=instance_name).delete()
























## syncing states for aws and openstack clouds 
def sync_state():
    clients = get_clients('admin')
    nova = clients['nova']
    state = {}
    instances = (nova.servers.list())

    for server in instances:
        state[server.name] = server.status
    
    instances = Instance.objects.filter(cloud_provider__cloud_prov_name='OpenStack')

    for instance in instances:
        Instance.objects.filter(instance_name = instance.instance_name).update(State=state[instance.instance_name])

def sync_aws_state():
    client = get_client_aws()
    Myec2=client.describe_instances()
    state = {}
    for data in Myec2['Reservations']:
     for instance_data in data['Instances']:
        for instance_name in instance_data['Tags']:
      
            state[instance_name['Value']] = instance_data['State']['Name']
            
    instances = Instance.objects.filter(cloud_provider__cloud_prov_name='AWS')
  
    for instance in instances:
        Instance.objects.filter(instance_name = instance.instance_name).update(State=state[instance.instance_name])



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
    for instance in instances:
            new_instance_snap = snapshot_instance(
            
            instance_snap_index_obj=new_instance_snap_index,
            instance_name = instance.instance_name,
            cloud_provider = instance.cloud_provider,
            team = instance.team,
            program = instance.program,
            contact = instance.contact,
            Image_op = instance.Image_op,
            Image_aws = instance.Image_aws,
            KeyName =  instance.KeyName,
            flavor = instance.flavor,
            users = instance.users,
            State = instance.State,
            id_instance = instance.id_instance,
            launch_time = instance.launch_time,
            CPU = instance.flavor.CPU,
            total_cost = instance.total_cost,
          
            )

            new_instance_snap.save()

def get_snapshots():

    end_date = date.today()
    start_date = date.today() - timedelta(hours=24)

    current_ind = Instance_snap_ind.objects.last()  # most recent snapshot 

    
    snapped_instances = snapshot_instance.objects.filter(instance_snap_index_obj=current_ind, cloud_provider = 'OpenStack') ## openstack instances
    snapped_instances_aws = snapshot_instance.objects.filter(instance_snap_index_obj=current_ind, cloud_provider = 'AWS') ## aws instances

    client = boto3.client(
    'ce',
    aws_access_key_id='AKIAQAS2UWXQJQVWZRSC',
    aws_secret_access_key='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',
    region_name = 'us-east-1'
    )

    for instance_aws in snapped_instances_aws: ## aws daily and updating total cost
        
        response = client.get_cost_and_usage(
            TimePeriod={
                'Start': str(start_date),
                'End': str(end_date)
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


    for instance in snapped_instances: ## openstack dialy cost and updating total cost 
            allocated_cpu = 0
            allocated_cpu += instance.CPU
            daily_cost = allocated_cpu*Decimal(.69)

       
            instance.daily_cost = daily_cost
            instance.save()

        
            current_instance = Instance.objects.get(instance_name = instance.instance_name)
            print(type(daily_cost))
            current_instance.total_cost += daily_cost
            current_instance.save()




def create_time_bill(params):
    timezone = pytz.timezone('Europe/Dublin')

# creating the start time and end time user inputted objects so calculation can be done 
    start_date_str = params['start_date']
    end_date_str = params['end_date']
    date_format = '%Y-%m-%d'
    start_date = datetime.strptime(start_date_str, date_format)
    start_date = timezone.localize(start_date)
    end_date = datetime.strptime(end_date_str, date_format)
    end_date = timezone.localize(end_date)
    instance_names = params['instances_names'] ## dictornary so it only get the instances associated with the user


    snapshot_indices = Instance_snap_ind.objects.filter(timestamp__range=(start_date, end_date))

# Get all snapshots asscoaited with the user inputted time range
    snapshots = snapshot_instance.objects.filter(instance_snap_index_obj__in=snapshot_indices, instance_name__in=instance_names)

    # creating a dictionary that groups all the instances by instance name so they can be called this way (key:instance_name -- value: snapshots asscoaited with the name)
    snapshots_instance = {}
    for snapshot in snapshots:
        if snapshot.instance_name not in snapshots_instance:
            snapshots_instance[snapshot.instance_name] = []
        snapshots_instance[snapshot.instance_name].append(snapshot)
  

    # to get the total cost within the specified range
    total_cost_range = {} 
    for instance_name, instance_snapshots in snapshots_instance.items():
        daily_cost_in_range = 0
        for snapshot in instance_snapshots:
            if snapshot.instance_snap_index_obj.timestamp >= start_date and snapshot.instance_snap_index_obj.timestamp <= end_date:   ## if it falls within this range do the following
                daily_cost_in_range += snapshot.daily_cost
        total_cost_range[instance_name] = daily_cost_in_range

  

    bill_details = {}
    for index in snapshot_indices:
        every_time_inst = snapshot_instance.objects.filter(instance_snap_index_obj= index, instance_name__in = instance_names)

        for instance in every_time_inst:
            bill_details[instance.instance_name] =  {

                'Instance': instance.instance_name,
                'program' : Program.objects.get(program_name = instance.program),
                'team': Team.objects.get(team_name = instance.team),
                'start_date' : start_date.strftime(date_format),
                'end_date' : end_date.strftime(date_format),
                'total_cost' : str(total_cost_range[instance.instance_name]),
                'Unit' : 'USD'

                } 
    
    return bill_details 












