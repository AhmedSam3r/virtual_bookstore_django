import pytest
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient

from users.models import User


@pytest.mark.django_db
class TestUserRefreshToken:
    refresh_url = reverse('auth_token_refresh')
    login_url = reverse('auth_login')
    user_email = 'testuser@example.com'
    user_password = 'securepassword123'
    login_response = None

    @pytest.fixture
    def client(self):
        """Fixture to instantiate APIClient."""
        yield APIClient()

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

    @pytest.fixture
    def login_and_get_tokens(self, client: APIClient):
        """Helper method to log in and retrieve access and refresh tokens."""
        login_response = client.post(
            self.login_url,
            {'email': self.user_email, 'password': self.user_password},
            format='json'
        )
        assert login_response.status_code == status.HTTP_200_OK
        assert 'refresh' in login_response.data
        assert 'access' in login_response.data

        self.login_response = login_response

    @pytest.mark.django_db
    def test_refresh_token_valid(self, create_user, client: APIClient, login_and_get_tokens):
        """Test refreshing an access token with a valid refresh token using verified user."""
        # get valid login data after test
        # login_response = self.login_and_get_tokens(client, self.user_email, self.user_password)
        refresh_token = self.login_response.data.get('refresh')
        refresh_response = client.post(self.refresh_url,
                                       data={'refresh': refresh_token},
                                       format='json')

        assert refresh_response.status_code == status.HTTP_200_OK
        assert 'access' in refresh_response.data
        assert 'refresh' in refresh_response.data

    @pytest.mark.django_db
    def test_refresh_token_invalid(self, client: APIClient):
        """Test refreshing an access token with an invalid refresh token."""
        invalid_refresh_response = client.post(self.refresh_url,
                                               {'refresh': 'invalidtoken123'},
                                               format='json')

        assert invalid_refresh_response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'detail' in invalid_refresh_response.data

    def test_rotating_refresh_token(self, create_user, client: APIClient, login_and_get_tokens):
        """Test the rotating refresh token feature."""
        old_refresh_token = self.login_response.data['refresh']
        refresh_response = client.post(self.refresh_url,
                                       {'refresh': old_refresh_token},
                                       format='json')
        new_refresh_token = refresh_response.data['refresh']

        assert refresh_response.status_code == status.HTTP_200_OK
        assert 'refresh' in refresh_response.data
        assert new_refresh_token != old_refresh_token
        # TODO later make this case work
        # assert refresh_response.data['success'] is True

        # Ensure that old refresh tokens are blocked
        blocked_refresh_response = client.post(self.refresh_url,
                                               {'refresh': old_refresh_token},
                                               format='json')
        assert blocked_refresh_response.status_code == status.HTTP_401_UNAUTHORIZED
        assert blocked_refresh_response.data["detail"] == 'Token is blacklisted'
        assert blocked_refresh_response.data['success'] is False
