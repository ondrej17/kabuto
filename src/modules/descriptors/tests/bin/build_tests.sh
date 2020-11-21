#!/bin/bash
echo "Building tests for \"descriptors\" library"

echo "Building tests for Atom class ..."
g++ -std=c++11 ../test_atom.cpp -I/usr/local/include -L/usr/local/lib -lboost_unit_test_framework -static -o test_atom
#echo "Building tests for Timestep class ..."
#g++ -std=c++11 ../test_timestep.cpp -I/usr/local/include -L/usr/local/lib -lboost_unit_test_framework -static -o test_timestep

echo "Done!"