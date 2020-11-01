#ifndef DESCRIPTORS_BOX_H
#define DESCRIPTORS_BOX_H

#include <vector>
#include "Atom.h"


class Box {
private:
    double m_pbcX;
    double m_pbcY;
    double m_pbcZ;
    std::vector <Atom> m_atoms;
    std::vector<int> m_timestepsId;

public:
    /**
     * Constructor of the class (the only one).
     * @param pbcX, pbcY, pbcZ Periodic boundary conditions in each direction.
     */
    Box(double pbcX, double pbcY, double pbcZ)
            : m_pbcX{pbcX}, m_pbcY{pbcY}, m_pbcZ{pbcZ} {
    }

    /**
     * Calculates descriptors for all atoms for all timesteps.
     */
    void calculateDescriptors();

    /**
     * Adds the ID of new timestep (mostly it is a time in ps from beginning of simulation).
     * @param id ID of timestep.
     */
    void addTimestepId(int id);

    /**
     * Adds new atom to the box.
     * @param id ID of the atom.
     * @param x, y, z Coordinates of the atom.
     */
    void addAtom(int id, double x, double y, double z);

    /**
     * Returns the number of timesteps in this box.
     * @returns number of timesteps in this box.
     */
    int getNumberOfTimesteps();

    /**
     * Returns the number of atoms in this box.
     * @returns number of atoms in this box.
     */
    int getNumberOfAtom();

    /**
     * Returns ID of the j-th timestep.
     * @param ithTimestep The order number of timestep (counted form 0).
     * @returns ID of the j-th timestep.
     */
    int getTimestepId(int ithTimestep);

    /**
     * Returns descriptors of the i-th atom from j-th timestep.
     * @param ithAtom The order number of atom (counted form 0).
     * @param jthTimestep The order number of timestep (counted form 0).
     * @return descriptors of the i-th atom from j-th timestep.
     */
    std::vector<double> getAtomDescriptors(int ithAtom, int jthTimestep);

    /**
     * Returns ID of the i-th atom.
     * @param ithAtom The order number of atom (counted form 0).
     * @returns ID of the i-th atom.
     */
    int getAtomId(int ithAtom);

};


#endif // DESCRIPTORS_BOX_H
