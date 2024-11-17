from django.urls import path, include
from .functions import activate_user
from .views import (
    LoginView,
    RegisterView,
    RequestPasswordReset, 
    PasswordResetView,
    VerifyTokenView
)


urlpatterns = [ 
    path('login/', LoginView.as_view()),
    path('activate/<uidb64>/<token>/', activate_user, name='activate_user')
]