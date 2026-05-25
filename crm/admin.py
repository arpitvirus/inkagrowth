from django.contrib import admin

# Register your models here.
# admin.py

from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(Service)
admin.site.register(Client)
admin.site.register(Lead)
admin.site.register(FollowUp)
admin.site.register(Task)
admin.site.register(Payment)
admin.site.register(LeadNote)
admin.site.register(ClientFile)
admin.site.register(Communication)
admin.site.register(ActivityLog)