"""
@daavoo Implementation of:

Maturana, D. and Scherer, S.;
VoxNet: A 3D Convolutional Neural Network for Real-Time Object Recognition.
"""
from keras.layers.advanced_activations import LeakyReLU
from keras import backend as K
from keras.layers import (
    Input,
    Conv3D,
    MaxPool3D,
    Dropout,
    Dense,
    Flatten
) 
from keras.models import Model          
            
def VoxNet(n_classes, input_shape=(32,32,32), weights=None):
    if  K.image_data_format() == "channels_last":
        input_shape = input_shape + (1,)
    else:
        input_shape = (1,) + input_shape

    data_input = Input(input_shape)
    
    conv1 = Conv3D(32, (5,5,5), strides=(2,2,2), activation=LeakyReLU(0.1), name="conv1")(data_input)
    drop1 = Dropout(0.2, name="drop1")(conv1)
    conv2 = Conv3D(32, (3,3,3), activation=LeakyReLU(0.1), name="conv2")(drop1)
    pool2 = MaxPool3D(name="pool2")(conv2)
    drop2 = Dropout(0.3, name="drop2")(pool2)
    flat = Flatten()(drop2)
    fc1 = Dense(128, activation="relu", name="fc1")(flat)
    drop3 = Dropout(0.4, name="drop3")(fc1)
    fc2 = Dense(n_classes, activation="softmax", name="fc2")(drop3)
    
    model = Model(data_input, fc2)
    
    if weights is not None:
        model.load_weights(weights)
    
    return model
    
