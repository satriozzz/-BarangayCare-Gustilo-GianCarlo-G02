from django.urls import path
from . import views

urlpatterns = [
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('health-worker/', views.health_worker_dashboard, name='health_worker_dashboard'),
]