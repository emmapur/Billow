from __future__ import unicode_literals
from django.contrib import admin

from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Team)
admin.site.register(Cloud_Provider)
admin.site.register(Program)
admin.site.register(UserProfile)
admin.site.register(Flavor)
admin.site.register(Key)
admin.site.register(Instance)
admin.site.register(Openstack_image)
admin.site.register(Openstack_Network)
admin.site.register(Bill)