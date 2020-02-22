import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import time
import sys


class Kabuto:

    # constructor of class
    def __init__(self, action, option):
        print("Kabuto was born.")

        # initialize attributes
        self.action = action
        self.option = option

        # based on option, call correct method
        if self.action == "prepare":
            if self.option is not None:
                self.prepare(self.option)

        elif self.action == "learn":
            if self.option is None:
                self.learn()

        elif self.action == "predict":
            if self.option is not None:
                self.predict(self.option)

        else:
            print("You entered wrong action:", self.action)
            print("Possible arguments:")
            print("    prepare <name_of_phase>")
            print("    learn")
            print("    predict <path_to_file_with_structure>")

    def prepare(self, option):
        print("ACTION: prepare")

        print("preparing:", option)

    def learn(self):
        print("ACTION: learn")

        print("learning ...")

    def predict(self, option):
        print("ACTION: predict")

        print("predicting:", option)


################################################################
# create Kabuto Machine iff there is correct number of arguments
################################################################
if len(sys.argv) == 1:
    # script called without action
    print("--------------")
    print("Kabuto Machine")
    print("--------------")
    print("Possible arguments:")
    print("    prepare <name_of_phase>")
    print("    learn")
    print("    predict <path_to_file_with_structure>")
elif len(sys.argv) == 2:
    # script called with one argument (action)
    Kabuto(action=sys.argv[1], option=None)
elif len(sys.argv) == 3:
    # script called with two argument (action, option)
    Kabuto(action=sys.argv[1], option=sys.argv[2])
