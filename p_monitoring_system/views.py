from rest_framework import generics
from .models import Project
from .serializers import ProjectSerializer
# from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from django.db.models import Q
import pandas as pd
from django.http import HttpResponse
from openpyxl import Workbook
from django.utils import timezone
import datetime

class ProjectListAPIView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['name', 'address', 'industry', 'status']
    
def project_list(request):
    project = Project.objects.all()
    
    search_query = request.GET.get('search')
    if search_query:
        project = project.filter(
            Q(name__icontains=search_query)
        )

    order_by_param = request.GET.get('order_by', 'name')
    valid_order_columns = ['name']
    if order_by_param not in valid_order_columns:
        order_by_param = 'name'

    project = project.order_by(order_by_param)    

    print(order_by_param)
    
    return render(request, 'project_list.html', {'project': project, 'order_by_param': order_by_param})

def export_project_to_excel(reqluest):
    project = Project.objects.all()

    # Membuat file Excel menggunakan openpyxl
    workbook = Workbook()
    sheet = workbook.active

    # Menulis header
    header = ['Year', 'PID', 'Name', 'Description', 'Status', 'Customer', 'End User',
              'Sales', 'PM', 'AM', 'PIC', 'Contract No', 'Contract Date', 'Amount (Tax)',
              'Amount (Exc Tax)', 'Start Date', 'End Date', 'TOP', 'SOW', 'OOS', 'Detail',
              'Remarks', 'Weight', 'Priority', 'Type', 'Market Segment', 'Tech Use',
              'Resiko', 'Completion Percentage']
    
    sheet.append(header)

    # Menulis data
    for project in project:
        data_row = []

        sheet.append(data_row)

    # Mengatur response untuk file Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=project_data.xlsx'
    workbook.save(response)

    return response