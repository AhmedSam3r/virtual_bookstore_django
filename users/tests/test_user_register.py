import pytest
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestUserRegister:
    url = reverse('auth_register')
    user_email = 'testuser@example.com'
    user_password = 'securepassword123'

    def test_register_user_success(self, client: APIClient):
        data = {
            'email': self.user_email,
            'password': self.user_password,
        }

        # Perform the POST request
        response = client.post(self.url, data, format='json')

        # Check if the response status code is HTTP 201 Created
        assert response.status_code == status.HTTP_201_CREATED
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert response.data['success'] is True
        assert 'user' in response.data
        assert response.data['user']['email'] == self.user_email
        assert response.data['user']['verified'] is False

    def test_register_user_missing_email(self, client: APIClient):
        data = {
            'password': self.user_password,
        }
        response = client.post(self.url, data, format='json')

        assert response.data['success'] is False
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        # Validate that the email field is required
        assert 'email' in response.data

    def test_password_validation(self, client: APIClient):
        data = {
            'email': self.user_email,
            'password': '123456',
        }
        response = client.post(self.url, data, format='json')

        assert response.data["success"] is False
        msg = 'This password is too short. It must contain at least 8 characters.' # NOQA 508
        assert msg in response.data["password"]
