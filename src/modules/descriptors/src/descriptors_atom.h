/**
 * Name: 
 *      descriptors_atom.h
 * Author: 
 *      Ondrej Bily
 * Description: 
 *      Header file corresponding to class Atom. Object Atom is created for 
 *      each atom in system. Each atom has its id, coordinates and calculated 
 *      descriptors. Descriptors are calculated in Box object.
 */

#ifndef DESCRIPTORS_ATOM_H
#define DESCRIPTORS_ATOM_H

#include <vector>

class Atom
{
private:
    int m_id;                           // ID of atom
    double m_x;                         // coordinate x
    double m_y;                         // coordinate y
    double m_z;                         // coordinate z
    std::vector<double> m_descriptors;  // descriptors of atom

public:
    // constructor
    Atom(int id, double x, double y, double z)
        : m_id{id}, m_x{x}, m_y{y}, m_z{z} {}

    // getters
    inline int getId() { return m_id; };
    inline double getX() { return m_x; };
    inline double getY() { return m_y; };
    inline double getZ() { return m_z; };
    inline const std::vector<double> &getDescriptors() { return m_descriptors; };

    // setters
    inline void setDescriptors(std::vector<double> descriptors) { m_descriptors = descriptors; };
};

#endif //DESCRIPTORS_ATOM_H
