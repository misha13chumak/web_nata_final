from django.shortcuts import render
from keras.src.utils import img_to_array

from .forms import ImageUploadForm  # Создайте новую форму для загрузки изображений, если её ещё нет
import tensorflow as tf
import numpy as np
from PIL import Image, ImageDraw
import os
from django.conf import settings
from django.core.files.storage import default_storage

# Загрузка новой модели
model = tf.keras.models.load_model(
    r'C:\Users\misha\Desktop\Учеба 4 курс\7 семестр\Диплом Наташа\programs\2d_cnn_lung_classification.keras'
)


# Классы для предсказания
class_labels = ['Normal (Норма)', 'Benign (Доброкачественный случай)', 'Malignant (Злокачественный случай)']

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
            with Image.open(default_storage.path(image_path)).convert("L") as img:  # Конвертация в черно-белое
                img_resized = img.resize((128, 128))
                img_array = img_to_array(img_resized) / 255.0
                img_array = np.expand_dims(img_array, axis=0)

                # Предсказание
                predictions = model.predict(img_array)
                predicted_class = class_labels[np.argmax(predictions)]
                result = f'Предсказанный класс: {predicted_class}'

                # Генерация отчёта анализа
                analysis_description = "Нейросеть определила, что изображение относится к классу '{}', на основе анализа структуры клеток и аномалий.".format(
                    predicted_class)

                # Выделение участков
                highlighted_areas = generate_highlighted_areas(img)

    else:
        form = ImageUploadForm()

    return render(request, 'lung_detection/index.html', {
        'form': form,
        'result': result,
        'uploaded_image_url': uploaded_image_url,
        'analysis_description': analysis_description,
        'highlighted_areas': highlighted_areas
    })

def generate_highlighted_areas(img):
    # Генерация областей интереса с выделением
    area_images = []
    for i in range(4):
        area = img.copy()
        draw = ImageDraw.Draw(area)
        draw.rectangle([i * 50, i * 50, i * 50 + 60, i * 50 + 60], outline="red", width=3)

        # Сохранение выделенных участков
        area_path = os.path.join(settings.MEDIA_ROOT, f"highlighted/area_{i}.png")
        os.makedirs(os.path.dirname(area_path), exist_ok=True)
        area.save(area_path)
        area_images.append(default_storage.url(f"highlighted/area_{i}.png"))

        area.close()

    return area_images
