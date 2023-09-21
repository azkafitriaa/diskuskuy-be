from django.contrib.auth import authenticate
from rest_framework import serializers

from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]

class UpdateCustomUserPhotoRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['photo_url']

class ProfileSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    name = serializers.CharField()
    nim = serializers.CharField()
    group = serializers.CharField()
    photo_url = serializers.CharField()

class LecturerCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'photo_url']

class LecturerSerializer(serializers.ModelSerializer):
    lecturer = LecturerCustomUserSerializer()

    class Meta:
        model = Lecturer
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs
    
class LoginResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
    user_id = serializers.IntegerField()
    role = serializers.CharField()
    group = serializers.CharField()
    photo_url = serializers.CharField()

class CustomGroupSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField()
    class Meta:
        model = CustomGroup
        fields = ('id', 'name')