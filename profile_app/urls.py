from django.urls import path
from .views import BusinessProfileView, CustomerProfileView

urlpatterns = [    
    path('business/', BusinessProfileView.as_view()),
    path('customer/', CustomerProfileView.as_view()),
]