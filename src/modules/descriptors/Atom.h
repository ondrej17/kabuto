#ifndef DESCRIPTORS_ATOM_H
#define DESCRIPTORS_ATOM_H

#include <vector>


class Atom {
private:
    int m_id;
    double m_x;
    double m_y;
    double m_z;
    std::vector<std::vector<double>> m_descriptors;

public:
    /**
     * Constructor of the class (the only one).
     * @param id ID of this atom.
     * @param x, y, z Coordinates of this atom
     */
    Atom(int id, double x, double y, double z)
            : m_id{id}, m_x{x}, m_y{y}, m_z{z} {}

    /**
     * Returns the ID of this atom.
     * @return ID of this atom.
     */
    inline int getId() {return m_id;};

    /**
     * Returns descriptors of the atom from given timestep.
     * @param jthTimestep The order number of timestep (counted form 0).
     * @returns (descriptor#1, descriptor#2, ..., descriptor#14)
     */
    std::vector<double> getDescriptors(int jthTimestep);

    /**
     * Calculates descriptors of the atom for the given timestep.
     * Checks whether the Verlet list of the atom had been already created.
     * @param jthTimestep The order number of timestep (counted form 0).
     */
    void calculateDescriptors(int jthTimestep);
};


#endif // DESCRIPTORS_ATOM_H
