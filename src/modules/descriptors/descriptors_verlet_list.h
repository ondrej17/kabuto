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
    std::vector<int> m_ids;

public:
    // constructor
    VerletList(int id) : m_id{id} {}

    // getters
    inline int getId() { return m_id; };
    inline std::vector<int> getIds() { return m_ids; };

    // methods
    void pushBack(int atomId);
};

#endif //DESCRIPTORS_VERLETLIST_H
