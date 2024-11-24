from rest_framework.response import Response
from rest_framework.generics import (
    CreateAPIView, GenericAPIView
)
from rest_framework import status
from rest_framework import permissions
from rest_framework_simplejwt.tokens import (
     RefreshToken,  # AccessToken,
)
from rest_framework.throttling import AnonRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenVerifyView
)


from .serializers import (
    UserSerializer, CustomTokenObtainPairSerializer
)
from .models import User
from .helpers import format_response_data
from .permissions import IsVerifiedUser
from bookstore.exceptions import APIExceptionErr
from users.throttling import (
    TokenRefreshThrottle, LoginThrottle
)


class UserRegisterView(CreateAPIView):
    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AnonRateThrottle]

    def _construct_response_data(self, user, serializer) -> dict:
        """
        Helper method to construct the response data.

        args:
            user: given user model field
            serializer: validated instance of UserSerializer class

        return dictionary of
            user: contains user data
            access: generated access token
            refresh: generated refresh token
            success: boolean flag for FE to check response data status
        """

        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        validated_data = serializer.validated_data
        validated_data.pop('password')
        result = {
            "user": {
                "email": user.email,
                "verified": user.verified
            },
            "access": str(access_token),
            # Grant the user refresh in case of verification
            # "refresh": str(refresh_token)
        }
        return format_response_data(result)

    def post(self, request, *args, **kwargs):
        try:
            # create user
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            # TODO We can add signal to send verification link for email
            user = serializer.save()

            # format response object
            response_data = self._construct_response_data(user, serializer)
        except ValidationError as e:
            raise APIExceptionErr(e.detail, e.status_code)

        return Response(data=response_data,
                        status=status.HTTP_201_CREATED)


class UserLoginView(GenericAPIView):
    serializer_class = CustomTokenObtainPairSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    throttle_classes = [LoginThrottle]
    queryset = User.objects.filter(verified=True)

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            response_data = serializer.validated_data
            response_data = format_response_data(response_data)
        except AuthenticationFailed as e:
            raise APIExceptionErr(e.detail, e.status_code)
        except ValidationError as e:
            raise APIExceptionErr(e.detail, e.status_code)

        return Response(data=response_data,
                        status=status.HTTP_200_OK)


class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = []
    throttle_classes = [AnonRateThrottle, TokenRefreshThrottle]

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenVerifyView(TokenVerifyView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsVerifiedUser]

    def post(self, request, *args, **kwargs):
        print("FIRST HERE")
        return super().post(request, *args, **kwargs)
