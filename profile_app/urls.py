from django.urls import path
from .views import BusinessProfileView, CustomerProfileView, ProfileView

urlpatterns = [
    path('business/', BusinessProfileView.as_view(), name='business-profile'),
    path('customer/', CustomerProfileView.as_view(), name='customer-profile'),
    path('<int:pk>/', ProfileView.as_view(), name='profile-detail'), 
]