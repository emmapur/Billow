from django.db import models
from django.contrib import auth
from django.utils import timezone
import django
from django.contrib.auth.models import User



class Cloud_Provider(models.Model):

    cloud_prov_name = models.CharField(max_length=64, unique=True)
    #auth_method = models.CharField(max_length=64, unique=True)
#    active = models.BooleanField(default=True) ??

    def __str__(self):
        return self.cloud_prov_name

class Program(models.Model):
    program_name = models.CharField(max_length=64)
    budget = models.CharField(max_length=64)

    def __str__(self):
        return self.program_name

class Team(models.Model):

    team_name = models.CharField(max_length=64, unique=False)
    program_name = models.ForeignKey(Program, on_delete=models.PROTECT, null=True)
    point_of_contact = models.CharField(max_length=64, unique=False)
    network_code = models.CharField(max_length=64, unique=False)

    def __str__(self):
        return self.team_name


class UserProfile(models.Model):
    user = models.ForeignKey(User,  on_delete=models.PROTECT)
    user_name = models.CharField(max_length=64, blank=False, null=True)
    team_name = models.ForeignKey(Team, on_delete=models.PROTECT, null=True)
    def __str__(self):
        return self.user.username


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
    team = models.ForeignKey(Team, on_delete=models.PROTECT, null=True)
    
    program = models.ForeignKey(Program, on_delete=models.PROTECT, null=True)
    contact = models.CharField(max_length=64)
 
    Image = models.CharField(max_length=64)
    KeyName = models.CharField(max_length=64)
    flavor = models.ForeignKey(Flavor, on_delete=models.PROTECT, null=True)
    users = models.ForeignKey(UserProfile, on_delete=models.PROTECT, null=True)
    contact = models.CharField(max_length=64, unique=True)
    id_instance = models.CharField(max_length=64, unique=True)
    launch_time = models.CharField(max_length=64, null=True)
    openstack_flavor_id = models.CharField(max_length=64, null=True)
    network = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return str(self.instance_name)

class Bill(models.Model):

    bill_name =  models.CharField(max_length=64)
    start_date = models.CharField(max_length=64)
    end_date = models.CharField(max_length=64)
    program =  models.CharField(max_length=64)
    team =  models.CharField(max_length=64)
    total_cost = models.CharField(max_length=64)
    Unit =  models.CharField(max_length=64)
 
def __str__(self):
        return str(self.start_date)
