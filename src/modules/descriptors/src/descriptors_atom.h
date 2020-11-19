/**
 * 
 * 
 * 
 * 
 * 
 * 
 * 
 */

#ifndef DESCRIPTORS_ATOM_H
#define DESCRIPTORS_ATOM_H

#include <vector>

class Atom
{
private:
    int m_id;
    double m_x;
    double m_y;
    double m_z;
    std::vector<double> m_descriptors;

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
