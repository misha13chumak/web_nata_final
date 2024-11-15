from django.urls import path
from . import views
app_name = 'detection_app'

urlpatterns = [
    path('', views.index, name='detection_app'),
]