from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(ClientMaster)
admin.site.register(Candidate)
admin.site.register(DrvingLicence)
admin.site.register(Interview)