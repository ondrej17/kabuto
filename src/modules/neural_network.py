import os

import tensorflow as tf


class NeuralNetwork:
    def __init__(self, name):
        """
        constructor of class NeuralNetwork
        """
        self.name = name
        self.model = None
        self.models_dir = os.path.join("..", "saved_nn")
        self.model_extension = ".h5"
        self.number_of_phases = None
        self.number_of_descriptors = None

    def train(self, first_array, second_array):
        """
        makes the current nn train data from input arrays
        """
        # TODO: to what should the number of epochs be equal?
        self.model.fit(first_array, second_array, epochs=500, verbose=True)
        print("INFO: Finished training!")

    def save_model(self):
        path_to_model = os.path.join(self.models_dir, self.name + self.model_extension)
        if self.model is not None:
            self.model.save(path_to_model)
            print("INFO: Model \'{}\' saved to file: {}".format(self.name, path_to_model))
        else:
            print("ERROR: Model \'{}\' was not saved.".format(self.name))

    def load_model(self):
        """
        loads model from 'self.models_dir' to self.model and compiles it
        """
        path_to_model = os.path.join(self.models_dir, self.name + self.model_extension)
        self.model = tf.keras.models.load_model(path_to_model, compile=True)
        print("INFO: \'{}\' is loaded.".format(self.name))

    def create_model(self, number_of_descriptors, number_of_phases):
        """
        creates a new model with 'self.name'
        """
        self.number_of_descriptors = number_of_descriptors
        self.number_of_phases = number_of_phases

        # define the layers
        layers = self.create_layers()

        # create the model
        self.model = tf.keras.Sequential(layers)

        # compile the model
        self.model.compile(loss='mean_squared_error',
                           optimizer=tf.keras.optimizers.Adam(0.1))
        print("INFO: Model \'{}\' created.".format(self.name))

    def create_layers(self):
        """
        returns an array of keras layers

        model.add(Dense(12, input_dim=8, init='uniform', activation='relu'))
        It means 8 input parameters, with 12 neurons in the FIRST hidden layer.
        """
        output_size = self.number_of_phases
        input_size = self.number_of_descriptors

        nodes_in_hidden = 25

        layers = [tf.keras.layers.Dense(units=nodes_in_hidden, input_dim=input_size),
                  tf.keras.layers.Dense(units=nodes_in_hidden),
                  tf.keras.layers.Dense(units=nodes_in_hidden),
                  tf.keras.layers.Dense(units=output_size)]
        return layers
