import re
from typing import Tuple, Optional

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ValidationError


from core import exception


def create_user(params):
    return get_user_model().objects.create(**params)


def email_validator(value):
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', value):
        raise exception.get_list_error(ValidationError, _('Invalid email format'))
    return value


def phone_validator(value):
    if not re.match(r'^\+?1?\d{9,15}$', value):
        raise exception.get_list_error(ValidationError, _('Invalid phone number format'))
    return value