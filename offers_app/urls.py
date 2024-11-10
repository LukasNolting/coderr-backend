from django.urls import path
from .views import OfferView

urlpatterns = [ 
    path('', OfferView.as_view()),
    path('<int:pk>', OfferView.as_view()),
]