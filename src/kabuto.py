import json
import os
import sys
import datetime

from descriptors import Descriptors


class Kabuto:

    # constructor of class
    def __init__(self, action, option, phase):
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
            # if self.option in self.accepted_phases:
            if self.option is not None and self.phase is not None:
                self.prepare(self.phase, self.option)
            else:
                print("Either phase or file not given ...")

        elif self.action == "learn":
            if self.option is None:
                self.learn()
            else:
                print("Action learn does not need any option ...")

        elif self.action == "predict":
            if self.option is not None:
                self.predict(self.option)
            else:
                print("No file given ...")

        else:
            print("You entered wrong action:", self.action)
            print("Possible arguments:")
            print("    prepare <name_of_phase>")
            print("    learn")
            print("    predict <path_to_file_with_structure>")

    ##################################################################
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
                # print("\tid: {}: [{}, {}, {}]".format(id, x, y, z))
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

        # save timesteps to separate files in 'prepared_for_learning' directory ---?
        # create directory for saving timesteps (if it does not exist)
        directory = 'prepared_for_learning'
        if os.path.isdir(directory):
            print("INFO: directory {} already exists.".format(directory))
        else:
            try:
                os.mkdir(directory)
            except OSError:
                print("ERROR: Creation of the directory {} failed".format(directory))
            else:
                print("INFO: Successfully created the directory {}".format(directory))

        # each timestep is saved to different file
        # filename = date_time_timestep, e.g. 2020_03_28_09_42_45_500.txt

        for timestep in timesteps.keys():
            # create specific filename
            filename = datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S_") + str(timestep) + ".txt"
            path_to_file = os.path.join(directory, filename)
            print("... saving timestep #{} to file {}".format(timestep, path_to_file))

            # open file
            with open(path_to_file, 'w') as file:
                # print informative header
                info_header = "# timestep {}\n" \
                              "# phase {}\n" \
                              "# id f1 f2 f3 f4 f5 f6 f7 f8 f9 f10 f11 f12 f13 f14\n".format(timestep, phase)
                file.write(info_header)

                # print descriptors for each atom
                for id in timesteps[timestep].keys():
                    # prepare string to be written
                    descriptor_line = str(id) + ' ' + ' '.join(map(str, timesteps[timestep][id][3])) + '\n'
                    # write this line to file
                    file.write(descriptor_line)

        # all files are prepared in 'prepared_for_learning' folder
        print("INFO: all timesteps were saved in \'prepared_for_learning\' folder")

    def learn(self):
        info = "ACTION: learn\n" \
               "learning ...\n" \
               "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
        print(info)  # this must be here

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
if len(sys.argv) == 1:
    # script called without action
    print("******************************************************")
    print("   | /     /\\     |‾‾‾|   |    |  ‾‾‾|‾‾‾   /‾‾‾‾\\")
    print("   |<     /__\\    |--<    |    |     |     |      |")
    print("   | \\   /    \\   |___|    \\__/      |      \\____/")
    print("******************************************************")
    print("                   Ondrej Bily")
    print("                  Diploma Thesis")
    print("                       2020")
    print("******************************************************")
    print("Usage:")
    print("    kabuto.py prepare <name_of_phase> <dump_file>")
    print("    kabuto.py learn")
    print("    kabuto.py predict <path_to_file_with_structure>")
    print("******************************************************")
elif len(sys.argv) == 2:
    # script called with one argument (action)
    Kabuto(action=sys.argv[1], option=None, phase=None)
elif len(sys.argv) == 3:
    # script called with two argument (action, option)
    Kabuto(action=sys.argv[1], option=sys.argv[2], phase=None)
elif len(sys.argv) == 4:
    # script called with three arguments (action, phase, file)
    Kabuto(action=sys.argv[1], phase=sys.argv[2], option=sys.argv[3])
