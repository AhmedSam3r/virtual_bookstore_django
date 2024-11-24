from rest_framework import serializers, exceptions, status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password

from bookstore.exceptions import APIExceptionErr
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'email', 'verified', 'last_login',
            'password'
        ]

    def validate_password(self, value):
        # NO need to for XSS protection
        # PW isn't display and it's hashed in the DB
        validate_password(value)  # Run the password validations
        return value

    # def validate_email(self, attrs):
        # TODO add oauth email to verify gmail for example
        # return super().validate(attrs)

    def validate(self, attrs):
        try:
            validated_data = super().validate(attrs)
        except exceptions.ValidationError as e:
            raise APIExceptionErr(e.detail, e.status_code)

        return validated_data

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = super().create(validated_data)
        return user

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     return response


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # assign self.user through authenticate() using email and pw
        # returns access & refresh token
        data = super().validate(attrs)
        if not self.user:
            raise exceptions.AuthenticationFailed(
                code=status.HTTP_401_UNAUTHORIZED)

        if self.user.verified is False:
            raise exceptions.PermissionDenied('Verify your account first',
                                              status.HTTP_403_FORBIDDEN)
        if self.user.blocked is True:
            raise exceptions.PermissionDenied('your account has been blocked',
                                              status.HTTP_403_FORBIDDEN)

        data['user'] = {
            'email': self.user.email,
            'verified': self.user.verified,
        }
        return data
