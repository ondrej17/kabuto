# KABUTO
## About
Developed by **Ondrej Bily**, Faculty of Mathematics, Physics and Informatics, Comenius University in Bratislava, Slovakia. 

It is an implementation of `tensorflow` neural network in `Python` for Diploma thesis in Condensed Matter Physics.

## Code Structure
* README.md
* src
    * modules
        * descriptors.py
        * neural_network.py
    * saved_nn
        * nn1.h5
        * ...
    * prepared_for_learning
        * to_learn1.txt
        * ...
    * kabuto.py

## Features

### Preparing
Prepares a file containing descriptors of each atom for each timestep of simulation. Dump file must be an output of the `LAMMPS` simulation. Input file for simulation must contain `dump` command in format:

    dump myDump all atom 100 dump.atom
    
Output files (from which neural network will be taught) are stored in `prepared_for_learning` directory.

### Listing neural networks
List all available models that are stored in `saved_nn` directory. These models are `tensorflow.keral.model` objects that contains information about neural network. 

### Creating neural network
Creates a new neural network and stores its model in `saved_nn` directory.

### Learning
Learns everything from files in `prepared_for_learning` directory. 

### Predicting
Predicts the percentage of each phase that neural network knows. 

## Usage
In `src` folder:

    python kabuto.py prepare <name_of_phase> <dump.file>
    
    python kabuto.py list_nn
    
    python kabuto.py create_nn <name_of_nn>
    
    python kabuto.py learn <name_of_nn>
    
    python kabuto.py predict <dump.file>
    
## Requirements
* `Python3.6`
* `tensorflow`, `matplotlib` and `numpy` packages