import json
import os
import sys
import datetime

from modules.descriptors import Descriptors
from modules.neural_network import NeuralNetwork


class Kabuto:

    def __init__(self, action, option, phase):
        """
        constructor of Kabuto class
        """
        self.print_intro()

        # initialize attributes
        self.nn = None
        self.action = action
        self.option = option
        self.phase = phase
        self.output_dir = 'prepared_for_training'
        self.tmp_dir = 'temporary'
        self.saved_nn_dir = 'saved_nn'
        self.trained_dir = 'trained'

        # based on option, call correct method
        if self.action == "prepare":
            # in future add a list of accepted phases
            if self.option is not None and self.phase is not None:
                self.prepare(self.phase, self.option)
            else:
                print("ERROR: Either phase or file not given")

        elif self.action == "list_nn":
            if self.option is None and self.phase is None:
                self.list_nn()
            else:
                print("ERROR: action \'list_nn\' takes no arguments")

        elif self.action == "create_nn":
            if self.option is not None and self.phase is None:
                self.create_nn(self.option)
            else:
                print("ERROR: either no name of neural network given or more arguments given")

        elif self.action == "train":
            if self.option is not None and self.phase is None:
                self.train(self.option)
            else:
                print("ERROR: either no name of neural network given or more arguments given")

        elif self.action == "predict":
            if self.option is not None and self.phase is None:
                self.predict(self.option)
            else:
                print("ERROR: either no file given or more arguments given")

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
        info = "ACTION: prepare\n" \
               "preparing phase: {}\n" \
               "preparing from file: {}\n" \
               "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^".format(phase, file)
        print(info)  # this must be here

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
        info = "ACTION: list_nn\n" \
               "listing all saved neural networks ...\n" \
               "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
        print(info)  # this must be here

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
        info = "ACTION: create_nn\n" \
               "creating neural network \'{}\' ...\n" \
               "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^".format(name)
        print(info)  # this must be here

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
            NeuralNetwork(name).create_model().save_model()

    def train(self, name):
        """
        Documentation for 'train' function:
            > ...
            > ...
            > usage:
                train(name)
        """
        info = "ACTION: train\n" \
               "\'{}\' is training from \'prepared_for_training\' directory\n" \
               "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^".format(name)
        print(info)  # this must be here

        # prepare two lists, one with descriptors, second one with vector q_i
        first_array, second_array = self.prepare_input_arrays(name)

        # prepare NN
        self.nn = NeuralNetwork(name).load_model()

        # let the NN train
        self.nn.train(first_array, second_array)

        # at the end, save the model
        self.nn.save_model()

        # create output_dir for saving timesteps (if it does not exist)
        if os.path.isdir(self.trained_dir):
            print("INFO: trained_dir {} already exists.".format(self.trained_dir))
        else:
            try:
                os.mkdir(self.output_dir)
            except OSError:
                print("ERROR: Creation of the trained_dir {} failed".format(self.trained_dir))
            else:
                print("INFO: Successfully created the trained_dir {}".format(self.trained_dir))

        # move all files from 'prepare_to_training' dir to 'trained' dir
        self.move_files_from_to(self.output_dir, self.trained_dir)

    def predict(self, option):
        info = "ACTION: predict\n" \
               "predicting ...\n" \
               "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
        print(info)  # this must be here

        # similar to 'train' function
        # prediction = model.predict([array of descriptors])

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
        print("   | /     /\\     |‾‾‾|   |    |  ‾‾‾|‾‾‾   /‾‾‾‾\\")
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
        # TODO: make this function
        pass

    def prepare_input_arrays(self, name):
        """
        prepares two arrays, input data, from all files in 'prepared_for_training' directory
        """
        # TODO: make this function using numpy
        return [], []


################################################################
# create Kabuto Machine iff there is correct number of arguments
################################################################
if len(sys.argv) == 2:
    # script called with one argument (action)
    Kabuto(action=sys.argv[1], option=None, phase=None)
elif len(sys.argv) == 3:
    # script called with two arguments (action, option)
    Kabuto(action=sys.argv[1], option=sys.argv[2], phase=None)
elif len(sys.argv) == 4:
    # script called with three arguments (action, phase, file)
    Kabuto(action=sys.argv[1], phase=sys.argv[2], option=sys.argv[3])
else:
    # script called without action
    print("******************************************************\n"
          "   | /     /\\     |‾‾‾|   |    |  ‾‾‾|‾‾‾   /‾‾‾‾\\\n"
          "   |<     /__\\    |--<    |    |     |     |      |\n"
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
          "    kabuto.py predict <dump.file>\n"
          "******************************************************\n")
