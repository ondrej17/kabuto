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

        self.max_epochs = 100
        self.batch_size = 100
        self.steps_per_epoch = 10000 // self.batch_size

    def create_layers(self):
        """
        returns an array of keras layers
        """
        output_size = self.number_of_phases
        input_size = self.number_of_descriptors
        nodes = 16  # 25

        layers = [
            tf.keras.Input(shape=(input_size,), dtype='float32'),
            tf.keras.layers.Dense(units=nodes, activation='elu'),
            tf.keras.layers.Dense(units=nodes, activation='elu'),
            tf.keras.layers.Dense(units=output_size)
        ]
        return layers

    def train(self, first_array, second_array):
        """
        trains the current nn from input arrays
        """
        logger.info("Training begins!")

        history = self.model.fit(x=first_array,
                                 y=second_array,
                                 steps_per_epoch=self.steps_per_epoch,
                                 validation_split=0.3,
                                 epochs=self.max_epochs,
                                 shuffle=True,
                                 verbose=2)

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

        # prepare scheduler
        lr_schedule = tf.keras.optimizers.schedules.InverseTimeDecay(
            0.00001,
            decay_steps=self.steps_per_epoch*50,
            decay_rate=1,
            staircase=False)

        # define the layers
        layers = self.create_layers()

        # create the model
        self.model = tf.keras.Sequential(layers)

        # compile the model
        self.model.compile(optimizer=tf.keras.optimizers.Adam(0.00001),
                           loss='mean_squared_error',
                           metrics=['accuracy'])
        self.model.summary()
        logger.info("Model \'{}\' created.".format(self.name))
