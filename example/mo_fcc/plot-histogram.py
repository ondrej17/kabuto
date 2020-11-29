##
#   Name: plot-historgam
#   Author: Ondrej Bily
#   Description: Calculates and saves histograms of descriptors values for given 
#                phase and folder that contains files with descriptors values.
#                The histograms  are saved in `plots` folder
#   Usage: python plot-historgam.py <folder-with-files> <phase>
##


import numpy as np
import matplotlib.pyplot as plt
import os
import sys


if len(sys.argv) == 3:
    pathToValues = sys.argv[1]
    phase = sys.argv[2]
else:
    print("INFO: Usage: python plot-historgam.py <folder-with-files> <phase>")
    print("ERROR: Wrong usage of this script.")
    sys.exit()


def plotDescriptorsFirstAtom(nbins, phase):
    """
    Plot histograms of descriptors for atom #1
    """
    for index, name in descriptorsNames.items():
        print("INFO: Plotting {} of atom #1".format(name))

        # the histogram of the data
        data = np.array(allDescriptors[index][1], dtype=float)

        plt.hist(data, nbins,
                 density=True,
                 color='green')

        # add value of perfect structure
        plt.axvline(perfectValues[phase][index],
                    color='k',
                    linestyle='dashed',
                    linewidth=1)

        plt.xlabel(name)
        plt.ylabel("Probability")
        plt.title("{} for Mo-{}".format(name, phase))
        plt.grid(True)
        plt.savefig("plots/histogram-f{}.png".format(index+1), format="png")
        plt.clf()


def plotDescriptorsAllAtom(nbins, phase):
    """
    Plots histograms of descriptors for all atom
    """
    for index, name in descriptorsNames.items():
        print("INFO: Plotting {} of all atom".format(name))

        # the histogram of the data
        data = []
        for values in allDescriptors[index].values():
            for value in values:
                data.append(value)

        data = np.array(data, dtype=float)

        plt.hist(data, nbins,
                 density=True,
                 color='green')

        # add value of perfect structure
        plt.axvline(perfectValues[phase][index],
                    color='k',
                    linestyle='dashed',
                    linewidth=1)

        plt.xlabel(name)
        plt.ylabel("Probability")
        plt.title("{} for Mo-{}".format(name, phase))
        plt.grid(True)
        plt.savefig("plots/histogram-f{}.png".format(index+1), format="png")
        plt.clf()


# dictionary that holds name of each descriptor
descriptorsNames = {
    0: "G2(Rs=2.8, eta=20.0)",
    1: "G2(Rs=3.2, eta=20.0)",
    2: "G2(Rs=4.4, eta=20.0)",
    3: "G2(Rs=4.8, eta=20.0)",
    4: "G2(Rs=5.0, eta=20.0)",
    5: "G2(Rs=5.3, eta=20.0)",
    6: "G2(Rs=5.7, eta=20.0)",
    7: "G2(Rs=6.0, eta=20.0)",
    8: "G3(kappa=3.5)",
    9: "G3(kappa=4.5)",
    10: "G3(kappa=7.0)",
    11: "SteinParam(l=6)",
    12: "SteinParam(l=7)",
    13: "SteinParam(l=8)"
}

# dictionary that holds the "initial" values of descriptors for perfect structures
perfectValues = {
    "bcc": [7.73, 5.80, 11.30, 1.77, 8.96, 26.29, 2.70, 0.51,
            5.35, 14.22, 33.66,
            0.51, 1.08e-05, 0.43],
    "fcc": [9.31, 2.30, 1.25, 7.22, 23.05, 6.59, 8.76, 6.53,
            -1.03, 3.45, -34.12,
            0.57, 3.57e-06, 0.40]
}

# dictionary that holds values of all descriptors for all atoms
allDescriptors = [dict() for i in range(14)]

# process each files in 'pathToValues' folder
for filename in os.listdir(pathToValues):
    fullFilename = os.path.join(pathToValues, filename)

    if os.path.isfile(fullFilename):
        with open(fullFilename, 'r') as file:
            print("INFO: Loading from file: {}".format(fullFilename))

            lines = [line.rstrip() for line in file]

            # process each line
            for line in lines:
                if line[0] == '#':
                    continue # comment line
                else:
                    # 15 parts: id + 14 values
                    partsOfLine = line.split()  
                    atomId = int(partsOfLine[0])
                    descriptors = partsOfLine[1:]
                    for cnt, value in enumerate(descriptors):
                        try:
                            allDescriptors[cnt][atomId].append(value)
                        except KeyError:
                            allDescriptors[cnt][atomId] = [value]

nbins = 100
plotDescriptorsAllAtom(nbins, phase)
