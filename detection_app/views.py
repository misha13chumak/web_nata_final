from django.shortcuts import render

from .forms import ImageUploadForm
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
from PIL import Image, ImageDraw
import os
from django.conf import settings
from django.core.files.storage import default_storage

# Загрузка модели
model = tf.keras.models.load_model(
    r'C:\Users\misha\Desktop\Учеба 4 курс\7 семестр\Диплом Наташа\biopsia_neiro_model.keras')


def index(request):
    result = None
    uploaded_image_url = None
    analysis_description = ""
    highlighted_areas = []

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']

            # Сохранение изображения
            image_path = default_storage.save(f"uploaded/{image.name}", image)
            uploaded_image_url = default_storage.url(image_path)

            # Загрузка и подготовка изображения
            with Image.open(default_storage.path(image_path)) as img:
                img_resized = img.resize((224, 224))
                img_array = img_to_array(img_resized) / 255.0
                img_array = np.expand_dims(img_array, axis=0)

                # Предсказание
                predictions = model.predict(img_array)
                classes = ['Lung_Adenocarcinoma (Аденокарцинома легкого)',
                           'Lung_Benign_Tissue (Доброкачественная ткань легкого)',
                           'Lung_Squamous_Cell_Carcinoma (Плоскоклеточный рак легкого)']

                predicted_class = classes[np.argmax(predictions)]
                result = f'Предсказанный класс: {predicted_class}'

                # Генерация отчёта анализа
                analysis_description = "Нейросеть определила, что изображение относится к классу '{}', на основе анализа структуры клеток и аномалий.".format(
                    predicted_class)

                # Выделение участков
                highlighted_areas = generate_highlighted_areas(img)

    else:
        form = ImageUploadForm()

    return render(request, 'detection_app/index.html', {
        'form': form,
        'result': result,
        'uploaded_image_url': uploaded_image_url,
        'analysis_description': analysis_description,
        'highlighted_areas': highlighted_areas
    })


def generate_highlighted_areas(img):
    # Генерирует области интереса с выделением
    area_images = []
    for i in range(4):  # Пример: 4 области интереса
        area = img.copy()
        draw = ImageDraw.Draw(area)
        draw.rectangle([i * 50, i * 50, i * 50 + 60, i * 50 + 60], outline="red", width=3)

        # Сохранение выделенных участков
        area_path = os.path.join(settings.MEDIA_ROOT, f"highlighted/area_{i}.png")
        os.makedirs(os.path.dirname(area_path), exist_ok=True)  # Создаем папку, если ее нет
        area.save(area_path)
        area_images.append(default_storage.url(f"highlighted/area_{i}.png"))

        area.close()  # Закрываем копию изображения для экономии памяти

    return area_images
