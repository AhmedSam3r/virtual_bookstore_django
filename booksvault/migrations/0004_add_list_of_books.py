# Generated by Django 5.1 on 2024-11-16 12:25

from django.db import migrations
from faker import Faker
import random

from booksvault.models import Category, Book


def add_books(apps, schema_editor):
    faker_object = Faker()

    categories = list(Category.objects.all())
    if not categories:
        print("NO CATEGORIES FOUND")

    authors = [faker_object.name() for _ in range(100)]
    books_list = []
    list_length = 1000
    for _ in range(list_length):
        book = Book(
            title=faker_object.sentence(nb_words=5),
            isbn=faker_object.isbn13(),
            author=random.choice(authors),
            publication_date=faker_object.date_between(
                start_date='-10y', end_date='today'),
            category=random.choice(categories),
            page_count=random.randint(100, 1000),
            price=round(random.uniform(5.0, 500.0), 2),
        )
        books_list.append(book)

    Book.objects.bulk_create(books_list, batch_size=list_length)


class Migration(migrations.Migration):

    dependencies = [
        ('booksvault', '0003_book'),
    ]

    operations = [
        migrations.RunPython(add_books,)
    ]