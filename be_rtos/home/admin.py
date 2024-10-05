from django.contrib import admin
from .models import Home, Room, DeviceType, Device

# Register your models here.
admin.site.register(Home)
admin.site.register(Room)
admin.site.register(DeviceType)
admin.site.register(Device)