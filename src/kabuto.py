import json
import os
import sys
import datetime

from modules.descriptors import Descriptors


class Kabuto:

    def __init__(self, action, option, phase):
        """
        constructor of Kabuto class
        """
        self.print_intro()

        # initialize attributes
        self.action = action
        self.option = option
        self.phase = phase
        self.output_dir = 'prepared_for_learning'
        self.tmp_dir = 'temporary'

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

        elif self.action == "learn":
            if self.option is not None and self.phase is None:
                self.learn(self.option)
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
                  "    learn <name_of_nn>\n"
                  "    predict <path_to_file_with_structure>\n".format(self.action))

    def prepare(self, phase, file):
        """
        Documentation for 'prepare' function:
            > prepares files for learning from dump-file
            > parses all atomic positions and calculates values of 14 functions for each atom
            > for each timestamp creates corresponding file in 'prepared_for_learning' folder
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
                descriptors = Descriptors(id, x, y, z, timesteps[timestep]).values_of_14_functions()
                # add descriptors to the dictionary
                timesteps[timestep][id][3] = descriptors
                # print("Descriptors:", descriptors)

        # save dictionary to json file
        with open(self.tmp_dir + os.path.sep + "dict_timesteps.json", "w") as json_file:
            json.dump(timesteps, json_file)
            print("INFO: dictionary 'timesteps' was saved to: dict_timesteps.json")

        # print timesteps-dictionary
        # self.print_timesteps(timesteps)

        # save timesteps to separate files in 'prepared_for_learning' output_dir ---?
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

        # all files are prepared in 'prepared_for_learning' folder
        print("INFO: all timesteps were saved in \'prepared_for_learning\' folder")

    def list_nn(self):
        """
        Documentation for 'list_nn' function:
            > ...
            > ...
            > usage:
                list_nn()
        """
        info = "ACTION: list_nn\n" \
               "listing all saved neural networks ...\n" \
               "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
        print(info)  # this must be here

    def create_nn(self, name):
        """
        Documentation for 'create_nn' function:
            > ...
            > ...
            > usage:
                create_nn(name)
        """
        info = "ACTION: create_nn\n" \
               "creating neural network \'{}\' ...\n" \
               "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^".format(name)
        print(info)  # this must be here

    def learn(self, name):
        """
        Documentation for 'learn' function:
            > ...
            > ...
            > usage:
                learn(name)
        """
        info = "ACTION: learn\n" \
               "\'{}\' is learning from \'prepared_for_learning\' directory\n" \
               "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^".format(name)
        print(info)  # this must be here

        # prepare two lists, one with descriptors, second one with vector q_i

        # prepare NN

        # let the NN learn

        # at the end, save the model

        # move learned files to another directory

    def predict(self, option):
        info = "ACTION: predict\n" \
               "predicting ...\n" \
               "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
        print(info)  # this must be here

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
          "    kabuto.py learn <name_of_nn>\n"
          "    kabuto.py predict <path_to_file_with_structure>\n"
          "******************************************************\n")
