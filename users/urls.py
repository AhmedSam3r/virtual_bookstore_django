from django.urls import path
from .views import (
    UserListAPI, UserRegisterView, UserLoginView,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenVerifyView
)

urlpatterns = [
    # TODO later on we can move auth endpoints into separate myauth_app
    path('auth/register/', UserRegisterView.as_view(), name='auth_register'),
    path('auth/login/', UserLoginView().as_view(), name='auth_login'),
    path('auth/token/verify/', TokenVerifyView.as_view(),
         name='auth_token_verify'),
    path('auth/token/refresh/', TokenRefreshView.as_view(),
         name='auth_token_refresh'),

    path('list/', UserListAPI.as_view(), name='list-users'),
]
