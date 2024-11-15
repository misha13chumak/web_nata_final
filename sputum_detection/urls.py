from django.urls import path
from . import views
app_name = 'sputum_detection'  # Добавьте эту строку

urlpatterns = [
    path('', views.index, name='sputum_detection'),
]