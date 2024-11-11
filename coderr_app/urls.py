from django.urls import path, include
from .views import BaseInfoView
from offers_app.views import OfferDetailView
from orders_app.views import OrderCountView, CompletedOrderCountView
from profile_app.views import BusinessProfileView, CustomerProfileView

# SETTINGS.PY die APPS ergänzen

urlpatterns = [ 
    path('offers/', include('offers_app.urls')),   
    path('offerdetails/<int:pk>', OfferDetailView.as_view()),
    path('orders/', include('orders_app.urls')),
    path('order-count/<int:pk>', OrderCountView.as_view()),
    path('completed-order-count/<int:pk>', CompletedOrderCountView.as_view()),
    path('base-info/', BaseInfoView.as_view()),
    path('profile/', include('profile_app.urls')),
    path('profiles/business/', BusinessProfileView.as_view()),
    path('profiles/customer/', CustomerProfileView.as_view()),
    path('reviews/', include('review_app.urls')),
]