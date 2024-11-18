from django.contrib import admin

from .models import Review


@admin.register(Review)
class UserCustomAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('id', 'description', 'rating', 'display', 'book', 'user',
                    'created_at', 'updated_at',)
    search_fields = ('book__title', 'book__author')
    raw_id_fields = ('book', 'user', )
    list_filter = ('created_at', 'rating',)
    ordering = ('id',)
