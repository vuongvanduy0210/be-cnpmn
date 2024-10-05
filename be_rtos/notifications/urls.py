from django.urls import path

from notifications import views

urlpatterns = [
    path('create/', views.CreateNotificationView.as_view(), name='create_notification',),
    path('list/', views.GetNotificationListView.as_view(), name='list_notification')
]