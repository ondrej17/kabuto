import json
import os
import sys
import datetime
import shutil
import logging.config

import numpy as np

from modules.descriptors import Descriptors
from modules.neural_network import NeuralNetwork

# set-up the logger
logging.config.fileConfig(os.path.join('config', 'logger.ini'))
logger = logging.getLogger('kabuto')


class Kabuto:

    def __init__(self, action, option1, option2):
        """
        constructor of Kabuto class
        """
        self.print_intro()

        # initialize attributes
        self.nn = None  # neural-network object
        self.action = action
        self.option1 = option1
        self.option2 = option2

        # directory names that will be used
        self.to_train_dir = 'dir_to_train'
        self.trained_dir = 'dir_trained'
        self.to_predict_dir = "dir_to_predict"
        self.predicted_dir = "dir_predicted"
        self.config_dir = 'config'
        self.saved_nn_dir = 'saved_nn'
        self.result_dir = "results"

        # file with phases that will be identified
        self.phase_file = os.path.join("config", "phases_to_learn.txt")

        # these parameters are specific for each nn, change it in your case
        # dictionary of phases and positions in vector_q
        self.phases_available = self.load_available_phases()
        if self.phases_available is None:
            logger.error("Available phases were not loaded!")
            return
        self.number_of_phases = len(self.phases_available)
        self.number_of_descriptors = Descriptors.number_of_descriptors

        # create 'results' directory if it does not exist
        if os.path.isdir(self.result_dir):
            logger.info("Directory \'{}\' already exists.".format(self.result_dir))
        else:
            try:
                os.mkdir(self.result_dir)
            except OSError:
                logger.error("Creation of the \'{}\' directory failed".format(self.result_dir))

            else:
                logger.info("Successfully created the \'{}\' directory".format(self.result_dir))

        # based on option, call correct method
        if self.action == "prepare":
            # in future add a list of accepted phases
            if self.option1 is not None and self.option2 is not None:
                self.prepare(self.option1, self.option2)
            else:
                logger.error("Either phase or file not given")

        elif self.action == "list_nn":
            if self.option1 is None and self.option2 is None:
                self.list_nn()
            else:
                logger.error("Action \'{}\' takes no arguments".format(self.action))

        elif self.action == "create_nn":
            if self.option1 is not None and self.option2 is None:
                self.create_nn(self.option1)
            else:
                logger.error("Either no name of neural network given or more arguments given")

        elif self.action == "train":
            if self.option1 is not None and self.option2 is None:
                self.train(self.option1)
            else:
                logger.error("Either no name of neural network given or more arguments given")

        elif self.action == "predict":
            if self.option1 is not None and self.option2 is not None:
                self.predict(self.option1, self.option2)
            else:
                logger.error("Either no file given or name of nn not given")

        elif self.action == "test":
            if self.option1 is None and self.option2 is None:
                self.test()
            else:
                logger.error("Action \'{}\' takes no arguments".format(self.action))

        else:
            logger.error("You entered wrong action: {}\n"
                         "Possible actions:\n"
                         "    prepare <name_of_phase> <dump_file>\n"
                         "    list_nn\n"
                         "    create_nn <name_of_nn>\n"
                         "    train <name_of_nn>\n"
                         "    predict <path_to_file_with_structure>".format(self.action))

    def prepare(self, phase, file):
        """
        Documentation for 'prepare' function:
            * prepares files for training from dump-file
            * parses all atomic positions and calculates descriptors for each atom
            * for each timestep creates corresponding file in 'dir_to_train' folder
            * those file are then used to feed the NN (teaching of NN to identify given phases)
            * usage:
                * prepare(phase, file)
        """
        logger.info("ACTION: prepare\n"
                    "preparing phase: {}\n"
                    "preparing from file: {}".format(phase, file))

        # processing of file ...
        with open(file, "r") as input_file:

            # main dictionary that stores individual timesteps {timestep: atoms}
            timesteps = {}

            # scanning booleans (starts and stops scanning particular parts of input file)
            scan_timestep = False
            scan_atoms = False
            scan_number_of_atoms = False
            scan_pbc = False

            # current timestep for accessing main dictionary
            current_timestep = None
            number_of_pbc = 0
            pbc = [None, None, None]
            pbc_dict = dict()

            for raw_line in input_file:
                line = raw_line.strip()

                if line == "ITEM: TIMESTEP":
                    # scan for timestep in next line
                    scan_timestep = True
                    # stop scanning for atoms
                    scan_atoms = False

                elif scan_timestep:
                    logger.debug("Timestep: {}".format(repr(line)))
                    timesteps[line] = {}
                    current_timestep = line
                    scan_timestep = False

                elif line == "ITEM: NUMBER OF ATOMS":
                    # scan for number of atoms in next line
                    scan_number_of_atoms = True

                elif scan_number_of_atoms:
                    logger.debug("Number of atoms: {}".format(repr(line)))
                    # number_of_atoms = int(line)
                    scan_number_of_atoms = False

                elif line == "ITEM: BOX BOUNDS pp pp pp":
                    # scan for pbc in next three lines
                    scan_pbc = True

                elif scan_pbc:
                    logger.debug("PBC: {}".format(repr(line)))
                    min_value, max_value = tuple(line.split())
                    if number_of_pbc <= 2:  # load another pbc's
                        pbc[number_of_pbc] = float(max_value) - float(min_value)
                        number_of_pbc += 1
                    if number_of_pbc == 3:  # end loading pbc's
                        scan_pbc = False

                elif line == "ITEM: ATOMS id type xs ys zs":
                    timesteps[current_timestep] = {}
                    # store the pbc's in separate dictionary (timestep:list(pbc))
                    pbc_dict[current_timestep] = list(pbc)
                    logger.info("PBC (timestep #{}): {}".format(current_timestep, pbc))
                    # scan for atoms in next lines
                    scan_atoms = True

                elif scan_atoms:
                    logger.debug("Atom: {}".format(repr(line)))
                    atom_id, atom_type, atom_x, atom_y, atom_z = line.strip().split()
                    timesteps[current_timestep][int(atom_id)] = [float(atom_x), float(atom_y), float(atom_z), None]

                else:
                    # skipping useless lines
                    pass
        # all atoms are loaded in dictionary
        logger.info("Calculating of descriptors begins")

        # calculating of the descriptors for each atoms
        for timestep in timesteps.keys():
            logger.info("... processing timestep #{}".format(timestep))
            # prepare extended dictionary of atoms that contains also atoms due to PBC
            atoms_with_pbc = self.create_atoms_with_pbc(timesteps[timestep], pbc_dict[timestep])
            for id in timesteps[timestep].keys():
                # coordinates of current atom
                x = timesteps[timestep][id][0]
                y = timesteps[timestep][id][1]
                z = timesteps[timestep][id][2]
                logger.debug("... ... id: {}: [{}, {}, {}]".format(id, x, y, z))
                # calculate descriptors for current atom
                descriptors = Descriptors(id, x, y, z, atoms_with_pbc).get_descriptors()
                # add descriptors to the dictionary
                timesteps[timestep][id][3] = descriptors
                logger.info("Atom: {}".format(id))
                logger.info("Descriptors: {}".format(descriptors))

        logger.info("Calculating of descriptors ended")

        # save dictionary to json file
        with open(self.config_dir + os.path.sep + "dict_timesteps.json", "w") as json_file:
            json.dump(timesteps, json_file)
            logger.info("Dictionary 'timesteps' was saved to: dict_timesteps.json")

        # save dictionary to json file
        with open(self.config_dir + os.path.sep + "dict_pbc.json", "w") as json_file:
            json.dump(pbc_dict, json_file)
            logger.info("Dictionary 'pbc_dict' was saved to: dict_pbc.json")

        # save timesteps to separate files in 'dir_to_train' output_dir
        # create output_dir for saving timesteps (if it does not exist)
        if os.path.isdir(self.to_train_dir):
            logger.info("Directory {} already exists.".format(self.to_train_dir))
        else:
            try:
                os.mkdir(self.to_train_dir)
            except OSError:
                logger.error("Creation of the directory {} failed".format(self.to_train_dir))
            else:
                logger.info("Successfully created the directory {}".format(self.to_train_dir))

        # each timestep is saved to different file
        # filename = date_time_timestep, e.g. 2020_03_28_09_42_45_500.txt

        logger.info("Saving timesteps to separate file begins")

        for timestep in timesteps.keys():
            # create specific filename
            filename = datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S_") + str(timestep) + ".txt"
            path_to_file = os.path.join(self.to_train_dir, filename)
            logger.info("... saving timestep #{} to file {}".format(timestep, path_to_file))

            # open file
            with open(path_to_file, 'w') as file:
                # print informative header
                file.write(Descriptors.info_header(timestep, phase))

                # print descriptors for each atom to file
                for id in timesteps[timestep].keys():
                    file.write(str(id) + ' ' + ' '.join(map(str, timesteps[timestep][id][3])) + '\n')

        # all files are prepared in 'dir_to_train' folder
        logger.info("All timesteps were saved in \'{}\' folder".format(self.to_train_dir))

    def list_nn(self):
        """
        Documentation for 'list_nn' function:
            * lists all nn models saved in 'saved_nn' directory
            * only nn from this list can be taught
            * using self.create_nn, new nn can be added to this directory
            * usage:
                * list_nn()
        """
        logger.info("ACTION: list_nn\n"
                    "listing all saved neural networks ...")

        # create saved_nn_dir for saving models of NN (if it does not exist)
        if os.path.isdir(self.saved_nn_dir):
            logger.info("Directory \'{}\' already exists.".format(self.saved_nn_dir))
        else:
            try:
                os.mkdir(self.saved_nn_dir)
            except OSError:
                logger.error("Creation of directory \'{}\' failed".format(self.saved_nn_dir))
            else:
                logger.info("Successfully created directory \'{}\'".format(self.saved_nn_dir))

        # list all files in saved_nn_dir and save it to models
        # saved model has extension .h5
        models = []
        model_extension = ".h5"
        for file in os.listdir(self.saved_nn_dir):
            if os.path.isfile(os.path.join(self.saved_nn_dir, file)) and file[-3:] == model_extension:
                # cut the extension out and add the name of NN to the list
                models.append(file.replace(model_extension, ""))

        # print models out
        string_of_models = self.models_to_string(models)
        logger.info("Listing all saved neural networks:\n{}".format(string_of_models))
        logger.info("Listing ended")

    def create_nn(self, name):
        """
        Documentation for 'create_nn' function:
            * creates a new neural network model in 'saved_nn' directory
            * it is a raw neural network, no teaching yet
            * usage:
                * create_nn(name)
        """
        logger.info("ACTION: create_nn\n"
                    "creating neural network \'{}\'".format(name))

        # create saved_nn_dir for saving models of NN (if it does not exist)
        if os.path.isdir(self.saved_nn_dir):
            logger.info("Directory \'{}\' already exists.".format(self.saved_nn_dir))
        else:
            try:
                os.mkdir(self.saved_nn_dir)
            except OSError:
                logger.error("Creation of directory \'{}\' failed".format(self.saved_nn_dir))
            else:
                logger.info("Successfully created directory \'{}\'".format(self.saved_nn_dir))

        # find all files in saved_nn_dir and save it to models
        models = []
        model_extension = ".h5"
        for item in os.listdir(self.saved_nn_dir):
            if os.path.isfile(os.path.join(self.saved_nn_dir, item)) and item[-3:] == model_extension:
                # cut the extension out
                models.append(item.replace(model_extension, ""))

        if name in models:
            # if 'name' is in 'saved_nn' directory, do nothing
            logger.info("Neural network \'{}\' already exists.".format(name))
        else:
            # else, create a new neural network and save its model to <name>.h5 file in 'saved_nn' directory
            nn = NeuralNetwork(name)
            nn.create_model(self.number_of_descriptors, self.number_of_phases)
            nn.save_model()

    def train(self, name):
        """
        Documentation for 'train' function:
            * trains given neural network on all files in 'dir_to_train' folder
            * these files were prepared by 'prepare' function
            * after training, all trained file are moved to the 'dir_trained' folder
            * usage:
                * train(name)
        """
        logger.info("ACTION: train\n"
                    "\'{}\' is training from \'{}\' directory".format(name, self.to_train_dir))

        # check whether the name is in saved_nn directory
        # create saved_nn_dir for saving models of NN (if it does not exist)
        if os.path.isdir(self.saved_nn_dir):
            logger.info("Directory \'{}\' already exists.".format(self.saved_nn_dir))
        else:
            try:
                os.mkdir(self.saved_nn_dir)
            except OSError:
                logger.error("Creation of directory \'{}\' failed".format(self.saved_nn_dir))
            else:
                logger.info("Successfully created directory \'{}\'".format(self.saved_nn_dir))

        # find all files in saved_nn_dir and save it to models
        models = []
        model_extension = ".h5"
        for item in os.listdir(self.saved_nn_dir):
            if os.path.isfile(os.path.join(self.saved_nn_dir, item)) and item[-3:] == model_extension:
                # cut the extension out
                models.append(item.replace(model_extension, ""))

        if name in models:

            # prepare two lists, one with descriptors, second one with vector q_i
            first_array, second_array, timestep = self.prepare_arrays(self.to_train_dir)
            if first_array is None or second_array is None:
                logger.error("The interrupting of the training NN!")
                return

            # prepare NN
            self.nn = NeuralNetwork(name)
            self.nn.load_model()

            # let the NN train
            self.nn.train(first_array, second_array)

            # at the end, save the model
            self.nn.save_model()

            # move all files from 'prepare_to_training' dir to 'dir_trained' dir
            self.move_files_from_to(self.to_train_dir, self.trained_dir)

        else:
            # if 'name' is in 'saved_nn' directory, do nothing
            logger.error("Neural network \'{}\' does not exist!".format(name))

    def predict(self, name, filename):
        """
        Documentation for 'predict' function:
            * predicts the global structure at each timestep that is in given file
            * main result is a dictionary {phase:percentage}, which is stored in 'result' folder
        """
        logger.info("ACTION: predict\n"
                    "predicting ...")

        # processing of file ...
        with open(filename, "r") as input_file:

            # main dictionary that stores individual timesteps (timestep: atoms)
            timesteps = {}

            # scanning booleans (starts and stops scanning parts of input file)
            scan_timestep = False
            scan_atoms = False
            scan_number_of_atoms = False
            scan_pbc = False

            # current timestep for accessing main dictionary
            current_timestep = None
            number_of_pbc = 0
            pbc = [None, None, None]
            pbc_dict = dict()

            for raw_line in input_file:
                line = raw_line.strip()

                if line == "ITEM: TIMESTEP":
                    # scan for timestep in next line
                    scan_timestep = True
                    # stop scanning for atoms
                    scan_atoms = False

                elif scan_timestep:
                    logger.debug("Timestep: {}".format(repr(line)))
                    timesteps[line] = {}
                    current_timestep = line
                    scan_timestep = False

                elif line == "ITEM: NUMBER OF ATOMS":
                    # scan for number of atoms in next line
                    scan_number_of_atoms = True

                elif scan_number_of_atoms:
                    logger.debug("Number of atoms: {}".format(repr(line)))
                    # number_of_atoms = int(line)
                    scan_number_of_atoms = False

                elif line == "ITEM: BOX BOUNDS pp pp pp":
                    # scan for pbc in next three lines
                    scan_pbc = True

                elif scan_pbc:
                    logger.debug("PBC: {}".format(repr(line)))
                    min_value, max_value = tuple(line.split())
                    if number_of_pbc <= 2:  # load another pbc's
                        pbc[number_of_pbc] = float(max_value) - float(min_value)
                        number_of_pbc += 1
                    if number_of_pbc == 3:  # end loading pbc's
                        scan_pbc = False

                elif line == "ITEM: ATOMS id type xs ys zs":
                    timesteps[current_timestep] = {}
                    # store the pbc's in separate dictionary (timestep:list(pbc))
                    pbc_dict[current_timestep] = list(pbc)
                    logger.info("PBC (timestep #{}): {}".format(current_timestep, pbc))
                    # scan for atoms in next lines
                    scan_atoms = True

                elif scan_atoms:
                    logger.debug("Atom: {}".format(repr(line)))
                    atom_id, atom_type, atom_x, atom_y, atom_z = line.strip().split()
                    timesteps[current_timestep][int(atom_id)] = [float(atom_x), float(atom_y), float(atom_z), None]

                else:
                    # skipping useless lines
                    pass
        # all atoms are loaded in dictionary
        logger.info("Calculating of descriptors begins")

        # calculating the descriptors for each atoms
        for timestep in timesteps.keys():
            logger.info("... processing timestep #{}".format(timestep))
            # prepare extended dictionary of atoms that contains also atoms due to PBC
            atoms_with_pbc = self.create_atoms_with_pbc(timesteps[timestep], pbc_dict[timestep])
            for id in timesteps[timestep].keys():
                # coordinates of current atom
                x = timesteps[timestep][id][0]
                y = timesteps[timestep][id][1]
                z = timesteps[timestep][id][2]
                logger.debug("... ... id: {}: [{}, {}, {}]".format(id, x, y, z))
                # calculate descriptors for current atom
                descriptors = Descriptors(id, x, y, z, atoms_with_pbc).get_descriptors()
                # add descriptors to the dictionary
                timesteps[timestep][id][3] = descriptors
                logger.info("Atom: {}".format(id))
                logger.info("Descriptors:".format(descriptors))

        logger.info("Calculating of descriptors ended")

        # save dictionary to json file
        with open(self.config_dir + os.path.sep + "dict_timesteps.json", "w") as json_file:
            json.dump(timesteps, json_file)
            logger.info("Dictionary 'timesteps' was saved to: dict_timesteps.json")

        # save dictionary to json file
        with open(self.config_dir + os.path.sep + "dict_pbc.json", "w") as json_file:
            json.dump(pbc_dict, json_file)
            logger.info("Dictionary 'pbc_dict' was saved to: dict_pbc.json")

        # save timesteps to separate files in 'dir_to_predict' folder
        # create to_predict_dir for saving timesteps (if it does not exist)
        if os.path.isdir(self.to_predict_dir):
            logger.info("Directory {} already exists.".format(self.to_predict_dir))
        else:
            try:
                os.mkdir(self.to_predict_dir)
            except OSError:
                logger.error("Creation of the directory {} failed".format(self.to_predict_dir))
            else:
                logger.info("Successfully created directory {}".format(self.to_predict_dir))

        # each timestep is saved to different file
        # filename = date_time_timestep, e.g. 2020_03_28_09_42_45_500.txt

        for timestep in timesteps.keys():
            # create specific filename
            filename = datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S_") + str(timestep) + ".txt"
            path_to_file = os.path.join(self.to_predict_dir, filename)
            logger.debug("... saving timestep #{} to file {}".format(timestep, path_to_file))

            # open file
            with open(path_to_file, 'w') as file:
                # print informative header
                file.write(Descriptors.info_header(timestep, phase=None))

                # print descriptors for each atom to file
                for id in timesteps[timestep].keys():
                    file.write(str(id) + ' ' + ' '.join(map(str, timesteps[timestep][id][3])) + '\n')

        # all files are prepared in 'dir_to_predict' folder
        logger.info("All timesteps were saved to \'{}\' folder".format(self.to_predict_dir))

        # check whether the name is in saved_nn directory
        if os.path.isdir(self.saved_nn_dir):
            logger.info("Directory \'{}\' already exists.".format(self.saved_nn_dir))
        else:
            logger.error("Directory \'{}\' does not exist!".format(self.saved_nn_dir))
            return None

        # find all files in saved_nn_dir and save it to models
        models = []
        model_extension = ".h5"
        for item in os.listdir(self.saved_nn_dir):
            if os.path.isfile(os.path.join(self.saved_nn_dir, item)) and item[-3:] == model_extension:
                # cut the extension out and save name to list
                models.append(item.replace(model_extension, ""))

        # initialize a dictionary that holds result
        global_structure_dict = dict()

        # we have existing NN
        if name in models:
            for root, directories, files in os.walk(self.to_predict_dir):

                # for each file in 'dir_to_predict' folder do:
                for filename in sorted(files):

                    # prepare two lists, one with descriptors, second one with None
                    input_array, second_array, timestep = self.prepare_arrays(self.to_predict_dir, filename)
                    if input_array is None or second_array is not None or timestep is None:
                        logger.error("The interrupting of the predicting!")
                        return

                    # prepare NN, load model
                    self.nn = NeuralNetwork(name)
                    self.nn.load_model()

                    # let the NN predict something
                    # output is vector q (local structure) for each atom in file at that timestep
                    # i.e. a numpy.ndarray [num_atoms, num_phases]
                    prediction = self.nn.predict(input_array)

                    # I have a prediction!
                    logger.info("prediction for file \'{}\'\n{}".format(filename, prediction))

                    # calculate the vector_Q (global structure) from vector_q (local structures)
                    vector_big_q = self.calculate_vector_big_q(prediction)

                    # I have vector Q that has information about global structure at given timestep
                    logger.debug("Q = {}".format(vector_big_q))

                    # add another timestep to results [phase:percentage]
                    global_structure_dict[timestep] = self.create_dict_phase_percentage(vector_big_q)

            # move all files from 'dir_to_predict' folder to 'dir_predicted' folder
            self.move_files_from_to(self.to_predict_dir, self.predicted_dir)

            # print result (global structure info)
            logger.info("RESULT:\n{}".format(global_structure_dict))

            # save results to 'results' dir
            self.save_results(global_structure_dict)

            logger.info("End of predicting.")

        else:
            # if 'name' is in 'saved_nn' directory, do nothing
            logger.error("Neural network \'{}\' does not exist!".format(name))

    @staticmethod
    def test():
        """
        Documentation for 'test' function:
            * a method for the testing of the features
        """
        logger.info("ACTION: test\n"
                    "Entering TEST mode. Object KABUTO created. ...")

        # test return values of functions in descriptors module
        test_descriptors = Descriptors(id=1, x=0, y=0, z=0, atoms_with_pbc=dict())
        logger.info("symmetry function parameters dictionary:\n{}"
                    .format(test_descriptors.symmetry_functions_parameters))
        logger.info("f_c(0) = {}".format(test_descriptors.f_c(0, 6.2, 6.4)))
        logger.info("f_c(6.2) = {}".format(test_descriptors.f_c(6.2, 6.2, 6.4)))
        logger.info("f_c(6.3) = {}".format(test_descriptors.f_c(6.3, 6.2, 6.4)))
        logger.info("f_c(6.4) = {}".format(test_descriptors.f_c(6.4, 6.2, 6.4)))
        logger.info("f_c(10) = {}".format(test_descriptors.f_c(10, 6.2, 6.4)))
        # logger.info("scipy version = {}".format(scipy.__version__))
        logger.info("y_00 = {}".format(test_descriptors.y_lm(0, 0, 1, 0, 0)))
        logger.info("y_42 = {}".format(test_descriptors.y_lm(4, 2, 1, 0, 0)))
        logger.info("y_20 = {}".format(test_descriptors.y_lm(2, 0, 1, 0, 0)))
        # logger.info("srt(2) * y_4^2 = {}".format(scipy.special.sph_harm(2, 4, 0, math.pi / 2) * math.sqrt(2)))

    def prepare_arrays(self, directory=None, filename=None):
        """
        * prepares two arrays, input data, either from all files in 'directory' or from a file 'directory + filename'
        * first array contains arrays of descriptors
        * second array contains arrays of 1 and 0s
            * position of 1 is determined by phase
            * calls function create_output_vector(phase)
        """

        if filename is None and directory is not None:
            input_array, output_array = [], []
            logger.info("Preparing arrays from directory: \'{}\'".format(directory))

            for root, directories, files in os.walk(directory):
                if not files:
                    logger.error("No files in \'{}\'".format(directory))
                    return None, None, None
                for filename in sorted(files):
                    # process each file
                    logger.debug("... processing file: {}".format(filename))
                    output_vector = None

                    with open(os.path.join(directory, filename)) as file:
                        for line in file:
                            if line[0] == '#':
                                # processing info header
                                if "phase" in line:
                                    # find phase that is about to be learned
                                    phase = line.split()[2]
                                    output_vector = self.create_output_vector(phase)
                                    if output_vector is None:
                                        logger.error("The interrupting of the preparing of arrays!")
                                        return None, None, None
                            else:
                                # processing a line with descriptors: [id, **descriptors]
                                items = line.split()
                                descriptors = list(map(float, items[1:]))
                                logger.debug("{} : {}".format(id, descriptors))

                                # add output_vector to output array
                                output_array.append(output_vector)

                                # add descriptors to input array
                                input_array.append(descriptors)

            logger.info("Input and output arrays have the same length: {}"
                        .format(len(input_array) == len(output_array)))

            logger.debug("... Descriptors:\n{}".format(np.array(input_array, dtype=float)))
            logger.debug("... Output vector:\n{}".format(np.array(output_array, dtype=float)))

            # return numpy array, tensorflow likes it
            return np.array(input_array, dtype=float), np.array(output_array, dtype=float), None

        elif filename is not None and directory is not None:
            logger.info("Preparing only input array from the file: \'{}\'".format(os.path.join(directory, filename)))

            input_array, output_array, timestep = [], None, None

            # processing a file
            try:
                with open(os.path.join(directory, filename)) as file:
                    for line in file:
                        if line[0] == '#':
                            # processing info header
                            if "timestep" in line:
                                # find phase that is about to be learned
                                timestep = line.split()[2]
                        else:
                            # processing a line with descriptors: [id, **descriptors]
                            items = line.split()
                            descriptors = list(map(float, items[1:]))
                            logger.debug("{} : {}".format(id, descriptors))

                            # add descriptors to input array
                            input_array.append(descriptors)

                logger.debug("... Descriptors:\n{}".format(np.array(input_array, dtype=float)))

                # return numpy array, tensorflow likes it
                return np.array(input_array, dtype=float), None, timestep

            except FileNotFoundError:
                logger.error("File {} not found!".format(filename))
                return None, None, None

        else:
            logger.error("Wrong use of \'prepare_arrays()\' function!")
            return None, None, None

    def create_output_vector(self, phase):
        """
        creates an output vector for neural network
            * it is a array of 0s and 1
            * 1 is at the position of given phase
        """

        if phase not in self.phases_available.keys():
            logger.error("Given phase is not one of the available phases!")
            return None

        # create output vector
        vector_q = [0] * self.number_of_phases

        # change correct place in vector_q
        try:
            vector_q[self.phases_available[phase]] = 1
        except IndexError:
            logger.error("Problem with available_phases attribute in Kabuto class!")
            return None

        logger.info("vector_q: {}".format(vector_q))
        return vector_q

    def load_available_phases(self):
        """
        loads a list of available phases from a file self.phase_file into the dictionary
            * comments (lines beginning with '#') are allowed
            * new line, new phase
        """
        phases_dict = dict()
        index = 0
        try:
            with open(self.phase_file, "r") as file:
                for line in file:
                    # skip the commented lines
                    # phase must be one word
                    if line.strip() != '' and line.split()[0] != '#' and len(line.split()) == 1:
                        phases_dict[line.strip()] = index
                        index += 1
        except FileNotFoundError:
            logger.error("File \'{}\' not found!".format(self.phase_file))
            return None

        logger.info("Available phases: {}".format(phases_dict))
        return phases_dict

    def calculate_vector_big_q(self, prediction):
        """
        returns the vector Q, that contains information about global structure
            * len(Q) = self.number_of_phases
            * each component is an average percentage of particular phase in all system
        """
        vector = [0] * self.number_of_phases
        n = len(prediction.tolist())
        logger.info("Number of atoms in prediction: {}".format(n))
        for i, q_i in enumerate(prediction.tolist()):  # rows
            for j, q_ij in enumerate(q_i):  # columns
                vector[j] += q_ij
        return [q_i / n for q_i in vector]

    def create_dict_phase_percentage(self, vector_big_q):
        """
        returns a dictionary {phase:percentage}
            percentage is from vector Q (global structure)
        """
        result_dict = dict()
        for phase, index in self.phases_available.items():
            result_dict[phase] = vector_big_q[index]
        return result_dict

    @staticmethod
    def print_timesteps(timesteps):
        """
        prints timesteps dictionary in well arranged way
        """
        logger.debug("Timesteps:")
        for timestep, atoms in timesteps.items():
            logger.debug("... Timestep: {}".format(timestep))
            for atom, coords in atoms.items():
                logger.debug("... ... Atom #{}:\t{}".format(atom, coords))

    @staticmethod
    def print_intro():
        """
        prints logo of KABUTO in nice way
        """
        logger.info("\n******************************************************\n"
                    "                   ___            _______    ____\n"
                    "   | /     /\\     |   |   |    |     |      /    \\\n"
                    "   |<     /__\\    |--<    |    |     |     |      |\n"
                    "   | \\   /    \\   |___|    \\__/      |      \\____/\n"
                    "******************************************************\n"
                    "                   Ondrej Bily\n"
                    "                  Diploma Thesis\n"
                    "                       2020\n"
                    "******************************************************\n")

    @staticmethod
    def models_to_string(models):
        to_print = ""
        for model in models:
            to_print += "... {}\n".format(model)
        return to_print.strip()

    @staticmethod
    def move_files_from_to(from_dir, to_dir):
        """
        moves all files from 'from_dir' to 'to_dir'
        """
        logger.info("Moving files ...")
        # create to_dir if it does not exist)
        if os.path.isdir(to_dir):
            logger.info("Directory {} already exists.".format(to_dir))
        else:
            try:
                os.mkdir(to_dir)
            except OSError:
                logger.error("Creation of the directory {} failed".format(to_dir))

            else:
                logger.info("Successfully created the directory {}".format(to_dir))
        files = os.listdir(from_dir)
        for filename in files:
            shutil.move(os.path.join(from_dir, filename), to_dir)

        logger.info("Files successfully moved from \'{}\' to \'{}\'".format(from_dir, to_dir))

    @staticmethod
    def dict_to_string(dictionary):
        """
        returns a string representation of a dictionary
        """
        result = ''
        for key, value in dictionary.items():
            result += "--> {} : {}\n".format(key, value)
        return result.strip()

    def save_results(self, global_structure_dict):
        """
        saves results (dictionary [timestep:[phase:percentage]]) to file in format:
            * # timestep phase1 phase2 .... phaseN
            * ...
        """
        # create specific filename
        filename = datetime.datetime.today().strftime("results_%Y_%m_%d_%H_%M_%S") + ".txt"
        path_to_file = os.path.join(self.result_dir, filename)

        logger.info("Saving results to file: \'{}\'".format(path_to_file))

        # prepare first descriptive line
        first_line = "timestep\t" + '\t'.join(self.phases_available.keys()) + "\n"

        try:
            with open(path_to_file, "w") as file:
                # write first line that describes each column
                file.write(first_line)

                # write other lines from dictionary
                for timestep in global_structure_dict.keys():
                    line = str(timestep) + "\t"
                    line += '\t'.join(list(map(str, global_structure_dict[timestep].values()))) + '\n'
                    file.write(line)
        except FileNotFoundError:
            logger.error("Problem with opening the file: {}".format(path_to_file))

    @staticmethod
    def create_atoms_with_pbc(atoms, pbc):
        """
        returns a dictionary that contains original atoms and their copies to each direction
            * it is a way to fulfill PBC (periodic boundary condition)
            * pbc parameter is list of three numbers, period in x, y and z direction
            * the added atoms should have different id than the original atoms
            * atoms is dictionary {id:[x, y, z, None]}, where None is reserved place for Descriptors
        """
        atoms_with_pbc = dict()
        r_x, r_y, r_z = pbc[0], pbc[1], pbc[2]

        max_id = max(map(int, list(atoms.keys()))) + 1  # 1 is for a case id = 0
        logger.info("Maximal ID of atom: {}".format(max_id))

        # go through the dictionary 'atoms' and add 27 atoms to the atoms_with_pbc dictionary
        # why 27? The original one and 26 new atoms due to the pbc
        for id, atom in atoms.items():
            x, y, z = atom[0], atom[1], atom[2]

            # add the original atom
            atoms_with_pbc[id] = [x, y, z, None]

            # add the other 26 atoms with different id number
            atoms_with_pbc[id + 1 * max_id] = [x + r_x, y, z, None]
            atoms_with_pbc[id + 2 * max_id] = [x, y + r_y, z, None]
            atoms_with_pbc[id + 3 * max_id] = [x, y, z + r_z, None]

            atoms_with_pbc[id + 4 * max_id] = [x - r_x, y, z, None]
            atoms_with_pbc[id + 5 * max_id] = [x, y - r_y, z, None]
            atoms_with_pbc[id + 6 * max_id] = [x, y, z - r_z, None]

            atoms_with_pbc[id + 7 * max_id] = [x + r_x, y + r_y, z, None]
            atoms_with_pbc[id + 8 * max_id] = [x + r_x, y - r_y, z, None]
            atoms_with_pbc[id + 9 * max_id] = [x - r_x, y + r_y, z, None]
            atoms_with_pbc[id + 10 * max_id] = [x - r_x, y - r_y, z, None]

            atoms_with_pbc[id + 11 * max_id] = [x + r_x, y, z + r_z, None]
            atoms_with_pbc[id + 12 * max_id] = [x + r_x, y, z - r_z, None]
            atoms_with_pbc[id + 13 * max_id] = [x - r_x, y, z + r_z, None]
            atoms_with_pbc[id + 14 * max_id] = [x - r_x, y, z - r_z, None]

            atoms_with_pbc[id + 15 * max_id] = [x, y + r_y, z + r_z, None]
            atoms_with_pbc[id + 16 * max_id] = [x, y + r_y, z - r_z, None]
            atoms_with_pbc[id + 17 * max_id] = [x, y - r_y, z + r_z, None]
            atoms_with_pbc[id + 18 * max_id] = [x, y - r_y, z - r_z, None]

            atoms_with_pbc[id + 19 * max_id] = [x + r_x, y + r_y, z + r_z, None]
            atoms_with_pbc[id + 20 * max_id] = [x + r_x, y + r_y, z - r_z, None]
            atoms_with_pbc[id + 21 * max_id] = [x + r_x, y - r_y, z + r_z, None]
            atoms_with_pbc[id + 22 * max_id] = [x + r_x, y - r_y, z - r_z, None]
            atoms_with_pbc[id + 23 * max_id] = [x - r_x, y + r_y, z + r_z, None]
            atoms_with_pbc[id + 24 * max_id] = [x - r_x, y + r_y, z - r_z, None]
            atoms_with_pbc[id + 25 * max_id] = [x - r_x, y - r_y, z + r_z, None]
            atoms_with_pbc[id + 26 * max_id] = [x - r_x, y - r_y, z - r_z, None]

        return atoms_with_pbc


# global function
def print_kabuto_intro():
    result = "\n******************************************************\n" \
             "                   ___            _______    ____\n" \
             "   | /     /\\     |   |   |    |     |      /    \\\n" \
             "   |<     /__\\    |--<    |    |     |     |     |\n" \
             "   | \\   /    \\   |___|    \\__/      |      \\____/\n" \
             "******************************************************\n" \
             "                   Ondrej Bily\n" \
             "                  Diploma Thesis\n" \
             "                       2020\n" \
             "******************************************************\n" \
             "Usage:\n" \
             "    kabuto.py prepare <name_of_phase> <dump_file>\n" \
             "    kabuto.py list_nn\n" \
             "    kabuto.py create_nn <name_of_nn>\n" \
             "    kabuto.py train <name_of_nn>\n" \
             "    kabuto.py predict <name_of_nn> <dump.file>\n" \
             "    kabuto.py test\n" \
             "******************************************************\n"
    return result


################################################################
# create Kabuto Machine iff there is correct number of arguments
################################################################
logger.info("Command line arguments:\n{}".format(' '.join(sys.argv)))
if len(sys.argv) == 2:
    # script called with one argument (action)
    Kabuto(action=sys.argv[1], option1=None, option2=None)
elif len(sys.argv) == 3:
    # script called with two arguments (action, option)
    Kabuto(action=sys.argv[1], option1=sys.argv[2], option2=None)
elif len(sys.argv) == 4:
    # script called with three arguments (action, phase/name, file)
    Kabuto(action=sys.argv[1], option1=sys.argv[2], option2=sys.argv[3])
else:
    # script called without action
    logger.info(print_kabuto_intro())
