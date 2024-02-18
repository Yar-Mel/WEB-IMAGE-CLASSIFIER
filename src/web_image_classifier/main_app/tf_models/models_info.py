import keras


CIFAR_10_LIST = [
    "airplane",
    "automobile",
    "bird",
    "cat",
    "deer",
    "dog",
    "frog",
    "horse",
    "ship",
    "truck",
]

cifar_10_model = keras.models.load_model('src/web_image_classifier/main_app/tf_models/cifar_10.h5')
