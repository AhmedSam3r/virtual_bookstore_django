from django.urls import path
from .views import (
    UserRegisterView, UserLoginView,
    CustomTokenVerifyView,
    CustomTokenRefreshView,
)

urlpatterns = [
    # TODO later on we can move auth endpoints into separate myauth_app
    path('auth/register/', UserRegisterView.as_view(), name='auth_register'),
    path('auth/login/', UserLoginView().as_view(), name='auth_login'),
    path('auth/token/verify/', CustomTokenVerifyView.as_view(),
         name='auth_token_verify'),
    # TODO add verify email endpoint
    path('auth/token/refresh/', CustomTokenRefreshView.as_view(),
         name='auth_token_refresh'),
]
