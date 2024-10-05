from core import logger
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from user import models

User = get_user_model()
    

class UserCreateSerializer(UserCreateSerializer):

    email = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField(write_only=True)
    gender =serializers.BooleanField(default=False)
    date_of_birth = serializers.DateField(allow_null=False)
    is_staff = serializers.BooleanField(default = False)
    fcm_token = serializers.CharField(allow_null=True, allow_blank=True)
    
    def create(sefl, validated_data: dict) -> models.User:
        validated_data['email'] = validated_data['email'].lower()
        password_candidate = validated_data['password']
        user = models.User(**validated_data)
        user.set_password(password_candidate)
        
        try:
            user.save()
            return user
        except Exception:
            raise ValidationError('Registration Error')
    
    class Meta:
        model = models.User
        fields = [
            'email', 'password', 'date_of_birth', 'is_staff', 'gender', 'first_name', 'last_name',  'fcm_token'
        ]
        
        
class LoginEmailSerializer(TokenObtainPairSerializer):
    fcm_token = serializers.CharField(allow_null=True)
    
    def validate(self, attrs):
        attrs['email'] = attrs['email'].lower()
        data = super().validate(attrs)
        user = models.User.objects.get(email=attrs['email'])
        user.fcm_token = attrs.get('fcm_token', None)
        user.save()
        return data
        

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['email', 'first_name', 'last_name', 'date_of_birth', 'gender', 'id', 'fcm_token']
        
    
class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True, write_only=True, allow_blank=False)
    new_password = serializers.CharField(required=True, write_only=True, allow_blank=False)
    
    def create(self, validated_data: dict) -> models.User:
        user = self.context['request'].user
        old_password = validated_data['old_password']
        new_password = validated_data['new_password']
        
        if not user.check_password(old_password):
            raise ValidationError('Old password is incorrect')
        user.set_password(new_password)
        user.save()
        return user

    class Meta:
        model = models.User
        fields = ['old_password', 'new_password']
    

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'fcm_token']
        