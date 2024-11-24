from rest_framework.generics import (
    ListAPIView, CreateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status


from .serializers import (
    ReviewSerializer, ReviewCreateSerializer,
)
from .models import Review
from booksvault.models import Book
from users.permissions import IsVerifiedUser


class ReviewListView(ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsVerifiedUser]
    pagination_class = PageNumberPagination
    lookup_field = 'book_id'

    def get_queryset(self):
        book_id = self.kwargs['book_id']
        return Review.objects.filter(book__id=book_id)

    def get_average_rating(self) -> float:
        book_id = self.kwargs.get('book_id')
        try:
            book = Book.objects.get(id=book_id)
            average_rating = book.average_rating
        except Book.DoesNotExist:
            average_rating = 0.0

        return average_rating

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        average_rating = self.get_average_rating()
        response.data.update({'average_rating': average_rating})
        return Response(response.data, status=status.HTTP_200_OK)


class ReviewSubmitView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated, IsVerifiedUser]
    pagination_class = PageNumberPagination

    # def perform_create(self, serializer):
    #     user = self.request.user
    #     return serializer.save(user=user)
