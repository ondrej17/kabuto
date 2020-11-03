#ifndef KABUTO_VERLETLIST_H
#define KABUTO_VERLETLIST_H

#include <vector>

class VerletList {
private:
    int m_id;
    std::vector<int> m_ids;

public:
    // constructor
    VerletList(int id) : m_id{id} {}

    // getters
    inline int getId() { return m_id; };
    inline std::vector<int> getIds() {return m_ids;};

    // methods
};


#endif //KABUTO_VERLETLIST_H
