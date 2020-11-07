/**
 * 
 * 
 * 
 * 
 * 
 * 
 * 
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
};
#endif //DESCRIPTORS_VERLETLIST_H
