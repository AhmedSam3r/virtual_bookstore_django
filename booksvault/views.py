from rest_framework import exceptions
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView,
)
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from .serializers import (
    BookSerializer, BookDetailsSerializer,
)
from rest_framework.pagination import PageNumberPagination
from .models import Book
from bookstore.exceptions import APIExceptionErr


class BookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        user = self.request.user
        if not user.verified:
            raise APIExceptionErr('not allowed',
                                  code=status.HTTP_403_FORBIDDEN)
        return super().list(request, *args, **kwargs)


class BookDetailListView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def retrieve(self, request, *args, **kwargs):
        try:
            response = super().retrieve(request, *args, **kwargs)
        except exceptions.NotFound as _:
            raise APIExceptionErr(detail='not found',
                                  code=status.HTTP_404_NOT_FOUND)

        return response
