from rest_framework.throttling import UserRateThrottle


class TokenRefreshThrottle(UserRateThrottle):
    scope = 'auth_token_refresh'


class LoginThrottle(UserRateThrottle):
    scope = 'auth_login'
