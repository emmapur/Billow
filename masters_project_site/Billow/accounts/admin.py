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
admin.site.register(Op_image)
admin.site.register(aws_image)
admin.site.register(snapshot_instance)
admin.site.register(Instance_snap_ind)


