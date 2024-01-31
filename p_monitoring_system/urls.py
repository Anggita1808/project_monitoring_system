from django.urls import path
from .views import ProjectListAPIView, export_project_to_excel, project_list

urlpatterns = [
    path('project/', ProjectListAPIView.as_view(), name='project-list-api'),
    path('export/', export_project_to_excel, name='project-export'),
    path('project/html/', project_list, name='project-list-html'),  # Tambahkan URL ini
]