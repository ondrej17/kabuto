/**
 * Name: 
 *      descriptors_verlet_list.h
 * Author: 
 *      Ondrej Bily
 * Description: 
 *      Header file corresponding to class VerletList. Box object 
 *      creates VerletList for each atom. VerletList contains IDs 
 *      of atoms that are in cutoff sphere of given atom.
 */

#ifndef DESCRIPTORS_VERLETLIST_H
#define DESCRIPTORS_VERLETLIST_H

#include <vector>

class VerletList
{
private:
    int m_id;
    std::vector<int> m_atomIds;

public:
    // constructor
    VerletList(int id, std::vector<int> atomIds) : m_id{id}, m_atomIds{atomIds} {}

    // getters
    inline int getId() { return m_id; };
    inline std::vector<int> getAtomIds() { return m_atomIds; };
    inline int getNumOfAtoms() {return m_atomIds.size();};
};
#endif //DESCRIPTORS_VERLETLIST_H
