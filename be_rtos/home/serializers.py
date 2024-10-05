from django.conf import settings
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.serializers import ValidationError, SerializerMethodField
from core.logger import logger
from home import models

import paho.mqtt.publish as publish
from paho import mqtt
import json

class RoomSerializer(serializers.ModelSerializer):
    devices = SerializerMethodField()
    
    def get_devices(self, obj: models.Room):
        db_devices = models.Device.objects.filter(room=obj)
        return DeviceSerializer(db_devices, many=True).data
    
    class Meta:
        model = models.Room
        fields = ['id', 'name', 'devices']
        

class MyHomeSerializer(serializers.ModelSerializer):
    # create a serializer for the Home model with its rooms
    rooms = SerializerMethodField()
    
    def get_rooms(self, obj: models.Home):
        db_rooms = models.Room.objects.filter(home=obj)
        return RoomSerializer(db_rooms, many=True).data
    
    class Meta:
        model = models.Home
        fields = ['id', 'address', 'rooms']
    


class UpdateMyHomeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Home
        fields = ['address']
        
    def update(self, instance: models.Home, validated_data: dict):
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        return instance
    

class DeviceSerializer(serializers.ModelSerializer):
    device_type = SerializerMethodField()
    
    def get_device_type(self, obj: models.Device):
        return obj.type.name
    
    class Meta:
        model = models.Device
        fields = ['id', 'name', 'is_auto', 'device_type', 'value']
        

class UpdateDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Device
        fields = ['is_auto', 'value']
        
    
    def validate(self, attrs):
        device = self.instance
        if (device.type.name in ['bulb', 'water'] and not (attrs.get('value') == 0 or attrs.get('value') == 1)):
            raise ValidationError('Value must be an integer')
        
        return super().validate(attrs)
        
    def update(self, instance: models.Device, validated_data: dict):
        instance.is_auto = validated_data.get('is_auto', instance.is_auto)
        value = float(validated_data.get('value', instance.value))
        if (instance.type.name in ['bulb', 'water', 'fan'] and isinstance(value, int)):
            raise ValidationError('Value must be an integer')
        instance.value = value
        instance.save()
        devices = models.Device.objects.filter(room__home__id=instance.room.home.id)
        logger.info(f"devices: {devices}")
        payload = {
            device.id: {
                "v": 1 if device.value == 0.0 else 0,
                "a": 1 if device.is_auto else 0
            }
            for device in devices if device.type.name in ['bulb', 'water', 'fan']
        }
        publish.single(settings.CONTROL_TOPIC, payload=json.dumps(payload), qos=0, retain=False, hostname=settings.MQTT_SERVER,
           port=settings.MQTT_PORT, client_id="", keepalive=60, will=None, auth=settings.MQTT_AUTH,
           tls=settings.MQTT_TLS)
        return instance