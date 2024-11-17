import pytest
from booksvault.models import Book, Category
from faker import Faker
import random
from django.db import IntegrityError


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
def create_book(**kwargs):
    categories = create_categories()
    assert len(categories) > 0
    book = Book.objects.create(**kwargs)
    return book


@pytest.mark.django_db
class TestBookModel:
    def create_book_object(self):
        faker_object = Faker()
        categories = create_categories()
        book_data = {
            "title": faker_object.sentence(nb_words=5),
            "isbn": faker_object.isbn13(),
            "author": faker_object.name(),
            "publication_date": faker_object.date_between(start_date='-10y', end_date='today'),
            "category": random.choice(categories),
            "page_count": random.randint(100, 1000),
            "price": round(random.uniform(5.0, 500.0), 2)
        }
        return book_data

    def test_add_book_success(self):
        book_object = self.create_book_object()
        book = create_book(**book_object)
        assert book.id is not None
        title = book_object['title']
        assert book.title == title
        assert Book.objects.get(title=title).id == book.id

    def test_add_book_fail(self):
        book_object = self.create_book_object()
        book = create_book(**book_object)
        assert book.id is not None
        try:
            Book.objects.create(**book_object)
            assert False, "IntegrityError was not raised"
        except IntegrityError:
            pass
