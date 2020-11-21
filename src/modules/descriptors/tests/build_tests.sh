#!/bin/bash
echo "Building tests for \"descriptors\" library"

# compiling all files
g++ -c -Wall ../src/descriptors_atom.cpp            -o build/descriptors_atom.o
g++ -c -Wall ../src/descriptors_descriptors.cpp     -o build/descriptors_descriptors.o
g++ -c -Wall src/test_atom.cpp                      -o build/test_atom.o
g++ -c -Wall src/test_descriptors.cpp               -o build/test_descriptors.o

# linking tests
g++ build/test_atom.o                   \
    build/descriptors_atom.o            \
    -I/usr/local/include                \
    -L/usr/local/lib                    \
    -lboost_unit_test_framework         \
    -static                             \
    -o bin/test_atom                    \

g++ build/test_descriptors.o            \
    build/descriptors_atom.o            \
    build/descriptors_descriptors.o     \
    -I/usr/local/include                \
    -L/usr/local/lib                    \
    -lboost_unit_test_framework         \
    -static                             \
    -o bin/test_descriptors             \

echo "Done!"