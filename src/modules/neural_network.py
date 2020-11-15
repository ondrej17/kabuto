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
        self.model_extension = ".h5"
        self.number_of_phases = None
        self.number_of_descriptors = None

        # learning parameters that must be set correctly ->
        self.learning_rate = 0.000005
        self.epochs = 100
        self.batch_size = 10000
            # prepare scheduler
        #self.lr_schedule = tf.keras.optimizers.schedules.InverseTimeDecay(
        #    initial_learning_rate   = self.learning_rate,
        #    decay_steps             = 1.0,
        #    decay_rate              = 0.5,
        #    staircase               = False
        #)
        self.lr_schedule = self.learning_rate
        # <-

    def create_layers(self):
        """
        returns an array of keras layers
        """
        output_size = self.number_of_phases
        input_size = self.number_of_descriptors
        nodes = 25

        layers = [
            # input tensor
            tf.keras.Input(shape=(input_size,), dtype='float32'),
            # hidden layers
            tf.keras.layers.Dense(units=nodes, activation='relu'),
            tf.keras.layers.Dense(units=nodes, activation='relu'),
            # output layer
            tf.keras.layers.Dense(units=output_size, activation='softmax')
        ]
        return layers

    def train(self, first_array, second_array):
        """
        trains the current nn from input arrays
        """
        logger.info("Training begins!")

        history = self.model.fit(
            x                   = first_array,
            y                   = second_array,
            batch_size          = self.batch_size,
            validation_split    = 0.3,
            epochs              = self.epochs,
            verbose             = 2
        )

        logger.info("Training finished!")
        return history

    def predict(self, input_array):
        """
        predicts the vector_q for each atom in input_array
            input_array is a matrix [num_of_atoms, num_of_descriptors]
            returns a matrix [num_of_atoms, num_of_phases]
        """
        return self.model.predict(input_array)

    def save_model(self, path):
        """
        saves model to 'path' folder
        """
        path_to_model = os.path.join(path, self.name + self.model_extension)
        if self.model is not None:
            self.model.save(path_to_model)
            logger.info("Model \'{}\' saved to file: {}".format(
                self.name, path_to_model))
        else:
            logger.error("Model \'{}\' was not saved.".format(self.name))

    def load_model(self, path):
        """
        loads model from 'path' to self.model and compiles it
        """
        path_to_model = os.path.join(path, self.name + self.model_extension)
        self.model = tf.keras.models.load_model(path_to_model)
        self.model.summary()
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
        self.model.compile(
            #optimizer   = tf.keras.optimizers.SGD(learning_rate = self.learning_rate),
            optimizer   = tf.keras.optimizers.Adam(self.lr_schedule),
            loss        = 'mse',
            metrics     = [tf.keras.metrics.MeanAbsoluteError()]
        )
        self.model.summary()
        logger.info("Model \'{}\' created.".format(self.name))
