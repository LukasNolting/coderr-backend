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
    path('activate/<uidb64>/<token>/', activate_user, name='activate_user'),
    path('password-reset/', RequestPasswordReset.as_view(), name='password_reset'),
    path('password-reset/<token>/', PasswordResetView.as_view(), name='password_reset_token'),
    path('authentication/', VerifyTokenView.as_view(), name='verify_token'),
]