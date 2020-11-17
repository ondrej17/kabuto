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
    int m_numOfAtoms;
    std::map<int, Atom> m_atoms;
    std::vector<int> m_atomsId;

public:
    // constructor
    Timestep(int id) : m_id{id}
    {
        m_numOfAtoms = 0;
    }

    // getters
    inline int getId() { return m_id; };
    inline int getNumOfAtoms() { return m_numOfAtoms; };
    inline std::map<int, Atom> &getAtoms() { return m_atoms; };
    inline std::vector<int> &getAtomsId() { return m_atomsId; };

    // methods
    void addAtom(int atomId, double x, double y, double z);
    Atom &getAtom(int id);
    const std::vector<double> &getAtomDescriptors(int atom_id);
    void setAtomDescriptors(int atom_id, std::vector<double> descriptors);
};

#endif //DESCRIPTORS_TIMESTEP_H
