import pytest
from rest_framework import status
from rest_framework.utils.serializer_helpers import ReturnList
from django.urls import reverse
from reviews.models import Review
from .utils import (
    create_book, create_review, create_user,
    api_client, authenticated_user
)


@pytest.mark.django_db
class TestReviewViews:
    review_submit_url = reverse('review_submit')

    def test_submit_review_success(self, api_client, authenticated_user):
        book = create_book()
        data = {
            'description': 'Great Product!',
            'book': book.id,
            'rating': 5
        }
        # {'id': 1, 'description': 'Great Product!', 'rating': 5, 'book': 1001}
        response = api_client.post(self.review_submit_url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert 'id' in response.data
        assert response.data['description'] == data['description']
        assert response.data['id'] == 1

    def test_submit_review_unauthenticated(self, api_client):
        book = create_book()
        data = {
            'description': 'Great Product!',
            'book': book.id,
            'rating': 5
        }
        response = api_client.post(self.review_submit_url, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_empty_review_view(self, api_client, authenticated_user):
        review_list_url = reverse('reviews_list', args=[3])
        response = api_client.get(review_list_url)
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert type(response.data.get('results')) is ReturnList
        assert len(response.data.get('results')) == 0

    def test_get_book_review(self, api_client, authenticated_user):
        review = create_review()
        review_list_url = reverse('reviews_list', args=[review.book.id,])
        response = api_client.get(review_list_url)
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert type(response.data.get('results')) is ReturnList
        assert len(response.data.get('results')) == 1
