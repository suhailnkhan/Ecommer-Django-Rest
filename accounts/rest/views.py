import json
from django.contrib.auth.models import Permission
from django.template import Context
from django.template.loader import get_template, render_to_string
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from accounts.constants import CUSTOMER_ROLE
# from accounts.email import EmailService
from accounts.models import User
from accounts.permission_constants import BLINKBUY_CUSTOMER
from accounts.rest.serializers import UserCreateSerializer , UserRetrieveSerializer , CustomTokenObtainPairSerializer
from accounts.utils import get_user_role_permission
from rest_framework.status import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



class UserCreateAPIView(CreateAPIView):
    def get_serializer_class(self):
        return UserCreateSerializer

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        password = request.data['password']
        user_type = "customer"
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        selected_permission = get_user_role_permission(user_type)
        (user_type)
        if not selected_permission:
            return Response({'error_messages': ['Please provide correct user role.']},
                            status=status.HTTP_400_BAD_REQUEST)
        role_permission = Permission.objects.get(codename=selected_permission)
        try : 
            instance = self.perform_create(serializer)
            instance.user_permissions.add(role_permission)
            instance.save_password(password)
        except Exception as e : 
            return Response({'error_messages': [e]},
                            status=status.HTTP_400_BAD_REQUEST)
        message = f'{user_type.title()} successfully added. '
        try:
            # mail = EmailService(user=instance, context={'password': password})
            # mail.send_welcome_email()
            # message += 'Welcome email has been sent.'
            pass
        except Exception as e:
            pass
        return Response({'message': message}, status=status.HTTP_201_CREATED)




class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return UserRetrieveSerializer

    def get_queryset(self):
            return User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        return Response(data)

  

class UserRolePermissions(APIView): 
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        return Response(['/'])