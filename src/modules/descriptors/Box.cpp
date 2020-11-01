//
// Created by ondrej on 1. 11. 2020.
//

#include "Box.h"


void Box::calculateDescriptors() {
    int numOfTimesteps{getNumberOfTimesteps()};
    int numOfAtoms{getNumberOfAtom()};

    for (int i{0}; i < numOfTimesteps; i++) {
        for (int j{0}; j < numOfAtoms; j++) {
            m_atoms[j].calculateDescriptors(i);
        }
    }
}

void Box::addTimestepId(int id) {
    m_timestepsId.push_back(id);
}

void Box::addAtom(int id, double x, double y, double z) {
    m_atoms.push_back(Atom(id, x, y, z));
}

int Box::getNumberOfTimesteps() {
    return m_timestepsId.size();
}

int Box::getNumberOfAtom() {
    return m_atoms.size();
}

int Box::getTimestepId(int ithTimestep) {
    return m_timestepsId[ithTimestep];
}

std::vector<double> Box::getAtomDescriptors(int ithAtom, int jthTimestep) {
    return m_atoms[i].getDescriptors(jthTimestep);
}

int Box::getAtomId(int ithAtom) {
    return m_atoms[ithAtom].getId();
}