from django.db import models
from django.contrib import auth
from django.utils import timezone
import django

class Instance(models.Model):

    cloud_provider = models.CharField(max_length=64, unique=True)
    instance_name = models.CharField(max_length=64, unique=True)
    team = models.CharField(max_length=64, unique=True)
    #reference = models.CharField(max_length=64, unique=True)
    program = models.CharField(max_length=64, unique=True)
    contact = models.CharField(max_length=64, unique=True)
    #created_by = models.CharField(max_length=64, unique=True)
    Image = models.CharField(max_length=64, unique=True)
    KeyName = models.CharField(max_length=64, unique=True)
    flavor = models.CharField(max_length=64, unique=True)
    users = models.CharField(max_length=64, unique=True)
    contact = models.CharField(max_length=64, unique=True)


    def __str__(self):
        return str(self.instance_name)

class Cloud_Provider(models.Model):

    cloud_prov_name = models.CharField(max_length=64, unique=True)
    #auth_method = models.CharField(max_length=64, unique=True)
#    active = models.BooleanField(default=True) ??

    def __str__(self):
        return self.cloud_prov_name

class Team(models.Model):

    team_name = models.CharField(max_length=64, unique=True)
    program_name = models.CharField(max_length=64, unique=True)
    point_of_contact = models.CharField(max_length=64, unique=True)
    network_code = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.team_name

class User(models.Model):

    username = models.CharField(max_length=64, unique=True)
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
    role_name = models.CharField(max_length=64, unique=True)
    role_type = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.role_name

class Flavor(models.Model):
    flavor_name = models.CharField(max_length=64, unique=True)
    CPU = models.CharField(max_length=32, blank=True, null=True)
    Storage = models.CharField(max_length=32, blank=True, null=True)
    Ram = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return self.flavor_name

class Program(models.Model):
    program_name = models.CharField(max_length=64, unique=True)
    budget = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.program_name

class Image(models.Model):
    Image_name = models.CharField(max_length=64, unique=True)
    Image_ID = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.Image_name

class Key(models.Model):
    key_name = models.CharField(max_length=64, unique=True)
    key_name_ID = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.key_name
