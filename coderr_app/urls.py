from django.urls import path, include
from .views import BaseInfoView, InitDBService
from offers_app.views import OfferDetailView
from profile_app.views import BusinessProfileView, CustomerProfileView
from auth_app.views import LoginView, RegisterView, RequestPasswordReset, PasswordResetView, VerifyTokenView
# SETTINGS.PY die APPS ergänzen

urlpatterns = [ 
    path('offers/', include('offers_app.urls')), 
    path('offerdetails/<int:pk>/', OfferDetailView.as_view(), name='offer-detail-view'),
    path('orders/', include('orders_app.urls')),
    path('base-info/', BaseInfoView.as_view(), name='base-info'),
    path('init-db/', InitDBService.as_view(), name='init-db'),
    path('profile/', include('profile_app.urls')),
    path('profiles/business/', BusinessProfileView.as_view()),
    path('profiles/customer/', CustomerProfileView.as_view()),
    path('reviews/', include('review_app.urls')),
    path('login/', LoginView.as_view()),
    path('password-reset/', RequestPasswordReset.as_view(), name='password_reset'),
    path('password-reset/<token>/', PasswordResetView.as_view(), name='password_reset_token'),
    path('authentication/', VerifyTokenView.as_view(), name='verify_token'),
    path('registration/', RegisterView.as_view()),
]