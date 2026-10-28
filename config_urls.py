from django.contrib import admin
from django.urls import path
from inspections import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('jobs/<int:pk>/', views.job_detail, name='job_detail'),
    path('worklist/', views.worklist_view, name='worklist'),
    path('import/', views.import_cases, name='import_cases'),
]

from inspections import calendar_views
