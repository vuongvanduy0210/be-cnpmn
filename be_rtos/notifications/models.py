from typing import Iterable
from django.db import models
import firebase_admin
from firebase_admin import messaging
import json
from core.logger import logger
from core import exception
from django.core.exceptions import ValidationError, FieldError

with open('./notifications/google-credentials.json') as file:
    json_cred = json.load(file)

credential = firebase_admin.credentials.Certificate(json_cred)
firebase_app = firebase_admin.initialize_app(credential)

class Notification(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    data = models.TextField(null=True, blank=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def send(self):
        if (self.user.fcm_token is None) or (self.user.fcm_token == ''):
            logger.info(f"FCM token is empty for {self.user.email}")
            return
        data = json.loads(self.data)
        logger.info(type(data))
        message = messaging.Message(
            notification=messaging.Notification(
                title=self.title,
                body=self.body
            ),
            data=data,
            token=self.user.fcm_token
        )
        response = messaging.send(message)
        logger.info(f"Notification sent to {self.user.email}")
        return response
    
    
    def post_save(self):
        self.send()