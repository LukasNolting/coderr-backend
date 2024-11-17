from django.urls import path, include
from .views import BaseInfoView
from offers_app.views import OfferDetailView
from orders_app.views import OrderCountView, CompletedOrderCountView
from profile_app.views import ProfileView
from auth_app.views import LoginView, RegisterView, RequestPasswordReset, PasswordResetView, VerifyTokenView

urlpatterns = [ 
    path('offers/', include('offers_app.urls')),   
    path('offerdetails/<int:pk>/', OfferDetailView.as_view()),
    path('orders/', include('orders_app.urls')),
    path('order-count/<int:pk>/', OrderCountView.as_view()),
    path('completed-order-count/<int:pk>/', CompletedOrderCountView.as_view()),
    path('base-info/', BaseInfoView.as_view()),
    path('profile/<int:pk>/', ProfileView.as_view()),
    path('profiles/', include('profile_app.urls')),
    path('reviews/', include('review_app.urls')),
    path('login/', LoginView.as_view()),
    path('password-reset/', RequestPasswordReset.as_view(), name='password_reset'),
    path('password-reset/<token>/', PasswordResetView.as_view(), name='password_reset_token'),
    path('authentication/', VerifyTokenView.as_view(), name='verify_token'),
    path('registration/', RegisterView.as_view()),
]