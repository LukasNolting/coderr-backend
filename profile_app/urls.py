from django.urls import path
from .views import BusinessProfileView, CustomerProfileView

urlpatterns = [    
    path('business/<int:pk>/', BusinessProfileView.as_view()),
    path('customer/<int:pk>/', CustomerProfileView.as_view()),
]