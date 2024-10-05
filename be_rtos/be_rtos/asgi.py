"""
ASGI config for be_rtos project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
import django
from core.logger import logger

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'be_rtos.settings')

application = get_asgi_application()
