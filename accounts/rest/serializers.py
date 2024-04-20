from accounts.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('full_name', 'email', 'mobile_number')


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,
                                     style={'input_type': 'password', 'placeholder': 'Password'})

    class Meta:
        model = User
        fields = ('full_name', 'email', 'mobile_number', 'password')

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.save_password(validated_data.get('password'))
        return user


class UserRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('full_name', 'email', 'mobile_number')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_id'] = str(user.id)
        return token
