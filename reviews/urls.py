from django.urls import path
from .views import (
    ReviewListView, ReviewSubmitView,
)
urlpatterns = [
    path('submit/', ReviewSubmitView.as_view(), name='review_submit'),
    path('book/<int:book_id>/', ReviewListView.as_view(), name='reviews_list'),

]
