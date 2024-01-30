# api_app/urls.py

from django.urls import path
from .views import ClientListAPIView, export_clients_to_excel, client_list

urlpatterns = [
    path('clients/', ClientListAPIView.as_view(), name='client-list-api'),
    path('export/', export_clients_to_excel, name='client-export'),
    path('clients/html/', client_list, name='client-list-html'),  # Tambahkan URL ini
]
