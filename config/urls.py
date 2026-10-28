from django.contrib import admin
from django.urls import path
from inspections import views

urlpatterns = [
    path('worklist/', views.worklist_view, name='worklist'),
    path('admin/', admin.site.urls),
    path('jobs/<int:pk>/quick-action/', views.quick_action, name='quick_action'),
    path('', views.dashboard, name='dashboard'),
    path('jobs/<int:pk>/', views.job_detail, name='job_detail'),
    path('import/', views.import_cases, name='import_cases'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('jobs/<int:pk>/edit/', views.job_edit, name='job_edit'),
]

