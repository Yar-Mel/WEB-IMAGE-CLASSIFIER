from PIL import Image
import numpy as np
import tensorflow as tf
from django.http import HttpResponseBadRequest
import cv2
from typing import Tuple
from copy import deepcopy
import keras
from .tf_models.models_info import CIFAR_10_LIST


class UploadProcessing:
    def __init__(self, allowed_extensions=('.jpg', '.jpeg', '.SVG', '.png'), max_size=50):
        """
        Инициализирует объект UploadProcessing.

        Parameters:
        - allowed_extensions (tuple): Кортеж допустимых расширений файлов изображений. По умолчанию ('.jpg', '.jpeg', '.SVG', '.png').
        - max_size (int): Максимальный допустимый размер файла изображения в мегабайтах. По умолчанию 50 MB.
        """
        self._image = None
        self.allowed_extensions = allowed_extensions
        self.max_size = max_size

    @property
    def image(self):
        """
        Возвращает файл изображения.
        """
        return self._image

    @image.setter
    def image(self, value):
        """
        Устанавливает файл изображения и выполняет его валидацию.

        Parameters:
        - value (InMemoryUploadedFile): Файл изображения, полученный из запроса.
        """
        self._validate_image(value)
        self._image = deepcopy(value)

    def _validate_image(self, image):
        """
        Проверяет расширение и размер изображения.

        Parameters:
        - image (InMemoryUploadedFile): Файл изображения, полученный из запроса.
        """
        # Проверяем расширение файла
        if not image.name.lower().endswith(self.allowed_extensions):
            raise HttpResponseBadRequest(
                f"Неверное расширение изображения. Пожалуйста, загрузите файлы с расширением {', '.join(self.allowed_extensions)}.")

        # Проверяем размер файла
        max_size_bytes = self.max_size * 1024 * 1024
        if image.size > max_size_bytes:
            raise HttpResponseBadRequest(
                f"Слишком большой размер изображения. Максимальный размер - {self.max_size} MB.")


class ImageClassification:
    """
    Класс для классификации изображений с использованием модели TensorFlow.

    Attributes:
    - model (str): Путь к файлу модели TensorFlow в формате .h5.
    - image_file (InMemoryUploadedFile): Файл изображения, полученный из запроса.

    Methods:
    - __call__(*args, **kwargs): Метод для вызова класса как функции.
    - process_image_raster(image_file: str, target_size: Tuple[int, int] = (32, 32)) -> np.ndarray:
        Обрабатывает растровое изображение.
    - process_image_vector(vector_image: str, target_size: Tuple[int, int] = (32, 32)) -> np.ndarray:
        Преобразует векторное изображение.
    - get_prediction(image_array: np.ndarray, model: str) -> dict:
        Получает предсказание модели на основе изображения.
    """

    def __init__(self, model: str, image_file):
        """
        Инициализация класса.

        Parameters:
        - model (str): Путь к файлу модели TensorFlow в формате .h5.
        - image_file (InMemoryUploadedFile): Файл изображения, полученный из запроса.
        """
        self.model = model
        self.image_file = image_file

    ALLOWED_EXTENSION = {
        'rastr': ('.jpg', '.jpeg', '.png'),
        'vector': ('.SVG',)
    }

    def process_image_raster(self, image_file: Image, target_size: Tuple[int, int] = (32, 32)) -> np.ndarray:
        """
        Обрабатывает загруженное растровое изображение.

        Parameters:
        - image_file (InMemoryUploadedFile): Файл изображения, полученный из запроса.
        - target_size (tuple): Целевой размер изображения после преобразования. По умолчанию (32, 32).

        Returns:
        - image_array (numpy.ndarray): Массив, представляющий изображение.
        """
        image = Image.open(image_file)
        image = image.resize(target_size)
        image_array = np.array(image) / 255.0
        return image_array

    def process_image_vector(self, vector_image: Image, target_size: Tuple[int, int] = (32, 32)) -> np.ndarray:
        """
        Преобразует векторное изображение в формат, подходящий для модели TensorFlow.

        Parameters:
        - image_file (InMemoryUploadedFile): Файл изображения, полученный из запроса.
        - target_size (tuple): Целевой размер изображения после преобразования. По умолчанию (32, 32).

        Returns:
        - processed_image (numpy.ndarray): Изображение в формате, подходящем для модели TensorFlow.
        """
        vector_image = cv2.imread(vector_image)
        resized_image = cv2.resize(vector_image, target_size)
        normalized_image = resized_image / 255.0
        processed_image = np.expand_dims(normalized_image, axis=0)
        return processed_image

    def get_prediction(self, image_array: np.ndarray, model: str) -> dict:
        """
        Получает предсказание модели на основе переданного изображения и пути к файлу модели.

        Parameters:
        - image_array (numpy.ndarray): Массив, представляющий изображение.
        - model (str): Файл модели TensorFlow в формате .h5.

        Returns:
        - prediction (dict): Словарь с предсказанными классами изображения моделью.
        """
        prediction = model.predict(np.expand_dims(image_array, axis=0))
        top_classes = tf.argsort(prediction, axis=1, direction='DESCENDING')[:, :3]
        probabilities = prediction[0][top_classes[0]]
        prediction_dict = {
            'first': CIFAR_10_LIST[top_classes[0][0]] + ': ' + str(round(probabilities[0] * 100, 2)) + '%',
            'second': CIFAR_10_LIST[top_classes[0][1]] + ': ' + str(round(probabilities[1] * 100, 2)) + '%',
            'third': CIFAR_10_LIST[top_classes[0][2]] + ': ' + str(round(probabilities[2] * 100, 2)) + '%',
        }

        return prediction_dict

    def get_results(self):
        """
        Метод для вызова класса как функции.
        """

        if self.image_file.name.lower().endswith(self.ALLOWED_EXTENSION['rastr']):
            image_array = self.process_image_raster(self.image_file)
            predictions = self.get_prediction(image_array, self.model)
        elif self.image_file.name.lower().endswith(self.ALLOWED_EXTENSION['vector']):
            image_array = self.process_image_vector(self.image_file)
            predictions = self.get_prediction(image_array, self.model)

        return predictions
