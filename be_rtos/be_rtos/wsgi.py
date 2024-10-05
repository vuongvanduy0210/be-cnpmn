"""
WSGI config for be_rtos project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from be_rtos.mqtt_consumer import Smarthome
from core.logger import logger
import django
from django.conf import settings
from django.core.wsgi import get_wsgi_application

FIRE_ALARM_CHANNEL = 'fire_alarm'
DEVICE_CHANNEL = 'device'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'be_rtos.settings')
django.setup()

application = get_wsgi_application()

consumer = Smarthome()
consumer.daemon = True
consumer.start()