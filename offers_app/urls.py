from django.urls import path
from orders_app.views import OrderAPIView, OrderCountAPIView, CompletedOrderCountAPIView

urlpatterns = [
    path('', OrderAPIView.as_view(), name='order-list-create'),  # GET (alle Bestellungen), POST (neue Bestellung)
    path('<int:pk>/', OrderAPIView.as_view(), name='order-detail'),  # GET, PATCH, DELETE für spezifische Bestellung
    path('order-count/<int:pk>/', OrderCountAPIView.as_view(), name='order-count'),  # Anzahl der laufenden Bestellungen
    path('completed-order-count/<int:pk>/', CompletedOrderCountAPIView.as_view(), name='completed-order-count'),  # Anzahl der abgeschlossenen Bestellungen
]