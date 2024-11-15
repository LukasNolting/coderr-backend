from django.urls import path
from .views import ProfileView

urlpatterns = [    
    path('<int:pk>/', ProfileView.as_view()), 
]