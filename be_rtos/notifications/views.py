from typing import Any
from django.http import HttpRequest, HttpResponse
from rest_framework import generics
from rest_framework import permissions
from notifications import serializers
from .models import Notification
from rest_framework import filters

# Create your views here.

class CreateNotificationView(generics.CreateAPIView):
    serializer_class = serializers.NotificationCreateSerializer
    

class GetNotificationListView(generics.ListAPIView):
    serializer_class = serializers.NotificationListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    
    def get_queryset(self) -> Any:
        return Notification.objects.filter(user_id=self.request.user.pk).order_by('-created_at')