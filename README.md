# WEB IMAGE CLASSIFIER
## GO IT Data Science Project
### Team
* [Yaroslav Melnychuk](https://github.com/Yar-Mel)
* [Yehor Serdiuk](https://github.com/De1c)
* [Dmitry Vokin](https://github.com/Noma9d)
* [Michael Gordiychuk](https://github.com/TurMod)

### Tools and Technologies
* Django
* Tensorflow
* Keras
* Poetry
* Docker

### Run and Installation
You can run the docker image with the application by using the following command:
 
    docker run -p 80:80 -td yarmel/wic-image

The start of the local server will be at http://0.0.0.0:80/

### Model Description

This neural network is a convolutional neural network (CNN) for
image classification of the CIFAR-10 dataset.
The main elements include three convolutional layers, batch normalization,
MaxPooling, Dropout for regularization and two connected layers.

### Architectural elements:

    Model: "pycrafters_team_model_v1.3"
    _________________________________________________________________
     Layer (type)                Output Shape              Param #   
    =================================================================
     conv2d (Conv2D)             (None, 30, 30, 32)        896       
                                                                     
     batch_normalization (Batch  (None, 30, 30, 32)        128       
     Normalization)                                                  
                                                                     
     dropout (Dropout)           (None, 30, 30, 32)        0         
                                                                     
     conv2d_1 (Conv2D)           (None, 28, 28, 64)        18496     
                                                                     
     batch_normalization_1 (Bat  (None, 28, 28, 64)        256       
     chNormalization)                                                
                                                                     
     max_pooling2d (MaxPooling2  (None, 14, 14, 64)        0         
     D)                                                              
                                                                     
     conv2d_2 (Conv2D)           (None, 14, 14, 128)       73856     
                                                                     
     batch_normalization_2 (Bat  (None, 14, 14, 128)       512       
     chNormalization)                                                
                                                                     
     max_pooling2d_1 (MaxPoolin  (None, 7, 7, 128)         0         
     g2D)                                                            
                                                                     
     conv2d_3 (Conv2D)           (None, 5, 5, 64)          73792     
                                                                     
     batch_normalization_3 (Bat  (None, 5, 5, 64)          256       
     chNormalization)                                                
                                                                     
     max_pooling2d_2 (MaxPoolin  (None, 1, 1, 64)          0         
     g2D)                                                            
                                                                     
     dropout_1 (Dropout)         (None, 1, 1, 64)          0         
                                                                     
     flatten (Flatten)           (None, 64)                0         
                                                                     
     dense (Dense)               (None, 256)               16640     
                                                                     
     dropout_2 (Dropout)         (None, 256)               0         
                                                                     
     dense_1 (Dense)             (None, 10)                2570      
                                                                     
    =================================================================
    Total params: 187402 (732.04 KB)
    Trainable params: 186826 (729.79 KB)
    Non-trainable params: 576 (2.25 KB)
    _________________________________________________________________

### Tuning:
* Used gate initializer (he_normal) and glorot_uniform for efficient weight initialization.
* The Adam optimizer and the categorical cross-entropy loss function.
* Used early stop and reduced learning rate to manage learning duration and performance.

![loss_acc_plot](/src/model/loss_acc.png)
![confusion_matrix](/src/model/cm.png)