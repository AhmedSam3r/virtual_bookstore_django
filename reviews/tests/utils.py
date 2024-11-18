import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from reviews.models import Review
from faker import Faker
import random
from typing import List

from users.models import User
from booksvault.models import Book, Category


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.mark.django_db
def create_user(email='useremail@example.com',
                password='securepassword123', verified=True) -> User:
    user = User.objects.create_user(
        email=email, password=password,
        verified=verified
    )
    return user


@pytest.fixture
def authenticated_user(api_client):
    data = {'email': 'test@example.com', 'password': 'securepassword123'}
    create_user(data['email'], data['password'])
    response = api_client.post(reverse('auth_login'), data, format='json')
    access_token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'JWT {access_token}')


@pytest.mark.django_db
def create_categories() -> List[Category]:
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
def create_book() -> Book:
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
def create_review() -> Review:
    faker = Faker()
    user = create_user('reviewer@example.com', 'reviewpassword123')
    book = create_book()
    review = Review.objects.create(
        description=faker.sentence(nb_words=10),
        rating=random.randint(1, 5),
        user=user,
        book=book,
    )
    return review
