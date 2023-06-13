from keras.layers import Input
from keras.applications.mobilenet_v2 import MobileNetV2
from keras.layers.core import Dense
from keras.models import Model
from tensorflow import image

input_shape=(224, 224, 3)
img_input = Input(shape=input_shape)

base_model = MobileNetV2(include_top=False, input_tensor=img_input, input_shape=input_shape, 
                         pooling="avg", weights='imagenet')
x = base_model.output
predictions = Dense(14, activation="sigmoid", name="predictions")(x)
model = Model(inputs=img_input, outputs=predictions)
model.load_weights('best_weights.h5')