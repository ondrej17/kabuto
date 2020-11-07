/**
 * 
 * 
 * 
 * 
 * 
 * 
 * 
 */

#ifndef DESCRIPTORS_BOX_H
#define DESCRIPTORS_BOX_H

#include <utility>
#include <map>

#include "descriptors_timestep.h"
#include "descriptors_atom.h"
#include "descriptors_verlet_list.h"

class Box
{
private:
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
    const std::vector<double> &getAtomDescriptors(int timestepId, int atomId);
    std::vector<int> &getTimestepAtomsId(int timestepId);
    void createVerletLists();
    void calculateDescriptors();
};

#endif //DESCRIPTORS_BOX_H
