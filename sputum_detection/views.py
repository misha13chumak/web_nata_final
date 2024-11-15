from django.shortcuts import render
from keras.src.utils import load_img, img_to_array

from .forms import ImageUploadForm  # Создайте форму, если её ещё нет
import tensorflow as tf
import numpy as np
from django.core.files.storage import default_storage
import os

# Загрузка модели
model = tf.keras.models.load_model(
    r'C:\Users\misha\Desktop/Учеба 4 курс/7 семестр/Диплом Наташа/sputum_classification_model.h5'  # Укажите путь к вашей модели
)

# Классы
class_labels = ['Акрацинома', 'Мелкоклеточный', 'Норма', 'Плоскоклеточный']

def index(request):
    result = None
    uploaded_image_url = None

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Получаем загруженное изображение
            image = form.cleaned_data['image']

            # Сохраняем изображение
            image_path = default_storage.save(f"uploaded/{image.name}", image)
            uploaded_image_url = default_storage.url(image_path)

            # Предобрабатываем изображение
            with load_img(default_storage.path(image_path), target_size=(224, 224)) as img:
                img_array = img_to_array(img) / 255.0
                img_array = np.expand_dims(img_array, axis=0)

                # Выполняем предсказание
                predictions = model.predict(img_array)
                predicted_class = class_labels[np.argmax(predictions)]
                result = f'Класс изображения: {predicted_class}'

    else:
        form = ImageUploadForm()

    return render(request, 'sputum_detection/index.html', {
        'form': form,
        'result': result,
        'uploaded_image_url': uploaded_image_url,
    })
