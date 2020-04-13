import json
import os
import sys
import datetime
import numpy as np
import shutil

from modules.descriptors import Descriptors
from modules.neural_network import NeuralNetwork


class Kabuto:

    def __init__(self, action, option1, option2):
        """
        constructor of Kabuto class
        """
        self.print_intro()

        # initialize attributes
        self.nn = None
        self.action = action
        self.option1 = option1
        self.option2 = option2
        self.output_dir = 'prepared_for_training'
        self.tmp_dir = 'temporary'
        self.saved_nn_dir = 'saved_nn'
        self.trained_dir = 'trained'
        self.phase_file = os.path.join("modules", "phases_to_learn.txt")
        self.to_predict_dir = "prepared_for_predicting"
        self.predicted_dir = "predicted"

        # these parameters are specific for each nn, change it in your case
        # dictionary of phases and positions in vector_q
        self.phases_available = self.load_available_phases()
        if self.phases_available is None:
            print("ERROR: Available phases were not loaded!")
            return
        self.number_of_phases = len(self.phases_available)
        self.number_of_descriptors = Descriptors.number_of_descriptors

        # based on option, call correct method
        if self.action == "prepare":
            # in future add a list of accepted phases
            if self.option1 is not None and self.option2 is not None:
                self.prepare(self.option1, self.option2)
            else:
                print("ERROR: Either phase or file not given")

        elif self.action == "list_nn":
            if self.option1 is None and self.option2 is None:
                self.list_nn()
            else:
                print("ERROR: action \'list_nn\' takes no arguments")

        elif self.action == "create_nn":
            if self.option1 is not None and self.option2 is None:
                self.create_nn(self.option1)
            else:
                print("ERROR: either no name of neural network given or more arguments given")

        elif self.action == "train":
            if self.option1 is not None and self.option2 is None:
                self.train(self.option1)
            else:
                print("ERROR: either no name of neural network given or more arguments given")

        elif self.action == "predict":
            if self.option1 is not None and self.option2 is not None:
                self.predict(self.option1, self.option2)
            else:
                print("ERROR: either no file given or name of nn not given")

        elif self.action == "test":
            if self.option1 is None and self.option2 is None:
                self.test()
            else:
                print("ERROR: action \'list_nn\' takes no arguments")

        else:
            print("You entered wrong action: {}\n"
                  "Possible actions:\n"
                  "    prepare <name_of_phase> <dump_file>\n"
                  "    list_nn\n"
                  "    create_nn <name_of_nn>\n"
                  "    train <name_of_nn>\n"
                  "    predict <path_to_file_with_structure>\n".format(self.action))

    def prepare(self, phase, file):
        """
        Documentation for 'prepare' function:
            > prepares files for training from dump-file
            > parses all atomic positions and calculates values of 14 functions for each atom
            > for each timestamp creates corresponding file in 'prepared_for_training' folder
            > those file are then used to feed the NN (teaching of NN to identify given phase)
            > usage:
                prepare(phase, file)
        """
        print("ACTION: prepare\n"
              "preparing phase: {}\n"
              "preparing from file: {}\n"
              "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^".format(phase, file))

        # processing of file ...
        with open(file, "r") as input_file:

            # main dictionary that stores individual timesteps (timestep: atoms)
            timesteps = {}

            # scanning booleans (starts and stops scanning parts of input file)
            scan_timestep = False
            scan_atoms = False
            scan_number_of_atoms = False

            # current timestep for accessing main dictionary
            current_timestep = None

            for raw_line in input_file:
                line = raw_line.strip()

                if line == "ITEM: TIMESTEP":
                    # scan for timestep in next line
                    scan_timestep = True
                    # stop scanning for atoms
                    scan_atoms = False

                elif scan_timestep:
                    # print("Timestamp:", repr(line))
                    timesteps[line] = {}
                    current_timestep = line
                    scan_timestep = False

                elif line == "ITEM: NUMBER OF ATOMS":
                    # scan for number of atoms in next line
                    scan_number_of_atoms = True

                elif scan_number_of_atoms:
                    # print("Number of atoms:", repr(line))
                    # number_of_atoms = int(line)
                    scan_number_of_atoms = False

                elif line == "ITEM: ATOMS id type xs ys zs":
                    timesteps[current_timestep] = {}
                    # scan for atoms in next lines
                    scan_atoms = True

                elif scan_atoms:
                    # print("Atom:", repr(line))
                    atom_id, atom_type, atom_x, atom_y, atom_z = line.strip().split()
                    timesteps[current_timestep][atom_id] = [float(atom_x), float(atom_y), float(atom_z), None]

                else:
                    # skipping useless lines
                    pass
        # all atoms are loaded in dictionary

        # calculating the values of 14 functions for each atoms
        for timestep in timesteps.keys():
            print("... processing timestep #", timestep)
            for id in timesteps[timestep].keys():
                # coordinates of current atom
                x = timesteps[timestep][id][0]
                y = timesteps[timestep][id][1]
                z = timesteps[timestep][id][2]
                print("... ... id: {}: [{}, {}, {}]".format(id, x, y, z))
                # calculate descriptors for current atom
                descriptors = Descriptors(id, x, y, z, timesteps[timestep]).get_descriptors()
                # add descriptors to the dictionary
                timesteps[timestep][id][3] = descriptors
                # print("Descriptors:", descriptors)

        # save dictionary to json file
        with open(self.tmp_dir + os.path.sep + "dict_timesteps.json", "w") as json_file:
            json.dump(timesteps, json_file)
            print("INFO: dictionary 'timesteps' was saved to: dict_timesteps.json")

        # print timesteps-dictionary
        # self.print_timesteps(timesteps)

        # save timesteps to separate files in 'prepared_for_training' output_dir ---?
        # create output_dir for saving timesteps (if it does not exist)
        if os.path.isdir(self.output_dir):
            print("INFO: output_dir {} already exists.".format(self.output_dir))
        else:
            try:
                os.mkdir(self.output_dir)
            except OSError:
                print("ERROR: Creation of the output_dir {} failed".format(self.output_dir))
            else:
                print("INFO: Successfully created the output_dir {}".format(self.output_dir))

        # each timestep is saved to different file
        # filename = date_time_timestep, e.g. 2020_03_28_09_42_45_500.txt

        for timestep in timesteps.keys():
            # create specific filename
            filename = datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S_") + str(timestep) + ".txt"
            path_to_file = os.path.join(self.output_dir, filename)
            print("... saving timestep #{} to file {}".format(timestep, path_to_file))

            # open file
            with open(path_to_file, 'w') as file:
                # print informative header
                file.write(Descriptors.info_header(timestep, phase))

                # print descriptors for each atom to file
                for id in timesteps[timestep].keys():
                    file.write(str(id) + ' ' + ' '.join(map(str, timesteps[timestep][id][3])) + '\n')

        # all files are prepared in 'prepared_for_training' folder
        print("INFO: all timesteps were saved in \'prepared_for_training\' folder")

    def list_nn(self):
        """
        Documentation for 'list_nn' function:
            > lists all nn models saved in 'saved_nn' directory
            > only nn from this list can be taught
            > using self.create_nn, new nn can be added to this directory
            > usage:
                list_nn()
        """
        print("ACTION: list_nn\n"
              "listing all saved neural networks ...\n"
              "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

        # list all files in self.saved_nn_dir
        # saved model has extension .h5
        # create saved_nn_dir for saving models of NN (if it does not exist)
        if os.path.isdir(self.saved_nn_dir):
            print("INFO: directory \'{}\' already exists.".format(self.saved_nn_dir))
        else:
            try:
                os.mkdir(self.saved_nn_dir)
            except OSError:
                print("ERROR: Creation of directory \'{}\' failed".format(self.saved_nn_dir))
            else:
                print("INFO: Successfully created directory \'{}\'".format(self.saved_nn_dir))

        # list all files in saved_nn_dir and save it to models
        models = []
        model_extension = ".h5"
        for item in os.listdir(self.saved_nn_dir):
            # print(item)
            if os.path.isfile(os.path.join(self.saved_nn_dir, item)) and item[-3:] == model_extension:
                # cut the extension out
                models.append(item.replace(model_extension, ""))

        # print models out
        print("INFO: listing all saved neural networks")
        self.print_nn_models(models)
        print("INFO: listing ended")

    def create_nn(self, name):
        """
        Documentation for 'create_nn' function:
            > creates a new model in 'saved_nn' directory
            > it is a raw neural network, no teaching yet
            > usage:
                create_nn(name)
        """
        print("ACTION: create_nn\n"
              "creating neural network \'{}\' ...\n"
              "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^".format(name))

        # create saved_nn_dir for saving models of NN (if it does not exist)
        if os.path.isdir(self.saved_nn_dir):
            print("INFO: directory \'{}\' already exists.".format(self.saved_nn_dir))
        else:
            try:
                os.mkdir(self.saved_nn_dir)
            except OSError:
                print("ERROR: Creation of directory \'{}\' failed".format(self.saved_nn_dir))
            else:
                print("INFO: Successfully created directory \'{}\'".format(self.saved_nn_dir))

        # find all files in saved_nn_dir and save it to models
        models = []
        model_extension = ".h5"
        for item in os.listdir(self.saved_nn_dir):
            # print(item)
            if os.path.isfile(os.path.join(self.saved_nn_dir, item)) and item[-3:] == model_extension:
                # cut the extension out
                models.append(item.replace(model_extension, ""))

        if name in models:
            # if 'name' is in 'saved_nn' directory, do nothing
            print("INFO: Neural network \'{}\' already exists.".format(name))
        else:
            # else, create a new neural network and save its model to <name>.h5 file in 'saved_nn' directory
            nn = NeuralNetwork(name)
            nn.create_model(self.number_of_descriptors, self.number_of_phases)
            nn.save_model()

    def train(self, name):
        """
        Documentation for 'train' function:
            > ...
            > ...
            > usage:
                train(name)
        """
        print("ACTION: train\n"
              "\'{}\' is training from \'prepared_for_training\' directory\n"
              "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^".format(name))

        # check whether the name is in saved_nn directory
        # create saved_nn_dir for saving models of NN (if it does not exist)
        if os.path.isdir(self.saved_nn_dir):
            print("INFO: directory \'{}\' already exists.".format(self.saved_nn_dir))
        else:
            try:
                os.mkdir(self.saved_nn_dir)
            except OSError:
                print("ERROR: Creation of directory \'{}\' failed".format(self.saved_nn_dir))
            else:
                print("INFO: Successfully created directory \'{}\'".format(self.saved_nn_dir))

        # find all files in saved_nn_dir and save it to models
        models = []
        model_extension = ".h5"
        for item in os.listdir(self.saved_nn_dir):
            # print(item)
            if os.path.isfile(os.path.join(self.saved_nn_dir, item)) and item[-3:] == model_extension:
                # cut the extension out
                models.append(item.replace(model_extension, ""))

        if name in models:

            # prepare two lists, one with descriptors, second one with vector q_i
            first_array, second_array = self.prepare_arrays(self.output_dir)
            if first_array is None or second_array is None:
                print("ERROR: The interrupting of the training NN!")
                return

            # prepare NN
            self.nn = NeuralNetwork(name)
            self.nn.load_model()

            # let the NN train
            self.nn.train(first_array, second_array)

            # at the end, save the model
            self.nn.save_model()

            print("here I am")

            # move all files from 'prepare_to_training' dir to 'trained' dir
            self.move_files_from_to(self.output_dir, self.trained_dir)

        else:
            # if 'name' is in 'saved_nn' directory, do nothing
            print("ERROR: Neural network \'{}\' does not exist!".format(name))

    # TODO: add more comments, documentary string and more prints
    def predict(self, name, filename):
        print("ACTION: predict\n"
              "predicting ...\n"
              "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

        # 1. prepare given file, i.e. make a file for each timestep and save it to 'prepared_for_predicting' directory
        # processing of file ...
        with open(filename, "r") as input_file:

            # main dictionary that stores individual timesteps (timestep: atoms)
            timesteps = {}

            # scanning booleans (starts and stops scanning parts of input file)
            scan_timestep = False
            scan_atoms = False
            scan_number_of_atoms = False

            # current timestep for accessing main dictionary
            current_timestep = None

            for raw_line in input_file:
                line = raw_line.strip()

                if line == "ITEM: TIMESTEP":
                    # scan for timestep in next line
                    scan_timestep = True
                    # stop scanning for atoms
                    scan_atoms = False

                elif scan_timestep:
                    # print("Timestamp:", repr(line))
                    timesteps[line] = {}
                    current_timestep = line
                    scan_timestep = False

                elif line == "ITEM: NUMBER OF ATOMS":
                    # scan for number of atoms in next line
                    scan_number_of_atoms = True

                elif scan_number_of_atoms:
                    # print("Number of atoms:", repr(line))
                    # number_of_atoms = int(line)
                    scan_number_of_atoms = False

                elif line == "ITEM: ATOMS id type xs ys zs":
                    timesteps[current_timestep] = {}
                    # scan for atoms in next lines
                    scan_atoms = True

                elif scan_atoms:
                    # print("Atom:", repr(line))
                    atom_id, atom_type, atom_x, atom_y, atom_z = line.strip().split()
                    timesteps[current_timestep][atom_id] = [float(atom_x), float(atom_y), float(atom_z), None]

                else:
                    # skipping useless lines
                    pass
        # all atoms are loaded in dictionary

        # calculating the values of 14 functions for each atoms
        for timestep in timesteps.keys():
            print("... processing timestep #", timestep)
            for id in timesteps[timestep].keys():
                # coordinates of current atom
                x = timesteps[timestep][id][0]
                y = timesteps[timestep][id][1]
                z = timesteps[timestep][id][2]
                print("... ... id: {}: [{}, {}, {}]".format(id, x, y, z))
                # calculate descriptors for current atom
                descriptors = Descriptors(id, x, y, z, timesteps[timestep]).get_descriptors()
                # add descriptors to the dictionary
                timesteps[timestep][id][3] = descriptors
                # print("Descriptors:", descriptors)

        # save dictionary to json file
        with open(self.tmp_dir + os.path.sep + "dict_timesteps.json", "w") as json_file:
            json.dump(timesteps, json_file)
            print("INFO: dictionary 'timesteps' was saved to: dict_timesteps.json")

        # print timesteps-dictionary
        # self.print_timesteps(timesteps)

        # save timesteps to separate files in 'prepared_for_predicting' to_predict_dir ---?
        # create to_predict_dir for saving timesteps (if it does not exist)
        if os.path.isdir(self.to_predict_dir):
            print("INFO: Directory {} already exists.".format(self.to_predict_dir))
        else:
            try:
                os.mkdir(self.to_predict_dir)
            except OSError:
                print("ERROR: Creation of the directory {} failed".format(self.to_predict_dir))
            else:
                print("INFO: Successfully created directory {}".format(self.to_predict_dir))

        # each timestep is saved to different file
        # filename = date_time_timestep, e.g. 2020_03_28_09_42_45_500.txt

        for timestep in timesteps.keys():
            # create specific filename
            filename = datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S_") + str(timestep) + ".txt"
            path_to_file = os.path.join(self.to_predict_dir, filename)
            print("... saving timestep #{} to file {}".format(timestep, path_to_file))

            # open file
            with open(path_to_file, 'w') as file:
                # print informative header
                file.write(Descriptors.info_header(timestep, phase=None))

                # print descriptors for each atom to file
                for id in timesteps[timestep].keys():
                    file.write(str(id) + ' ' + ' '.join(map(str, timesteps[timestep][id][3])) + '\n')

        # all files are prepared in 'prepared_for_predicting' folder
        print("INFO: all timesteps were saved in \'prepared_for_predicting\' folder")

        # 2. prepare arrays
        # load NN model with 'name'

        # check whether the name is in saved_nn directory
        # create saved_nn_dir for saving models of NN (if it does not exist)
        if os.path.isdir(self.saved_nn_dir):
            print("INFO: directory \'{}\' already exists.".format(self.saved_nn_dir))
        else:
            print("ERROR: directory \'{}\' does not exist!".format(self.saved_nn_dir))
            return None

        # find all files in saved_nn_dir and save it to models
        models = []
        model_extension = ".h5"
        for item in os.listdir(self.saved_nn_dir):
            # print(item)
            if os.path.isfile(os.path.join(self.saved_nn_dir, item)) and item[-3:] == model_extension:
                # cut the extension out
                models.append(item.replace(model_extension, ""))

        # we have existing NN
        if name in models:
            for root, directories, files in os.walk(self.to_predict_dir):
                for filename in sorted(files):

                    # prepare two lists, one with descriptors, second one with vector q_i
                    input_array, second_array = self.prepare_arrays(self.to_predict_dir, filename)
                    if input_array is None or second_array is not None:
                        print("ERROR: The interrupting of the predicting!")
                        return

                    # prepare NN, load model
                    self.nn = NeuralNetwork(name)
                    self.nn.load_model()

                    # let the NN predict something
                    # output is vector q for each atom in file at that timestep
                    #   i.e. a matrix [num_atoms, num_phases], type = numpy.ndarray
                    prediction = self.nn.predict(input_array)

                    # I have a prediction!
                    # TODO: do something with the prediction
                    # print("... prediction for file \'{}\'\n{}".format(filename, prediction))

                    # calculate vector_Q
                    vector_big_q = self.calculate_vector_big_q(prediction)

                    # I have vector Q that has information about global structure at given timestep
                    # TODO: do something with the vector Q
                    # print("Q = {}".format(vector_big_q))

                    # create dictionary [phase:percentage]
                    global_structure_dict = self.create_dict_phase_percentage(vector_big_q)

                    # print result (global structure info)
                    print("RESULT: global structure:\n{}".format(self.dict_to_string(global_structure_dict)))

            # move all files from 'prepare_to_predicting' dir to 'predicted' dir
            self.move_files_from_to(self.to_predict_dir, self.predicted_dir)
            print("INFO: End of predicting.")

        else:
            # if 'name' is in 'saved_nn' directory, do nothing
            print("ERROR: Neural network \'{}\' does not exist!".format(name))

    @staticmethod
    def print_timesteps(timesteps):
        """
        prints timesteps dictionary in well arranged way
        """
        print("Timesteps:")
        for timestep, atoms in timesteps.items():
            print("\tTimestep:", timestep)

            for atom, coords in atoms.items():
                print("\t\tAtom #{}:\t{}".format(atom, coords))

    @staticmethod
    def print_intro():
        """
        prints logo of KABUTO in nice way
        """
        print("******************************************************")
        print("                   ___            _______    ____")
        print("   | /     /\\     |   |   |    |     |      /    \\")
        print("   |<     /__\\    |--<    |    |     |     |      |")
        print("   | \\   /    \\   |___|    \\__/      |      \\____/")
        print("******************************************************")
        print("                   Ondrej Bily")
        print("                  Diploma Thesis")
        print("                       2020")
        print("******************************************************")
        print()

    @staticmethod
    def print_nn_models(models):
        to_print = ""
        for model in models:
            to_print += "... {}\n".format(model)
        print(to_print.strip())

    @staticmethod
    def move_files_from_to(from_dir, to_dir):
        """
        moves all files from 'from_dir' to 'to_dir'
        """
        print("INFO: Moving files ...")
        # create to_dir if it does not exist)
        if os.path.isdir(to_dir):
            print("INFO: {} already exists.".format(to_dir))
        else:
            try:
                os.mkdir(to_dir)
            except OSError:
                print("ERROR: Creation of the trained_dir {} failed".format(to_dir))

            else:
                print("INFO: Successfully created the trained_dir {}".format(to_dir))
        files = os.listdir(from_dir)
        for filename in files:
            shutil.move(os.path.join(from_dir, filename), to_dir)

        print("INFO: files from \'{}\' successfully moved to \'{}\'".format(from_dir, to_dir))

    def prepare_arrays(self, directory=None, filename=None):
        """
        prepares two arrays, input data, either from all files in 'directory' or from a file 'directory + filename'
        * first array contains arrays of descriptors
        * second layer contains arrays of 1 and 0s
            * position of 1 is determined by phase
            * call function create_output_vector(phase)
        """

        if filename is None and directory is not None:
            input_array, output_array = [], []
            print("INFO: Preparing arrays from directory: \'{}\'".format(directory))

            for root, directories, files in os.walk(directory):
                if not files:
                    print("ERROR: No files in \'{}\'".format(directory))
                    return None, None
                for filename in sorted(files):
                    # process each file
                    print("... processing file: {}".format(filename))
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
                                        print("ERROR: The interrupting of the preparing of arrays!")
                                        return None, None
                            else:
                                # processing a line with descriptors: [id, **descriptors]
                                items = line.split()
                                descriptors = list(map(float, items[1:]))
                                # print("{} : {}".format(id, descriptors))

                                # add output_vector to output array
                                output_array.append(output_vector)

                                # add descriptors to input array
                                input_array.append(descriptors)

            print("INFO: input and output arrays have the same length:", len(input_array) == len(output_array))
            print("... Descriptors:\n{}".format(np.array(input_array, dtype=float)))
            print("... Output vector:\n{}".format(np.array(output_array, dtype=float)))

            # return numpy array, tensorflow likes it
            return np.array(input_array, dtype=float), np.array(output_array, dtype=float)

        elif filename is not None and directory is not None:
            print("INFO: Preparing only input array from the file: \'{}\'".format(os.path.join(directory, filename)))

            input_array, output_array = [], None

            # processing a file
            try:
                with open(os.path.join(directory, filename)) as file:
                    for line in file:
                        if line[0] == '#':
                            # processing info header
                            pass
                        else:
                            # processing a line with descriptors: [id, **descriptors]
                            items = line.split()
                            descriptors = list(map(float, items[1:]))
                            # print("{} : {}".format(id, descriptors))

                            # add descriptors to input array
                            input_array.append(descriptors)

                # print("... Descriptors:\n{}".format(np.array(input_array, dtype=float)))

                # return numpy array, tensorflow likes it
                return np.array(input_array, dtype=float), None

            except FileNotFoundError:
                print("ERROR: File {} not found!".format(filename))
                return None, None

        else:
            print("ERROR: Wrong use of \'prepare_arrays()\' function!")
            return None, None

    def create_output_vector(self, phase):
        """
        creates an output vector for neural network
            > it is a array of 0s and 1
            > 1 is at the position of given phase
        """

        if phase not in self.phases_available.keys():
            print("ERROR: Given phase is not one of the available phases!")
            return None

        # create output vector
        vector_q = [0] * self.number_of_phases

        # change correct place in vector_q
        try:
            vector_q[self.phases_available[phase]] = 1
        except IndexError:
            print("ERROR: Problem with available_phases attribute in Kabuto class!")
            return None

        # print("vector_q: {}".format(vector_q))
        return vector_q

    def load_available_phases(self):
        """
        loads a list of available phases from a file self.phase_file into the dictionary
            > comments (lines beginning with '#') are allowed
            > new line, new phase
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
            print("ERROR: File \'{}\' not found!".format(self.phase_file))
            return None

        print(phases_dict)
        return phases_dict

    def test(self):
        """
        a method for the testing of the features
        """
        print("ACTION: test\n"
              "Entering TEST mode. Object KABUTO created. ...\n"
              "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

        # add tests of features here -->
        self.move_files_from_to(self.output_dir, self.trained_dir)

    # TODO: add documentary string and comments
    def calculate_vector_big_q(self, prediction):
        vector = [0] * self.number_of_phases
        n = len(prediction.tolist())

        for i, q_i in enumerate(prediction.tolist()):  # rows
            for j, q_ij in enumerate(q_i):  # columns
                vector[j] += q_ij
        return [q_i / n for q_i in vector]

    # TODO: add documentary string and comments
    def create_dict_phase_percentage(self, vector_big_q):
        result_dict = dict()
        for phase, index in self.phases_available.items():
            result_dict[phase] = vector_big_q[index]
        return result_dict

    @staticmethod
    def dict_to_string(dictionary):
        result = ''
        for key, value in dictionary.items():
            result += "--> {} : {}\n".format(key, value)
        return result.strip()


################################################################
# create Kabuto Machine iff there is correct number of arguments
################################################################
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
    # TODO: here could be the test whether all necessary packages are installed
    # script called without action
    print("******************************************************\n"
          "                   ___            _______    ____\n"
          "   | /     /\\     |   |   |    |     |      /    \\\n"
          "   |<     /__\\    |--<    |    |     |     |     |\n"
          "   | \\   /    \\   |___|    \\__/      |      \\____/\n"
          "******************************************************\n"
          "                   Ondrej Bily\n"
          "                  Diploma Thesis\n"
          "                       2020\n"
          "******************************************************\n"
          "Usage:\n"
          "    kabuto.py prepare <name_of_phase> <dump_file>\n"
          "    kabuto.py list_nn\n"
          "    kabuto.py create_nn <name_of_nn>\n"
          "    kabuto.py train <name_of_nn>\n"
          "    kabuto.py predict <name_of_nn> <dump.file>\n"
          "    kabuto.py test\n"
          "******************************************************\n")
