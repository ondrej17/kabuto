#ifndef KABUTO_TIMESTEP_H
#define KABUTO_TIMESTEP_H

#include <vector>
#include <utility>

#include "Atom.h"

class Box;

class Timestep {
private:
    int m_id;
    std::vector <std::pair<int, Atom>> m_atoms;
    Box &m_masterBox;   // holds reference to Box object that contains this Timestep object

public:
    // constructor
    Timestep(int id, Box &masterBox)
            : m_id{id}, m_masterBox{masterBox} {}

    // getters
    inline int getId() { return m_id; };

    inline std::vector <std::pair<int, Atom>> getAtoms() { return m_atoms; };

    inline Box &getMasterBox() { return m_masterBox; };

    // methods
    void calculateDescriptors();

    void createVerletLists();
};


#endif //KABUTO_TIMESTEP_H
