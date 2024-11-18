from rest_framework import serializers
from rest_framework import status

from .models import Review

from bookstore.exceptions import APIExceptionErr
import bleach
# from django.utils.html import escape


class ReviewSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        user = self.context['request'].user
        if not user.verified:
            raise APIExceptionErr('verify your account first',
                                  status_code=status.HTTP_403_FORBIDDEN)
        description = attrs["description"]
        if self.sanitize_input(description) != description:
            raise APIExceptionErr('please enter valid description, avoid use non alphabet charachters',
                                  status.HTTP_400_BAD_REQUEST)

        return super().validate(attrs)

    def sanitize_input(self, text):
        """sanitising HTML fragments to use in an HTML context–not for use in HTML attributes, CSS, JavaScript"""
        sanitized_text = bleach.clean(text, tags=[], attributes={})
        return sanitized_text

    class Meta:
        model = Review
        fields = '__all__'
        extra_fields = ['average_rating']


class ReviewCreateSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        user = self.context['request'].user
        if not user.verified:
            raise APIExceptionErr('verify your account first',
                                  status_code=status.HTTP_403_FORBIDDEN)

        validated_data['user'] = user
        return super().create(validated_data)

    class Meta:
        model = Review
        fields = ['id', 'description', 'rating', 'book']
