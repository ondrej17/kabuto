import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# this script is called with the relative path to folder containing
#   files with values, and phase
try:
    # path to the folder with files
    pathToValues = sys.argv[1]
except IndexError:
    print("ERROR: Path to folder with files with descriptors not given.")
    sys.exit()

try:
    # phase
    phase = sys.argv[2]
except IndexError:
    print("ERROR: Phase not given.")
    sys.exit()


def plotDescriptorsFirstAtom(nbins, phase):
    # plot descriptors for atom #1
    for index, name in descriptorsNames.items():
        print("INFO: Plotting {} of atom #1".format(name))

        # the histogram of the data
        x = np.array(allDescriptors[index][1], dtype=float)

        n, bins, patches = plt.hist(x, nbins,
                                    density=True,
                                    color='green')

        # add value of perfect structure
        plt.axvline(perfectValues[phase][index],
                    color='k', 
                    linestyle='dashed', 
                    linewidth=1)

        plt.xlabel(name)
        plt.ylabel("Probability")
        plt.title("Histogram of {} for Mo-{}".format(name, phase))
        plt.grid(True)
        plt.savefig("plots/histogram-f{}.png".format(index+1), format="png")
        plt.clf()


def plotDescriptorsAllAtom(nbins, phase):
    # plot descriptors for all atom
    for index, name in descriptorsNames.items():
        print("INFO: Plotting {} of all atom".format(name))

        # the histogram of the data
        x = []
        for atomId, values in allDescriptors[index].items():
            for value in values:
                x.append(value)

        x = np.array(x, dtype=float)

        n, bins, patches = plt.hist(x, nbins,
                                    density=True,
                                    color='green')
        
        # add value of perfect structure
        plt.axvline(perfectValues[phase][index],
                    color='k', 
                    linestyle='dashed', 
                    linewidth=1)
        
        plt.xlabel(name)
        plt.ylabel("Probability")
        plt.title("Histogram of {} for Mo-{}".format(name, phase))
        plt.grid(True)
        plt.savefig("plots/histogram-f{}.png".format(index+1), format="png")
        plt.clf()


# dictionary that holds all value of all descriptors of first atom
descriptorsNames = {
    0: "G2(R_s=2.8, eta=20.0)",
    1: "G2(R_s=3.2, eta=20.0)",
    2: "G2(R_s=4.4, eta=20.0)",
    3: "G2(R_s=4.8, eta=20.0)",
    4: "G2(R_s=5.0, eta=20.0)",
    5: "G2(R_s=5.3, eta=20.0)",
    6: "G2(R_s=5.7, eta=20.0)",
    7: "G2(R_s=6.0, eta=20.0)",
    8: "G3(kappa=3.5)",
    9: "G3(kappa=4.5)",
    10: "G3(kappa=7.0)",
    11: "SteinParam(l=6)",
    12: "SteinParam(l=7)",
    13: "SteinParam(l=8)"
}

perfectValues = {
    "bcc": [7.73, 5.80, 11.30, 1.77, 8.96, 26.29, 2.70, 0.51,
            5.35, 14.22, 33.66,
            0.51, 1.08e-05, 0.43],
    "fcc": [9.31, 2.30, 1.25, 7.22, 23.05, 6.59, 8.76, 6.53,
            -1.03, 3.45, -34.12,
            0.57, 3.57e-06, 0.40]
}

allDescriptors = []     # list of dictionaries
for i in range(14):
    allDescriptors.append(dict())

# path to the folder with files
pathToValues = sys.argv[1]

# go through all files in 'pathToValues'
for filename in os.listdir(pathToValues):
    if os.path.isfile(os.path.join(pathToValues, filename)):
        # I have a filename, open it and load lines
        lines = []
        with open(os.path.join(pathToValues, filename), 'r') as file:
            print("INFO: Loading from file: {}".format(
                os.path.join(pathToValues, filename)))

            # load all lines
            lines = [line.rstrip() for line in file]

            # process each line
            for line in lines:
                # print("\tINFO: Processing line: {}".format(line))
                if line[0] == '#':
                    continue                    # comment line
                else:
                    partsOfLine = line.split()  # 15 parts: id + 14 values
                    atomId = int(partsOfLine[0])
                    descriptors = partsOfLine[1:]
                    for cnt, value in enumerate(descriptors):
                        try:
                            allDescriptors[cnt][atomId].append(value)
                        except KeyError:
                            allDescriptors[cnt][atomId] = [value]

nbins = 100
#plotDescriptorsFirstAtom(nbins, phase)
plotDescriptorsAllAtom(nbins, phase)
