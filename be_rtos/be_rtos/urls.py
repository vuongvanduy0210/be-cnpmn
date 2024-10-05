"""
URL configuration for be_rtos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import authentication
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


# Swagger
swagger_patterns = path('api/schema/', include([
    path('', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
]))


api_patterns = path('api/', include([
    path('user/', include('user.urls')),
    path('home/', include('home.urls')),
    path('notifications/', include('notifications.urls')),
]))

urlpatterns = [
    api_patterns,
    swagger_patterns,
    path('admin/', admin.site.urls),
]