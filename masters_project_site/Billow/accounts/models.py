from django.db import models
from django.contrib import auth
from django.utils import timezone
import django



class Cloud_Provider(models.Model):

    cloud_prov_name = models.CharField(max_length=64, unique=True)
    #auth_method = models.CharField(max_length=64, unique=True)
#    active = models.BooleanField(default=True) ??

    def __str__(self):
        return self.cloud_prov_name

class Team(models.Model):

    team_name = models.CharField(max_length=64, unique=False)
    program_name = models.CharField(max_length=64, unique=False)
    point_of_contact = models.CharField(max_length=64, unique=False)
    network_code = models.CharField(max_length=64, unique=False)

    def __str__(self):
        return self.team_name

class User(models.Model):

    username = models.CharField(max_length=64)
    #password = models.CharField(max_length=64, unique=True)
    team_name =  models.CharField(max_length=64, unique=True)
    employee_number = models.CharField(max_length=64, unique=True)
    #email = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(editable=False, default=django.utils.timezone.now)
    last_login = models.DateTimeField(editable=False, default=django.utils.timezone.now)
    user_role = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return "@{}".format(self.username) #username is built in with .User normal built in stuff user name password and email

class role(models.Model):
    role_name = models.CharField(max_length=64, unique=False)
    role_type = models.CharField(max_length=64, unique=False)

    def __str__(self):
        return self.role_name

class Flavor(models.Model):
    flavor_name = models.CharField(max_length=64, blank=False, null=False)
    CPU = models.CharField(max_length=32, blank=True, null=True)
    Storage = models.CharField(max_length=32, blank=True, null=True)
    Ram = models.CharField(max_length=32, blank=True, null=True)
    id_flavor = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return self.flavor_name

class Program(models.Model):
    program_name = models.CharField(max_length=64)
    budget = models.CharField(max_length=64)

    def __str__(self):
        return self.program_name

class Openstack_image(models.Model):
    Openstack_image_name = models.CharField(max_length=64)
    Image_ID = models.CharField(max_length=64)

    def __str__(self):
        return self.Openstack_image_name
        
class Image(models.Model):
    Image_name = models.CharField(max_length=64)
    Image_ID = models.CharField(max_length=64)

    def __str__(self):
        return self.Image_name

class Openstack_Network(models.Model):
    Openstack_Network_name = models.CharField(max_length=64)
    Openstack_Network_id = models.CharField(max_length=64)

    def __str__(self):
        return self.Openstack_Network_name



class Key(models.Model):
    key_name = models.CharField(max_length=64)
    key_name_ID = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.key_name

class id_instance(models.Model):
    id_instance_name = models.CharField(max_length=64)

    def __str__(self):
        return self.id_instance_name

class Instance(models.Model):

    cloud_provider = models.CharField(max_length=64)
    instance_name = models.CharField(max_length=64, unique=True)
    team = models.CharField(max_length=64)
    #reference = models.CharField(max_length=64, unique=True)
    program = models.CharField(max_length=64)
    contact = models.CharField(max_length=64)
    #created_by = models.CharField(max_length=64, unique=True)
    Image = models.CharField(max_length=64)
    KeyName = models.CharField(max_length=64)
    flavor = models.ForeignKey(Flavor, on_delete=models.PROTECT, null=True)
    users = models.CharField(max_length=64)
    contact = models.CharField(max_length=64, unique=True)
    id_instance = models.CharField(max_length=64, unique=True)
    launch_time = models.CharField(max_length=64, null=True)
    openstack_flavor_id = models.CharField(max_length=64, null=True)
    network = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return str(self.instance_name)
