from django.forms import ValidationError
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from home import models
from .serializers import MyHomeSerializer, RoomSerializer, UpdateMyHomeSerializer, DeviceSerializer,UpdateDeviceSerializer
from rest_framework import generics, status, views
from core import exception

class MyHomeView(generics.RetrieveAPIView):
    serializer_class = MyHomeSerializer
    permisison_classes = [IsAuthenticated]
    
    def get_object(self):
        home =  models.Home.objects.filter(user=self.request.user).first()
        if not home:
            raise exception.get(
                ValidationError, message='Home not found', status='404'
            )
        return home
    

class UpdateHomeView(generics.UpdateAPIView):
    serializer_class = UpdateMyHomeSerializer
    permission_classes = [IsAuthenticated]
    allowed_methods = {'PATCH'}
    
    def get_object(self):
        return models.Home.objects.get(user=self.request.user)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    
class RoomListView(generics.ListAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return models.Room.objects.filter(home__user=self.request.user)
    

class DeviceListView(generics.ListAPIView):
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return models.Device.objects.filter(room_id=self.kwargs['id'])
    

class UpdateDeviceView(generics.UpdateAPIView):
    serializer_class = UpdateDeviceSerializer
    permission_classes = [IsAuthenticated]
    allowed_methods = {'PATCH'}
    
    def get_object(self):
        return models.Device.objects.get(id=self.kwargs['id'])
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

