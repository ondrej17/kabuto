# The Basics: Training My First Model
# f = c*1.8 + 32

# import dependencies
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# set up training data
celsius_q = np.array([-40, -10, 0, 8, 15, 22, 38], dtype=float)
fahrenheit_a = np.array([-40, 14, 32, 46, 59, 72, 100], dtype=float)

# print training data
for ii in range(len(celsius_q)):
    print(celsius_q[ii], '\t', fahrenheit_a[ii])

# ML terminology:
#   feature - inputs to our model, e.g. the degrees in celsius
#   labels - the output our model predicts, e.g. the degrees in fahrenheit

# create the model
# step 1:   Build the layers
#           units=1 means that there will be one neuron in layer
#           input_shape=[1] means that input is a single value
l0 = tf.keras.layers.Dense(units=4, input_shape=[1])
l1 = tf.keras.layers.Dense(units=4)
l2 = tf.keras.layers.Dense(units=1)

# step2:    Assemble layers into the model
#           [l0] means we have only one layer
model = tf.keras.Sequential([l0, l1, l2])

# compile the model, with loss and optimizer functions
model.compile(loss='mean_squared_error',
              optimizer=tf.keras.optimizers.Adam(0.1))

# train the model
history = model.fit(celsius_q, fahrenheit_a, epochs=500, verbose=False)
print("Finished training the model")

# display training statistics
#   the 'fit' funcion returns history object
plt.xlabel('Epoch Number')
plt.ylabel('Loss Magnitude')
plt.plot(history.history['loss'])
plt.show()

# use the model to predict values
print("Model predicts that 100 degrees Celsius is: {} degrees Fahrenheit".format(model.predict([100.0])))

# print wights for each layer
print("These are the l0 variables: {}".format(l0.get_weights()))
print("These are the l1 variables: {}".format(l1.get_weights()))
print("These are the l2 variables: {}".format(l2.get_weights()))

# end !
