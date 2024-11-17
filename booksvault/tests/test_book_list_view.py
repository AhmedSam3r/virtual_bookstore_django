import pytest
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.utils.serializer_helpers import ReturnList
from django.urls import reverse
from users.models import User
from booksvault.models import Book, Category
from faker import Faker
import random


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def create_user(email, password, verified=True):
    user = User.objects.create_user(
        email=email, password=password,
        verified=verified
    )
    return user


@pytest.mark.django_db
def update_user(user):
    user.verified = False
    user.save()
    return user


@pytest.fixture
def authenticated_user(api_client):
    data = {'email': 'test@example.com', 'password': 'securepassword123'}
    create_user(data['email'], data['password'])
    response = api_client.post(reverse('auth_login'), data, format='json')
    access_token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'JWT {access_token}')


@pytest.fixture
def unauthenticated_user(api_client):
    data = {'email': 'test@example.com', 'password': 'securepassword123'}
    user = create_user(data['email'], data['password'])
    response = api_client.post(reverse('auth_login'), data, format='json')
    access_token = response.data['access']
    update_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'JWT {access_token}')


@pytest.mark.django_db
def create_categories():
    categories_list = []
    categories = [
        'Fiction',
        'Non-Fiction',
        'Science',
        'Biography',
        'Mystery',
        'Fantasy',
        'History',
        'Romance',
        'Horror',
        'Children'
    ]
    for category in categories:
        category_object = Category.objects.get(name=category)
        if not category_object:
            category = Category.objects.create(name=category)
            categories_list.append(category)

    if not categories_list:
        categories_list = list(Category.objects.all())

    return categories_list


@pytest.mark.django_db
def create_book():
    categories = create_categories()
    assert len(categories) > 0

    faker_object = Faker()
    book = Book.objects.create(
        title=faker_object.sentence(nb_words=5),
        isbn=faker_object.isbn13(),
        author=faker_object.name(),
        publication_date=faker_object.date_between(
            start_date='-10y', end_date='today'),
        category=random.choice(categories),
        page_count=random.randint(100, 1000),
        price=round(random.uniform(5.0, 500.0), 2),
    )
    return book


@pytest.mark.django_db
class TestBookViews:
    login_url = reverse('auth_login')
    books_list_url = reverse('books_list')
    books_details_name = 'book_details'

    def test_book_empty_list(self, api_client, authenticated_user):
        create_book()
        response = api_client.get(self.books_list_url)
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert type(response.data.get('results')) is ReturnList
        # TODO fix this issue due to the 1,000 inserted book
        # assert len(response.data.get('results')) == 0

    def test_book_list(self, api_client, authenticated_user):
        create_book()
        response = api_client.get(self.books_list_url)
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        # TODO fix this issue due to the 1,000 inserted book
        # assert len(response.data.get('results')) == 1
        create_book()
        response = api_client.get(self.books_list_url)
        assert response.status_code == status.HTTP_200_OK
        assert type(response.data.get('results')) is ReturnList
        assert 'results' in response.data
        # TODO fix this issue due to the 1,000 inserted book
        # assert len(response.data.get('results')) == 2

    def test_unauthorized_user(self, api_client):
        create_book()
        response = api_client.get(self.books_list_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_unauthenticated_user(self, api_client, unauthenticated_user):
        create_book()
        response = api_client.get(self.books_list_url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
