/**
 * Name: 
 *      descriptors_timestep.h
 * Author: 
 *      Ondrej Bily
 * Description: 
 *      Header file corresponding to class Timestep. Object Timestep 
 *      is created in Box class for each loaded timestep. Timestep holds
 *      all atoms and theirs IDs. 
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
    int m_id;                       // ID of timestep
    int m_numOfAtoms;               // number of atoms in this timestep
    std::map<int, Atom> m_atoms;    // map of atoms objects in this timestep
    std::vector<int> m_atomsId;     // IDs of atoms in this timestep

public:
    // constructor
    Timestep(int id) : m_id{id}
    {
        m_numOfAtoms = 0;           // no atoms in the beginning
    }

    // getters
    inline int getId() { return m_id; };
    inline int getNumOfAtoms() { return m_numOfAtoms; };
    inline std::map<int, Atom> &getAtoms() { return m_atoms; };
    inline std::vector<int> &getAtomsId() { return m_atomsId; };

    // methods
    void addAtom(int atomId, double x, double y, double z);
    //void setAtomDescriptors(int atom_id, std::vector<double> descriptors);
    Atom &getAtom(int id);
    const std::vector<double> &getAtomDescriptors(int atom_id);
    
};

#endif //DESCRIPTORS_TIMESTEP_H
