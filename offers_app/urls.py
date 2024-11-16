from django.urls import path
from .views import OfferView, OfferDetailView

urlpatterns = [ 
    path('', OfferView.as_view(), name='offer-list'),
    path('<int:pk>/', OfferView.as_view(), name='offer-detail'),
    path('details/<int:pk>/', OfferDetailView.as_view(), name='offer-detail-view'),
]