from django.urls import path
from . import views
app_name = 'lung_detection'  # Добавьте эту строку

urlpatterns = [
    path('', views.index, name='lung_detection'),
]
