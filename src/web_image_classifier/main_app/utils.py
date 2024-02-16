from PIL import Image
import numpy as np
import tensorflow as tf
from django.http import HttpResponseBadRequest
from . import tf_models as models
import cv2



class UploadProcessing:
    def __init__(self, image_file, allowed_extensions, max_size):
        self.image_file = image_file
        self.allowed_extensions = allowed_extensions
        self.max_size = max_size


    def validate_image(image_file, allowed_extensions=('.jpg', '.jpeg'), max_size=50 ):
        """
        Проверяет расширение и размер изображения.

        Parameters:
        - image_file (InMemoryUploadedFile): Файл изображения, полученный из запроса.
        - allowed_extensions (tuple): Кортеж разрешенных расширений изображения.
        - max_size (int): Максимальный размер изображения.

        Returns:
        - image_file (InMemoryUploadedFile): Файл изображения, если он валиден.

        Raises:
        - HttpResponseBadRequest: Если расширение изображения неверное или размер изображения слишком большой.
        """
        # Проверяем расширение файла
        if not image_file.name.lower().endswith(allowed_extensions):
            raise HttpResponseBadRequest(
                f"Неверное расширение изображения. Пожалуйста, загрузите файлы с расширением {', '.join(allowed_extensions)}.")

        
        # Проверяем размер файла
        max_size = max_size * 1024 * 1024
        if image_file.size > max_size:
            raise HttpResponseBadRequest(
                f"Слишком большой размер изображения. Максимальный размер - {max_size / (1024 * 1024)} MB.")

        # Если изображение прошло валидацию, возвращаем его
        return image_file


class Classification:
    def __init__(self, model, image_file):
        self.model = model
        self.image_file = image_file

    def process_image_raster(self, image_file, target_size=(32, 32)):
        """
        Обрабатывает загруженное изображение.

        Parameters:
        - image_file (InMemoryUploadedFile): Файл изображения, полученный из запроса
        - target_size (tuple): Целевой размер изображения после преобразования. По умолчанию (32, 32).

        Returns:
        - image_array (numpy.ndarray): Массив, представляющий изображение.
        """

        # Читаем изображение в память
        image = Image.open(image_file)

        # Изменяем размер изображения до целевого размера
        image = image.resize(target_size)

        # Переводим изображение в формат numpy массива
        image_array = np.array(image) / 255.0  # Нормализация значений пикселей

        return image_array
    

    def process_image_for_tensorflow(self, vector_image, target_size=(32, 32)):
        """
        Преобразует векторное изображение в формат, подходящий для модели TensorFlow.

        Parameters:
        - vector_image (InMemoryUploadedFile): Файл изображения, полученный из запроса
        - target_size (tuple): Целевой размер изображения после преобразования. По умолчанию (32, 32).

        Returns:
        - processed_image (numpy.ndarray): Изображение в формате, подходящем для модели TensorFlow.
        """

        # Загрузка векторного изображения (SVG, например)
        # и преобразование его в растровое изображение (PNG, например)
        vector_image = cv2.imread(vector_image)

        # Изменение размера изображения до целевого размера
        resized_image = cv2.resize(vector_image, target_size)

        # Нормализация значений пикселей
        normalized_image = resized_image / 255.0

        # Добавление размерности для соответствия ожидаемому формату входных данных модели TensorFlow
        processed_image = np.expand_dims(normalized_image, axis=0)

        return processed_image


    def get_prediction(self, image_array, model):
        """
        Получает предсказание модели на основе переданного изображения в виде массива и пути к файлу модели.

        Parameters:
        - image_array (numpy.ndarray): Массив, представляющий изображение.
        - model (str): Путь к файлу модели TensorFlow в формате .h5.

        Returns:
        - prediction (dict): Словарь с предсказанными классами изображения моделью.

        Raises:
        - None
        """
        # Загружаем модель TensorFlow из файла .h5
        model = tf.keras.models.load_model(model)

        # Выполняем предсказание
        prediction = model.predict(np.expand_dims(image_array, axis=0))

        # Получаем три наиболее вероятных класса
        top_classes = tf.argsort(prediction, axis=1, direction='DESCENDING')[:,:3]

        # Получаем имена классов и вероятности
        classes = ['class1', 'class2', 'class3']  # Поменяйте на реальные имена классов
        probabilities = prediction[0][top_classes[0]].numpy()

        # Сохраняем предсказание в формате, как указано в вашем запросе
        prediction_dict = {
            'first': classes[top_classes[0][0]] + ': ' + str(round(probabilities[0] * 100, 2)) + '%',
            'second': classes[top_classes[0][1]] + ': ' + str(round(probabilities[1] * 100, 2)) + '%',
            'third': classes[top_classes[0][2]] + ': ' + str(round(probabilities[2] * 100, 2)) + '%',
        }

        # Удаляем изображение из памяти
        del image_array

        return prediction_dict
