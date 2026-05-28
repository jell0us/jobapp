from django.contrib import admin
from .models import Application, Job, UserDetail

# Register your models here.
admin.site.register(Application)
admin.site.register(Job)
admin.site.register(UserDetail)