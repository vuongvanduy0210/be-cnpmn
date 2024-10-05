from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create_user'),
    path('auth/', views.LoginEmailView.as_view(), name='auth_token'),
    path('me/', views.MyDetailView.as_view(), name='me'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('update-details/', views.UpdateDetailsView.as_view(), name='update_details'),
    path('refresh-token/', views.TokenPairRefreshView.as_view(), name='refresh_token'),
]
