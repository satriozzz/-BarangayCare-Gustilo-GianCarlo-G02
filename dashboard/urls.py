
from django.urls import path
from . import views

urlpatterns = [
    path('owner/', views.owner_dashboard, name='owner_dashboard'),
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
    path('mechanic/', views.mechanic_dashboard, name='mechanic_dashboard'),
]
