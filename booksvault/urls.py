from django.urls import path
from .views import (
    BookListView,
    BookDetailListView
)
urlpatterns = [
    path('list/', BookListView.as_view(), name='books_list'),
    path('<int:pk>/details/', BookDetailListView.as_view(),
         name='book_details'),
]
