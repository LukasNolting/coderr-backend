from django.urls import path, include
from .views import (
    LoginView,
    RegistrationView
)


urlpatterns = [ 
    path('login/', LoginView.as_view()),
    path('registration/', RegistrationView.as_view()),
]