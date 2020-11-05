#ifndef DESCRIPTORS_ATOM_H
#define DESCRIPTORS_ATOM_H

#include <vector>
#include "Box.h"

#define DUMMY_DOUBLE 3.14

class Atom: protected Box {
private:
    int m_id;
    int m_idOfMasterTimestep;
    double m_x;
    double m_y;
    double m_z;
    std::vector<double> m_descriptors;

public:
    // constructor
    Atom(int id, double x, double y, double z, int idOfTimestep)
        : m_id{id}, m_x{x}, m_y{y}, m_z{z}, m_idOfMasterTimestep{idOfTimestep} {}

    // getters
    inline int getId() { return m_id; };

    inline double getX() { return m_x; };

    inline double getY() { return m_y; };

    inline double getZ() { return m_z; };

    inline std::vector<double> getDescriptors() { return m_descriptors; };

    // methods
    void calculateDescriptors();

    void createVerletList();
};

#endif //DESCRIPTORS_ATOM_H
