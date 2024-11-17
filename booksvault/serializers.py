from rest_framework import serializers

from .models import Book, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'isbn', 'author',
            'publication_date', 'price'
        ]


class BookDetailsSerializer(serializers.ModelSerializer):
    category_name = CategorySerializer(source='category', read_only=True)

    class Meta:
        model = Book
        fields = '__all__'
