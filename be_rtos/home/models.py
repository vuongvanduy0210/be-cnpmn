from django.db import models
import shortuuid
from user.models import User
from uuid import uuid4
from shortuuidfield import ShortUUIDField
 
    
class Home(models.Model):
    id = models.UUIDField(unique=True, default=uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
            
    def __str__(self):
        return self.address
    

class Room(models.Model):
    id = models.UUIDField(unique=True, default=uuid4, editable=False, primary_key=True)
    home = models.ForeignKey(Home, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False)
    def __str__(self):
        return self.name


class DeviceType(models.Model):
    id = models.UUIDField(unique=True, default=uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    
    def __str__(self):
        return self.name



class Device(models.Model):
    id = ShortUUIDField(unique=True, editable=False, primary_key=True, max_length=10)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False)
    type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    is_auto = models.BooleanField(default=False)
    value = models.FloatField(default=0)
    
    def __str__(self) -> str:
        return self.name
    