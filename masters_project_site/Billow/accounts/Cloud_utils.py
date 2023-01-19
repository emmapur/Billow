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
        cloud_provider= params['cloud_provider'],
        flavor=Flavor.objects.get(flavor_name=params['flavor']),
        Image=params['Image'],
        KeyName=params['aws_key_name'],
        instance_name=params['instance_name'],
        team=params['team'],
        program=params['program'],
        users=params['users'],
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
    auth_url = 'http://10.54.48.19/identity/v3'
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


    nova.servers.create(name = params['instance_name'], image = params['openstack_image_id'], flavor = params['openstack_flavor_id'],  nics = [{'net-id': params['openstack_network_id']}])
    instance_list = []
    instances = (nova.servers.list())
    for instances in instances:
        instances = instances.id
        li = (instances.split(" "))
    #print(li.append)
        instance_list.append(li)    
    Instance_id = instance_list[0][0]

    Instance_object = Instance(
    cloud_provider= params['cloud_provider'],
    flavor=Flavor.objects.get(flavor_name=params['flavor']),
    Image=params['openstack_image_id'],
   # KeyName=params['aws_key_name'],
    instance_name=params['instance_name'],
    team=params['team'],
    program=params['program'],
    users=params['users'],
    contact=params['contact'],
    network=params['openstack_network_id'],
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

