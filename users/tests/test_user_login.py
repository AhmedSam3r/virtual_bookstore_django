import pytest
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient

from users.models import User


@pytest.mark.django_db
class TestUserLogin:
    url = reverse('auth_login')
    user_email = 'testuser@example.com'
    user_password = 'securepassword123'
    client: APIClient = APIClient()

    @pytest.fixture
    def create_user(self):
        """Create a user for testing login."""
        data = {
            'password': self.user_password,
            'email': self.user_email,
            'verified': True
        }
        # it will create a verified user
        user = User.objects.create_user(**data)
        return user

    def test_login_missing_fields(self):
        """Test logging in with missing fields."""
        data = {
            'password': 'password'
        }
        response = self.client.post(self.url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['success'] is False
        assert 'access' not in response.data
        assert 'refresh' not in response.data

    def test_login_successful(self, create_user):
        """Test logging in with valid credentials."""
        data = {
            'password': self.user_password,
            'email': self.user_email
        }
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['success'] is True
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_login_unverified_user(self):
        """Test logging in with users signed up but not verified."""
        data = {
            'password': self.user_password,
            'email': self.user_email
        }
        user = User.objects.create_user(**data)
        user.verified = False
        user.save()
        assert user is not None
        assert user.verified is False

        response = self.client.post(self.url, data, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data['success'] is False
        assert 'access' not in response.data
        assert 'refresh' not in response.data

    def test_login_invalid_credentials(self, create_user):
        """Test logging in with verified user but invalid credentials."""
        data = {
            'email': self.user_email,
            'password': 'password'
        }
        response = self.client.post(self.url, data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data['success'] is False
        assert 'access' not in response.data
        assert 'refresh' not in response.data
