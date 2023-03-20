from django.db import models
import django
from django.contrib.auth.models import User

#model for cloud provider
class Cloud_Provider(models.Model):
    cloud_prov_name = models.CharField(max_length=64, unique=True)

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
    program_name = models.ForeignKey(Program, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.user.username

class Flavor(models.Model):
    flavor_name = models.CharField(max_length=64, blank=False, null=False)
    CPU = models.CharField(max_length=32, blank=True, null=True)
    Storage_GB = models.CharField(max_length=32, blank=True, null=True)
    Ram_GB = models.CharField(max_length=32, blank=True, null=True)
    id_flavor = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return self.flavor_name





class Op_image(models.Model):
    image_name = models.CharField(max_length=64)
    Image_ID = models.CharField(max_length=64)

    def __str__(self):
        return self.image_name
        
class aws_image(models.Model):
    Image_name = models.CharField(max_length=64)
    Image_ID = models.CharField(max_length=64)

    def __str__(self):
        return self.Image_name


class Key(models.Model):
    key_name = models.CharField(max_length=64)

    def __str__(self):
        return self.key_name



class Instance(models.Model):

    cloud_provider = models.ForeignKey(Cloud_Provider, on_delete=models.PROTECT, null=True)
    instance_name = models.CharField(max_length=64, unique=True)
    team = models.ForeignKey(Team, on_delete=models.PROTECT, null=True)
    program = models.ForeignKey(Program, on_delete=models.PROTECT, null=True)
    contact = models.CharField(max_length=64, unique=False)
    Image_op =  models.ForeignKey(Op_image, on_delete=models.PROTECT, null=True)
    Image_aws =  models.ForeignKey(aws_image, on_delete=models.PROTECT, null=True)
    State = models.CharField(max_length=64, unique=False)
    KeyName =  models.ForeignKey(Key, on_delete=models.PROTECT, null=True)
    flavor = models.ForeignKey(Flavor, on_delete=models.PROTECT, null=True)
    users = models.ForeignKey(UserProfile, on_delete=models.PROTECT, null=True)
    id_instance = models.CharField(max_length=64, unique=True)
    launch_time = models.CharField(max_length=64, null=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    
    def __str__(self):
        return str(self.instance_name)

class Instance_snap_ind(models.Model):
    timestamp = models.DateTimeField()
    hash_key = models.CharField(max_length=64, default=None)  # hash of timestamp
    created = models.DateTimeField(editable=False, default=django.utils.timezone.now)
    modified = models.DateTimeField(default=django.utils.timezone.now)
    
    def __str__(self):
        return str(self.hash_key)

    
class snapshot_instance(models.Model):

    instance_snap_index_obj = models.ForeignKey(Instance_snap_ind, on_delete=models.CASCADE)
    cloud_provider = models.CharField(max_length=64, unique=False)
    team = models.CharField(max_length=64, unique=False)
    instance_name = models.CharField(max_length=64)
    program = models.CharField(max_length=64, unique=False)
    contact = models.CharField(max_length=64, unique=False)
    Image_op = models.CharField(max_length=64, unique=False)
    Image_aws = models.CharField(max_length=64, unique=False)
    KeyName =  models.CharField(max_length=64, unique=False)
    flavor = models.CharField(max_length=64, unique=False)
    users = models.CharField(max_length=64, unique=False)
    CPU = models.DecimalField(max_digits=10, decimal_places=2)
    State = models.CharField(max_length=64, unique=False)
    id_instance =models.CharField(max_length=64, unique=False)
    launch_time = models.CharField(max_length=64, null=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    daily_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)


    def __str__(self):
        return str(self.instance_name)



