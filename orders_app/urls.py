from django.urls import path
from .views import OrderAPIView, OrderCountAPIView, CompletedOrderCountAPIView

urlpatterns = [
    path('', OrderAPIView.as_view(), name='order-list-create'),  # GET / POST
    path('<int:pk>/', OrderAPIView.as_view(), name='order-detail'),  # GET / PATCH / DELETE für eine Bestellung
    path('order-count/<int:pk>/', OrderCountAPIView.as_view(), name='order-count'),
    path('completed-order-count/<int:pk>/', CompletedOrderCountAPIView.as_view(), name='completed-order-count'),
]

