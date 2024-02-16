from PIL import Image
import numpy as np
# import tensorflow as tf
from django.http import HttpResponseBadRequest
from . import tf_models as models


class UploadProcessing:
    image = None


class Classification:
    def __init__(self, model, image):
        self.model = model
        self.image = image

    def process_image(image_file):
        """
        Обрабатывает загруженное изображение.

        Parameters:
        - image_file (InMemoryUploadedFile): Файл изображения, полученный из запроса.

        Returns:
        - image_array (numpy.ndarray): Массив, представляющий изображение.

        Raises:
        - HttpResponseBadRequest: Если загруженный файл имеет неверное расширение.
        """
        # Проверяем расширение файла
        if not image_file.name.lower().endswith(('.jpg', '.jpeg')):
            raise HttpResponseBadRequest(
                "Неверное расширение изображения. Пожалуйста, загрузите файлы с расширением .jpg или .jpeg.")

        # Читаем изображение в память
        image = Image.open(image_file)

        # Изменяем размер изображения до 32x32
        image = image.resize((32, 32))

        # Переводим изображение в формат numpy массива
        image_array = np.array(image) / 255.0  # Нормализация значений пикселей

        return image_array


    def get_prediction(self):
        """
        Получает предсказание модели на основе переданного изображения в виде массива и пути к файлу модели.

        Parameters:
        - image_array (numpy.ndarray): Массив, представляющий изображение.
        - model_path (str): Путь к файлу модели TensorFlow в формате .h5.

        Returns:
        - prediction (numpy.ndarray): Предсказанные классы изображения моделью.

        Raises:
        - None
        """
        # Загружаем модель TensorFlow из файла .h5
        # model = tf.keras.models.load_model(model_path)

        # Выполняем предсказание
        # prediction = model.predict(np.expand_dims(image_array, axis=0))

        # Удаляем изображение из памяти

        prediction = {
            'first': self.image.name,
            'second': 'some_class: 84%',
            'third': 'some_class: 74%',
        }  # TODO

        return prediction
