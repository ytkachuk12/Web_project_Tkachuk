"""DRF serializers:
    - registration serializer
    - login serializer
"""
import re

from rest_framework import serializers
from django.contrib.auth import authenticate

from authentication.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """DRF serializer for register new user (User model)"""
    password = serializers.CharField(max_length=121, min_length=8, write_only=True)

    def validate_password(self, value):
        """Validate password:
            - password must contain at least 1 uppercase letter
            - password must contain at least ONE digit"""
        if not re.findall('[A-Z]', value):
            raise serializers.ValidationError("The password must contain at least 1 uppercase letter, A-Z.")
        if not re.findall('\d', value):
            raise serializers.ValidationError("The password must contain at least ONE digit, 0-9.")
        return value

    class Meta:
        model = User
        """Set all fields that should be serialized
            all fields has relation to model  User"""
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        """Create new user in DB"""
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """DRF serializer for user's login"""
    email = serializers.CharField(max_length=127)
    password = serializers.CharField(max_length=127, write_only=True)

    def validate(self, data):
        """Check is email valid
        Check is password valid
        Check are email and pass match some user"""
        email = data.get('email', None)
        password = data.get('password', None)

        if not email:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        # The 'authenticate' Django's method checks that the provided email and password match some user.
        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )
        # Check did user deactivate or block
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'email': user.email,
        }
