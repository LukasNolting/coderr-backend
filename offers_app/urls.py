from django.urls import path
from .views import OfferAPIView, OfferDetailView
urlpatterns = [
    path('', OfferAPIView.as_view(), name='offer-list'),
    path('<int:pk>/', OfferAPIView.as_view(), name='offer-detail'),
]