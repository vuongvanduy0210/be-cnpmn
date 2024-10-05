from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.serializers import ValidationError
import json
from notifications import models


class NotificationCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField()
    data = serializers.DictField()
    class Meta:
        model = models.Notification
        fields = ['title', 'body', 'user_id', 'data']
        
    def to_representation(self, instance):
        data = {}
        data['title'] = instance.title
        data['body'] = instance.body
        data['created_at'] = instance.created_at
        data['user_id'] = instance.user_id
        data['data'] = json.loads(instance.data)
        return data
        
    def create(self, validated_data):
        new_data = validated_data
        new_data['data'] = json.dumps(validated_data['data'])
        notification = models.Notification(**new_data)
        notification.user = get_user_model().objects.get(pk=new_data['user_id'])
        try :
            notification.save()
            notification.send()
            return notification
        except Exception as e:
            raise ValidationError(e)
        

class NotificationListSerializer(serializers.ModelSerializer):
    data = serializers.DictField()    
    def to_representation(self, instance):
        data = {}
        data['title'] = instance.title
        data['body'] = instance.body
        data['created_at'] = instance.created_at
        data['user_id'] = instance.user_id
        data['data'] = json.loads(instance.data)
        return data

    class Meta:
        model = models.Notification
        fields = ['title', 'body', 'created_at', 'user_id', 'data']