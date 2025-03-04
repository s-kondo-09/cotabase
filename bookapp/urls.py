from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('bookapp/', views.ListBookView.as_view(), name='list-book'),
    path('bookapp/<int:pk>/detail/', views.DetailBookView.as_view(), name='detail-book'),
    path('bookapp/create/', views.CreateBookView.as_view(), name='create-book'),
    path('bookapp/<int:pk>/delete/', views.DeleteBookView.as_view(), name='delete-book'),
    path('bookapp/<int:pk>/update/', views.UpdateBookView.as_view(), name='update-book'),
    path('bookapp/<int:book_id>/review/', views.CreateReviewView.as_view(), name='review-book'),
    path('bookapp/<int:book_id>/answer/', views.CreateAnswerView.as_view(), name='answer-book'),
]
