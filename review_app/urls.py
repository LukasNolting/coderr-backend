from django.urls import path
from .views import ReviewView
    

urlpatterns = [
    path('', ReviewView.as_view(), name='review-list-create'),
    path('<int:pk>/', ReviewView.as_view(), name='review-detail'),
]