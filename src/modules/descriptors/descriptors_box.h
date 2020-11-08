/**
 * Name: 
 *      descriptors_box.h
 * Author: 
 *      Ondrej Bily
 * Description: 
 *      Header file corresponding to class Box. Object Box is created in 
 *      descriptor_module's "compute" function. In this function, A python 
 *      arguments are parsed into C++ objects. Namely, all timesteps are 
 *      contained in the Box object. Object Box is also responsible for 
 *      creating Verlet lists for each atom and for calculating descriptors
 *      for each atom.  
 */

#ifndef DESCRIPTORS_BOX_H
#define DESCRIPTORS_BOX_H

#include <utility>
#include <map>
#include <vector>

#include "descriptors_timestep.h"
#include "descriptors_atom.h"
#include "descriptors_verlet_list.h"
#include "descriptors_descriptors.h"

class Box
{
protected:
    double m_pbcX;
    double m_pbcY;
    double m_pbcZ;
    int m_numOfTimesteps;
    std::map<int, VerletList> m_verletLists;
    std::map<int, Timestep> m_timesteps;
    std::vector<int> m_timestepsId;

public:
    // constructor
    Box(double pbcX, double pbcY, double pbcZ)
        : m_pbcX{pbcX}, m_pbcY{pbcY}, m_pbcZ{pbcZ}
    {
        m_numOfTimesteps = 0;
    }

    // getters
    inline int getNumOfTimesteps() { return m_numOfTimesteps; };
    inline double getPbcX() { return m_pbcX; };
    inline double getPbcY() { return m_pbcY; };
    inline double getPbcZ() { return m_pbcZ; };
    inline std::map<int, VerletList> &getVerletLists() { return m_verletLists; };
    inline std::map<int, Timestep> &getTimesteps() { return m_timesteps; };
    inline std::vector<int> &getTimestepsId() { return m_timestepsId; };

    // methods
    void addTimestep(int timestepId);
    void addAtomToTimestep(int timestepId, int atomId, double x, double y, double z);
    void createVerletLists();
    void calculateDescriptors();
    const std::vector<double> &getAtomDescriptors(int timestepId, int atomId);
    const std::vector<int> &getTimestepAtomsId(int timestepId);
};

#endif //DESCRIPTORS_BOX_H
