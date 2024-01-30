# api_app/views.py

from rest_framework import generics
from .models import Client
from .serializers import ClientSerializer
# from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from django.db.models import Q
import pandas as pd
from django.http import HttpResponse
from openpyxl import Workbook
from django.utils import timezone
import datetime

class ClientListAPIView(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['name', 'address', 'industry', 'status']
    
def client_list(request):
    clients = Client.objects.all()
    
    search_query = request.GET.get('search')
    if search_query:
        clients = clients.filter(
            Q(name__icontains=search_query)
        )

    order_by_param = request.GET.get('order_by', 'name')
    valid_order_columns = ['name']
    if order_by_param not in valid_order_columns:
        order_by_param = 'name'

    clients = clients.order_by(order_by_param)    

    print(order_by_param)
    
    return render(request, 'client_list.html', {'clients': clients, 'order_by_param': order_by_param})

def export_clients_to_excel(request):
    clients = Client.objects.all()

    # Membuat file Excel menggunakan openpyxl
    workbook = Workbook()
    sheet = workbook.active

    # Menulis header
    header = ['name', 'address', 'pic_phone', 'pic_email', 'pic_title', 'industry', 'website_url',
              'logo', 'company_size', 'company_address', 'contact_person_name', 'company_email',
              'company_phone', 'additional_info', 'date_joined', 'status', 'last_activity']

    sheet.append(header)

    # Menulis data
    for client in clients:
        data_row = []
        for field in header:
            value = getattr(client, field)
            if field in ['date_joined', 'last_activity'] and value:
                # Convert datetime.date to naive datetime
                value = datetime.datetime.combine(value, datetime.datetime.min.time())
                value = timezone.make_aware(value, timezone.utc).replace(tzinfo=None)
            data_row.append(value)

        sheet.append(data_row)

    # Mengatur response untuk file Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=client_data.xlsx'
    workbook.save(response)

    return response