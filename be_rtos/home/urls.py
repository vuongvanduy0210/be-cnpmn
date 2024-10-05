from django.urls import path

from home import views

app_name = 'home'

urlpatterns = [
    path('my', views.MyHomeView.as_view(), name='my_home'),
    path('my/update', views.UpdateHomeView.as_view(), name='update_home'),
    path('device/<str:id>/update/', views.UpdateDeviceView.as_view(), name='toggle_device'),
]
