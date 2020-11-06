/**
 * 
 * 
 * 
 * 
 * 
 * 
 * 
 */

#ifndef DESCRIPTORS_TIMESTEP_H
#define DESCRIPTORS_TIMESTEP_H

#include <vector>
#include <map>
#include <utility>

#include "descriptors_atom.h"

class Timestep
{
private:
    int m_id;
    std::map<int, Atom> m_atoms;
    // add other attributes

public:
    // constructor
    Timestep(int id) : m_id{id} {}

    // getters
    inline int getId() { return m_id; };

    inline std::map<int, Atom> getAtoms() { return m_atoms; };

    // setters
};

#endif //DESCRIPTORS_TIMESTEP_H
