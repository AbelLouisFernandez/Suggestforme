from django.contrib import admin
from .models import CustomUser,userwatchedstatus,anime
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(anime)
admin.site.register(userwatchedstatus)
