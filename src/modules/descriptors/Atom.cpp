//
// Created by ondrej on 1. 11. 2020.
//

#include "Atom.h"


std::vector<double> Atom::getDescriptors(int jthTimestep) {
    return m_descriptors[jthTimestep];
}


void Atom::calculateDescriptors(int jthTimestep) {
    // TODO: correctly write this function. Use the descriptors_func_module.cpp/.h files(s).
}