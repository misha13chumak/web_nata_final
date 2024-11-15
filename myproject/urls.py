from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Навигация будет доступна по корневому URL
    path("", include("navigation.urls")),

    # Остальные приложения
    path("detection/", include("detection_app.urls")),
    path("lung-detection/", include("lung_detection.urls")),
    path("sputum-detection/", include("sputum_detection.urls")),
]
