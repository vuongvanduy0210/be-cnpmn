from rest_framework import generics
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken

from user import serializers
# Create your views here.

class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.UserCreateSerializer
    

class LoginEmailView(TokenObtainPairView):
    serializer_class = serializers.LoginEmailSerializer
    
    
class MyDetailView(generics.RetrieveAPIView):
    serializer_class = serializers.UserDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    

class ChangePasswordView(generics.CreateAPIView):
    serializer_class = serializers.ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]
    

class TokenPairRefreshView(TokenRefreshView):

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh = RefreshToken()
        response.data["refresh"] = str(refresh)
        return response
    

class UpdateDetailsView(generics.UpdateAPIView):
    serializer_class = serializers.UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    allowed_methods = {'PATCH'}
    
    def get_object(self):
        return self.request.user