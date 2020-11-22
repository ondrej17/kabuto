#!/bin/bash

echo "Moving trained files back ..."
mv ../src/dir_trained/* ../src/dir_to_train/ 

echo "Removing saved NN ..."
rm ../src/saved_nn/nn1.h5

echo "Creating NN model ..."
python ../src/kabuto.py create_nn nn1

echo "Run traininf of NN ..."
python ../src/kabuto.py train nn1
