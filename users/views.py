from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import (
    CreateAPIView
)
from rest_framework.status import (
    HTTP_201_CREATED, HTTP_200_OK
)
from rest_framework_simplejwt import authentication
from rest_framework import permissions

from rest_framework_simplejwt.tokens import (
     RefreshToken,  # AccessToken,
)
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from rest_framework.exceptions import ValidationError, AuthenticationFailed
from .serializers import (
    UserSerializer, CustomTokenObtainPairSerializer
)


from .models import User
from .helpers import format_response_data
from bookstore.exceptions import APIExceptionErr


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
            "refresh": str(refresh_token)
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
                        status=HTTP_201_CREATED)


class UserLoginView(CreateAPIView):
    serializer_class = CustomTokenObtainPairSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
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
                        status=HTTP_200_OK)
