from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator


class Review(models.Model):
    """Review model"""
    book = models.ForeignKey('booksvault.Book',
                             on_delete=models.CASCADE,
                             related_name='book_reviews')
    user = models.ForeignKey('users.User',
                             on_delete=models.CASCADE,
                             related_name='user_reviews')
    description = models.TextField(validators=[MinLengthValidator(10),
                                               MaxLengthValidator(500)])
    rating = models.PositiveSmallIntegerField()
    display = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['book_id', 'user_id'],
                                    name='unique_user_book')
        ]
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
