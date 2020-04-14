# KABUTO
## About
Developed by **Ondrej Bily**, Faculty of Mathematics, Physics and Informatics, Comenius University in Bratislava, Slovakia. 

It is an implementation of `tensorflow`'s `keras` neural network in `Python` for Diploma thesis in Condensed Matter Physics. The neural network (NN) is used to identify the structural phases during structural phase transitions in crystalline systems. 

## Features

### Preparing
Prepares a file containing descriptors of each atom for each timestep of simulation. Dump file must be an output of the `LAMMPS` simulation. Input file for simulation must contain `dump` command in format:

    dump myDump all atom 100 dump.atom
    
Output files (from which neural network will be taught) are stored in `dir_to_train` directory.

### Listing neural networks
List all available models that are stored in `saved_nn` directory. These models are `tensorflow.keral.model` objects that contains information about neural network. 

### Creating neural network
Creates a new neural network and stores its model in `saved_nn` directory.

### Training
Trains everything from files in `dir_to_train` directory.

### Predicting
Predicts the percentage of each phase that neural network knows. Determines global structure in given dump file for each timestep. 

## Usage
In `src` folder:

    python kabuto.py prepare <name_of_phase> <dump.file>
    
    python kabuto.py list_nn
    
    python kabuto.py create_nn <name_of_nn>
    
    python kabuto.py train <name_of_nn>
    
    python kabuto.py predict <name_of_nn> <dump.file>
  
 ## Code Structure
 * README.md
 * src
     * modules
         * descriptors.py
         * neural_network.py
         * phases_to_learn.txt
     * saved_nn
         * nn1.h5
         * ...
     * dir_to_train
         * to_train1.txt
         * ...
     * dir_to_predict
         * to_predict1.txt
         * ...
     * dir_trained
         * trained1.txt
         * ...
     * dir_predicted
         * predicted1.txt
         * ...
     * temporary
         * dict_timesteps.json
     * results
         * ...
     * kabuto.py
  
## Requirements
* `Python3.6`
* `tensorflow`, `scipy` and `numpy` packages