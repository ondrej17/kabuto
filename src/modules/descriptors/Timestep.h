#ifndef DESCRIPTORS_TIMESTEP_H
#define DESCRIPTORS_TIMESTEP_H

#include <vector>
#include <utility>

#include "Atom.h"

class Timestep
{
private:
    int m_id;
    std::map<int, Atom> m_atoms;

public:
    // constructor
    Timestep(int id) : m_id{id} {}

    // getters
    inline int getId() { return m_id; };

    inline std::map<int, Atom> getAtoms() { return m_atoms; };

    // methods
    void calculateDescriptors();

    void createVerletLists();

    void addAtom(int id, double x, double y, double z);

    int getNumberOfAtom();

    int getAtomId(int jthAtom);

    std::vector<double> getAtomDescriptors(int jthAtom);

    std::map<int, Atom> getAllAtoms();
};

#endif //DESCRIPTORS_TIMESTEP_H
