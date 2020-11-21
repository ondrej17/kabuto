# KABUTO

## Announcements
*Predicting method will be extended (or another method will be added). We want Kabuto to be able to identify structure in real time - during simulation - and simultaneously provide the input for PLUMED plugin and LAMMPS simulation.*

## About
Developed by **Ondrej Bily**, Faculty of Mathematics, Physics and Informatics, Comenius University in Bratislava, Slovakia. 

It is an implementation of `tensorflow`'s `keras` neural network in `Python` for Diploma thesis in Condensed Matter Physics. The neural network (NN) is used to identify the structural phases during structural phase transitions in crystalline systems. 

## Features

### Preparing
Prepares a file containing descriptors of each atom for each timestep of simulation. Dump file must be an output of the `LAMMPS` simulation. Input file for simulation must contain `dump` command in the format:

    dump 1 all custom 50 atoms.out id type x y z
    
Output files (from which neural network will be taught) are stored in `dir_to_train` directory.

### Listing neural networks
Lists all available models that are stored in `saved_nn` directory. These models are `tensorflow.keral.model` objects that contain information about neural network. 

### Creating a neural network
Creates a new neural network and stores its model in `saved_nn` directory.

### Training
Trains everything from files in `dir_to_train` directory.

### Predicting
Predicts the percentage of each phase that neural network knows. Determines global structure in given dump file for each timestep.

## Usage
Compile C++ extension `descriptors` in `src/modules/descriptors` folder:
    
    (sudo) ./install.sh

In `src` folder:

    python kabuto.py prepare <name_of_phase> <dump.file>
    
    python kabuto.py list_nn
    
    python kabuto.py create_nn <name_of_nn>
    
    python kabuto.py train <name_of_nn>
    
    python kabuto.py predict <name_of_nn> <dump.file>
    
Phases that we want to be learned must be in file `src/config/phases_to_learn.txt`.

The results of the script are stored in `src/result` folder.

The log of script is both printed to console and written in file `src/kabuto.log`. 

The example run and simulation are located in `example` folder.
  
 ## Code Structure
 * `README.md`
 * `src`
     * `modules`
         * `descriptors`
            * `tests`
                * `...`
            * `src`
                * `descriptors_atom.cpp`
                * `descriptors_atom.h`
                * `descriptors_box.cpp`
                * `descriptors_box.h`
                * `descriptors_descriptors.cpp`
                * `descriptors_descriptors.h`
                * `descriptors_module.cpp`
                * `descriptors_module.h`
                * `descriptors_timestep.cpp`
                * `descriptors_timestep.h`
                * `descriptors_utility.cpp`
                * `descriptors_utility.h`
                * `descriptors_verlet_list.cpp`
                * `descriptors_verlet_list.h`
            * `CMakeLists.txt`
            * `setup.py`
         * ~~`descriptors.py`~~
         * `neural_network.py`
     * `config`
         * `dict_timesteps.json`
         * `dict_pbc.json`
         * `logger.ini`
         * `phases_to_learn.txt`
     * `saved_nn`
         * `nn1.h5`
         * `...`
     * `dir_to_train`
         * `to_train1.txt`
         * `...`
     * `dir_to_predict`
         * `to_predict1.txt`
         * `...`
     * `dir_trained`
         * `trained1.txt`
         * `...`
     * `dir_predicted`
         * `predicted1.txt`
         * `...`
     * `results`
         * `...`
     * `kabuto.py`
     * `kabuto.log`
 * `example`
    * `molybden_bcc`
        * `...`
    * `molybden_fcc`
        * `...`
    * `small_example_dump.file`
 * `scripts`
    * `...`
     
 ## Design of the NNs
* input layer
	* 14 input nodes
	* correspond to 14 functions that we use as descriptors
		* 11 symmetry functions
		* 3 Steinhardt parameters
* hidden layers
	* first hidden layer
		* 25 nodes
	* second hidden layer
		* 25 nodes
* output layer
	* N output nodes
		* N is number of phases we want to identify
  
## Requirements
* `Python`
* `tensorflow`, `scipy` and `numpy` packages
* `boost` library
* `cmake`
* compiled `descriptors` C++ extension 