import os
import logging
import tensorflow as tf

# set-up the logger
logger = logging.getLogger('kabuto.neural_networks')


class NeuralNetwork:
    def __init__(self, name):
        """
        constructor of class NeuralNetwork
        """
        self.name = name
        self.model = None
        self.models_dir = "saved_nn"
        self.model_extension = ".h5"
        self.number_of_phases = None
        self.number_of_descriptors = None

    def train(self, first_array, second_array):
        """
        trains the current nn from input arrays
        """
        logger.debug("First_array:", first_array)
        logger.debug("Second_array:", second_array)
        # TODO: to what should the number of epochs be equal?
        self.model.fit(first_array, second_array, epochs=500, verbose=True)
        logger.info("Finished training!")

    def predict(self, input_array):
        """
        predicts the vector_q for each atom in input_array
            input_array is a matrix [num_of_atoms, num_of_descriptors]
            returns a matrix [num_of_atoms, num_of_phases]
        """
        return self.model.predict(input_array)

    def save_model(self):
        path_to_model = os.path.join(self.models_dir, self.name + self.model_extension)
        if self.model is not None:
            self.model.save(path_to_model)
            logger.info("Model \'{}\' saved to file: {}".format(self.name, path_to_model))
        else:
            logger.error("Model \'{}\' was not saved.".format(self.name))

    def load_model(self):
        """
        loads model from 'self.models_dir' to self.model and compiles it
        """
        path_to_model = os.path.join(self.models_dir, self.name + self.model_extension)
        self.model = tf.keras.models.load_model(path_to_model, compile=True)
        logger.info("NN \'{}\' is loaded.".format(self.name))

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
        logger.info("Model \'{}\' created.".format(self.name))

    def create_layers(self):
        """
        returns an array of keras layers
        """
        output_size = self.number_of_phases
        input_size = self.number_of_descriptors
        nodes_in_hidden = 25

        layers = [tf.keras.layers.Dense(units=nodes_in_hidden, input_shape=[input_size]),
                  tf.keras.layers.Dense(units=nodes_in_hidden),
                  tf.keras.layers.Dense(units=nodes_in_hidden),
                  tf.keras.layers.Dense(units=output_size)]
        return layers
