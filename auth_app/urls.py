from django.urls import path, include
from .views import (
    LoginView,
    RegisterView
)


urlpatterns = [ 
    path('login/', LoginView.as_view()),
    path('registration/', RegisterView.as_view()),
]