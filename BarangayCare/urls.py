
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('patients/', include('patients.urls')),
]

handler404 = 'BarangayCare.views.custom_404'
handler500 = 'BarangayCare.views.custom_500'
