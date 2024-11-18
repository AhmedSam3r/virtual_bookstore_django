import pytest
from rest_framework import status
# from rest_framework.test import APIClient
from rest_framework.utils.serializer_helpers import ReturnList
from django.db import IntegrityError
from django.urls import reverse
from reviews.models import Review
from .utils import (
    create_book, create_review, create_user,
)


@pytest.mark.django_db
class TestReviewModel:

    def test_review_success_creation(self):
        book = create_book()
        user = create_user()
        data = {
            'description': 'Excellent Product!',
            'book': book,
            'user': user,
            'rating': 3
        }
        review = Review.objects.create(**data)
        assert review is not None
        assert review.rating == data['rating']
        assert review.book.id == book.id
        assert Review.objects.count() == 1

    def test_review_fail_creation(self, api_client):
        book = create_book()
        user = create_user()
        data = {
            'description': 'Excellent Product!',
            'book': book,
            'rating': 5,
            'user': user
        }
        review_1 = Review.objects.create(**data)
        assert review_1 is not None
        assert review_1.book.id == book.id
        try:
            review_2 = Review.objects.create(**data)
            assert False
        except IntegrityError as _:
            pass
