#ifndef KABUTO_ATOM_H
#define KABUTO_ATOM_H

#include <vector>

class Timestep; // forward declaration of Timestep class

class Atom {
private:
    int m_id;
    double m_x;
    double m_y;
    double m_z;
    std::vector<double> m_descriptors;
    Timestep &m_masterTimestep; // holds reference to Timestep object that contains this Atom object

public:
    // constructor
    Atom(int id, double x, double y, double z, Timestep &masterTimestep)
            : m_id{id}, m_x{x}, m_y{y}, m_z{z}, m_masterTimestep{masterTimestep} {}

    // getters
    inline int getId() { return m_id; };

    inline double getX() { return m_x; };

    inline double getY() { return m_y; };

    inline double getZ() { return m_z; };

    inline std::vector<double> getDescriptors() { return m_descriptors; };

    inline Timestep &getMasterTimestep() { return m_masterTimestep; };

    // methods
    void calculateDescriptors();

    void createVerletLists();
};


#endif //KABUTO_ATOM_H
