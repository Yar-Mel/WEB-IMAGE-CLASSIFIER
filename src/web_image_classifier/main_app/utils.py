import numpy as np
import tensorflow as tf
from django.http import HttpResponseBadRequest
from typing import Tuple
from itertools import chain
from django.core.files.uploadedfile import InMemoryUploadedFile
from copy import deepcopy
from PIL import Image
from io import BytesIO
import cairosvg
import cv2
from .tf_models.models_info import CIFAR_10_LIST
import cairosvg
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO


ALLOWED_EXTENSION = {"rastr": ("jpg", "jpeg", "png"), "vector": ("svg",)}


class UploadProcessing:
    def __init__(
        self,
        allowed_extensions=tuple(chain.from_iterable(ALLOWED_EXTENSION.values())),
        max_size=50,
    ):
        """
        Initializes the UploadProcessing object.

        Parameters:
        - allowed_extensions (tuple): Tuple of allowed image file extensions. Default is ('.jpg', '.jpeg', '.SVG', '.png').
        - max_size (int): Maximum allowed size of the image file in megabytes. Default is 50 MB.
        """
        self._image = None
        self.allowed_extensions = allowed_extensions
        self.max_size = max_size

    @property
    def image(self):
        """
        Returns the image file.
        """
        return self._image

    @image.setter
    def image(self, value):
        """
        Sets the image file and performs validation.

        Parameters:
        - value (InMemoryUploadedFile): Image file obtained from the request.
        """
        self._validate_image(value)
        value = self._svg_to_png(value)
        self._image = deepcopy(Image.open(value))

    def _svg_to_png(self, image):
<<<<<<< Updated upstream
        if not isinstance(image, InMemoryUploadedFile) or not image.name.lower().endswith('.svg'):
=======
        if not isinstance(
            image, InMemoryUploadedFile
        ) or not image.name.lower().endswith(".svg"):
>>>>>>> Stashed changes
            return image  # If the file is not SVG or not InMemoryUploadedFile, return it as is
        else:
            svg_content = image.read()  # Read the content of the SVG file
            image.seek(0)  # Return the cursor to the beginning of the file
            png_content = cairosvg.svg2png(bytestring=svg_content)  # Convert SVG to PNG
<<<<<<< Updated upstream
    
=======

>>>>>>> Stashed changes
            # Create a BytesIO object to save the PNG image in memory
            png_buffer = BytesIO()
            png_buffer.write(png_content)
            png_buffer.seek(0)
<<<<<<< Updated upstream
    
            # Create an InMemoryUploadedFile object for the PNG image
            png_file = InMemoryUploadedFile(png_buffer, None, image.name.replace('.svg', '.png'), 'image/png', png_buffer.tell(), None)
    
            return png_file  # Return the PNG image


=======

            # Create an InMemoryUploadedFile object for the PNG image
            png_file = InMemoryUploadedFile(
                png_buffer,
                None,
                image.name.replace(".svg", ".png"),
                "image/png",
                png_buffer.tell(),
                None,
            )

            return png_file  # Return the PNG image

>>>>>>> Stashed changes
    def _validate_image(self, image):
        """
        Checks the extension and size of the image.

        Parameters:
        - image (InMemoryUploadedFile): Image file obtained from the request.
        """
        # Check the file extension
        if not image.name.lower().endswith(self.allowed_extensions):
            raise HttpResponseBadRequest(
                f"Invalid image extension. Please upload files with extensions {', '.join(self.allowed_extensions)}."
            )

        # Check the file size
        max_size_bytes = self.max_size * 1024 * 1024
        if image.size > max_size_bytes:
            raise HttpResponseBadRequest(
                f"Image size is too large. Maximum size is {self.max_size} MB."
            )


class ImageClassification:
    """
    Class for image classification using TensorFlow model.

    Attributes:
    - model (str): Path to the TensorFlow model file in .h5 format.
    - image_file (InMemoryUploadedFile): Image file obtained from the request.

    Methods:
    - __call__(*args, **kwargs): Method to call the class as a function.
    - process_image_raster(image_file: str, target_size: Tuple[int, int] = (32, 32)) -> np.ndarray:
        Processes raster image.
    - process_image_vector(vector_image: str, target_size: Tuple[int, int] = (32, 32)) -> np.ndarray:
        Converts vector image.
    - get_prediction(image_array: np.ndarray, model: str) -> dict:
        Gets model prediction based on the image.
    """

    def __init__(self, model, image_file):
        """
        Initializes the class.

        Parameters:
        - model (str): Path to the TensorFlow model file in .h5 format.
        - image_file (InMemoryUploadedFile): Image file obtained from the request.
        """
        self.model = model
        self.image_file = image_file

    def process_image_raster(
        self, image_file: Image, target_size: Tuple[int, int] = (32, 32)
    ) -> np.ndarray:
        """
        Processes the uploaded raster image.

        Parameters:
        - image_file (InMemoryUploadedFile): Image file obtained from the request.
        - target_size (tuple): Target size of the image after transformation. Default is (32, 32).

        Returns:
        - image_array (numpy.ndarray): Array representing the image.
        """

        # Check the file extension
        if image_file.format.lower() == "png":
            # If the file has a png extension, convert it to RGB mode
            image = image_file.convert("RGB")
        else:
            # Otherwise, simply open the image
            image = image_file.convert("RGB")

        image = image.resize(target_size)
        image_array = np.array(image) / 255.0
        return image_array

    def process_image_vector(
        self, vector_image: Image, target_size: Tuple[int, int] = (32, 32)
    ) -> np.ndarray:
        """
        Converts vector image to a format suitable for TensorFlow model.

        Parameters:
        - image_file (InMemoryUploadedFile): Image file obtained from the request.
        - target_size (tuple): Target size of the image after transformation. Default is (32, 32).

        Returns:
        - processed_image (numpy.ndarray): Image in a format suitable for TensorFlow model.
        """
        vector_image = cv2.imread(vector_image)
        resized_image = cv2.resize(vector_image, target_size)
        normalized_image = resized_image / 255.0
        processed_image = np.expand_dims(normalized_image, axis=0)
        return processed_image

    def get_prediction(self, image_array: np.ndarray, model: str) -> dict:
        """
        Gets model prediction based on the provided image and model file path.

        Parameters:
        - image_array (numpy.ndarray): Array representing the image.
        - model (str): TensorFlow model file in .h5 format.

        Returns:
        - prediction (dict): Dictionary with predicted image classes by the model.
        """
        prediction = model.predict(np.expand_dims(image_array, axis=0))
        top_classes = tf.argsort(prediction, axis=1, direction="DESCENDING")[:, :3]
        probabilities = prediction[0][top_classes[0]]
        prediction_dict = {
            "first": (
                CIFAR_10_LIST[top_classes[0][0]]
                + ": "
                + str(round(probabilities[0] * 100, 2))
                + "%"
            ).capitalize(),
            "second": (
                CIFAR_10_LIST[top_classes[0][1]]
                + ": "
                + str(round(probabilities[1] * 100, 2))
                + "%"
            ).capitalize(),
            "third": (
                CIFAR_10_LIST[top_classes[0][2]]
                + ": "
                + str(round(probabilities[2] * 100, 2))
                + "%"
            ).capitalize(),
        }

        return prediction_dict

    def get_results(self):
        predictions = None
        print("Start classification")
        print(f"Current model: {self.model.name}")
        if self.image_file.format.lower() in ALLOWED_EXTENSION["rastr"]:
            image_array = self.process_image_raster(self.image_file)
            predictions = self.get_prediction(image_array, self.model)
        elif self.image_file.format.lower() in ALLOWED_EXTENSION["vector"]:
            image_array = self.process_image_vector(self.image_file)
            predictions = self.get_prediction(image_array, self.model)
        print(f"results: {predictions}")
        return predictions
