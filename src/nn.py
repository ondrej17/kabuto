# DEMO FILE
# converter from celsius to fahrenfeit

import tensorflow_hub as hub
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import time

# set up an input data
celsius_q = np.array([-40, -10, 0, 8, 15, 22, 38], dtype=float)
fahrenheit_a = np.array([-40, 14, 32, 46, 59, 72, 100], dtype=float)

# print an input data
for ii in range(len(celsius_q)):
    print(celsius_q[ii], '\t', fahrenheit_a[ii])

# define the layers
layer_0 = tf.keras.layers.Dense(units=4, input_shape=[1])   # input layer
layer_1 = tf.keras.layers.Dense(units=4)                    # hidden layer
layer_2 = tf.keras.layers.Dense(units=1)                    # output layer

# load the Keras .h5 model - uncomment this to load model to the 'reloaded' variable from folder 'models_saved'
# export_path_keras = './models_saved/1574538278.h5'
# reloaded = tf.keras.models.load_model(
#     export_path_keras,
#     # `custom_objects` tells keras how to load a `hub.KerasLayer`
#     custom_objects={'KerasLayer': hub.KerasLayer})
# reloaded.summary()

# create the model
model = tf.keras.Sequential([layer_0, layer_1, layer_2])

# compile the model
model.compile(loss='mean_squared_error',
              optimizer=tf.keras.optimizers.Adam(0.1))

# train the model
history = model.fit(celsius_q, fahrenheit_a, epochs=500, verbose=True)
print("Finished training the model !")

# display training statistics
plt.xlabel('Epoch Number')
plt.ylabel('Loss Magnitude')
plt.plot(history.history['loss'])
#plt.show()

# use the model to predict
temperature_c = 100.0
predictions_f = model.predict([temperature_c])
print("{} degrees Celsius = {} degrees Fahrenheit".format(temperature_c, predictions_f))

# print weights for each layer
print("These are the layer_0 variables: {}\n".format(layer_0.get_weights()))
print("These are the layer_1 variables: {}\n".format(layer_1.get_weights()))
print("These are the layer_2 variables: {}\n".format(layer_2.get_weights()))

# save the model as Keras .h5 model
t = time.time()
export_path_keras = "./models_saved/{}.h5".format(int(t))
# uncomment this to save the model
#model.save(export_path_keras)
#print("Model saved to file:", export_path_keras)
