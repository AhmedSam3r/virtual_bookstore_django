from django.db import models
from django.db.models import Avg


class Category(models.Model):
    """Category model"""
    name = models.CharField(max_length=300, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return (self.name)


class Book(models.Model):
    """
    Book Model
    TODO:
        create a publisher & foreign key
        create an author table with M2M
    """
    title = models.CharField(max_length=500, db_index=True)
    isbn = models.CharField(max_length=500, unique=True)
    author = models.CharField(max_length=255)
    publication_date = models.DateField()
    # Forward Relation & Reverse relation
    category = models.ForeignKey(to=Category,
                                 related_name='books_category',
                                 null=True,
                                 on_delete=models.deletion.SET_NULL)
    page_count = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=6)
    readers_count = models.PositiveBigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    @property
    def num_of_reviews(self) -> int:
        return self.book_reviews.count()

    @property
    def average_rating(self) -> float:
        return self.book_reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    def __str__(self) -> str:
        return str(self.title)


# TODO add intermediate table for the M2M between User and book for readings
# TODO more descriptive name ('users.User')
# class BookReading(models.Model):
#     pass
