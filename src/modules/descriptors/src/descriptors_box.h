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
    std::map<int, std::vector<double>> m_pbc;   // PBCs foreach timestep
    int m_numOfTimesteps;                       // number of timesteps of system
    double m_rVerletListLimit;                  // cutoff for atoms in the Verlet List 
    std::map<int, VerletList> m_verletLists;    // map of Verlet List for each atom
    std::map<int, Timestep> m_timesteps;        // map of all timesteps of systems
    std::vector<int> m_timestepsId;             // IDs of all timesteps

public:
    // constructor
    Box(std::map<int, std::vector<double>> pbcMap)
        : m_pbc{pbcMap}
    {
        m_numOfTimesteps = 0;       // no timesteps at the beginning
        m_rVerletListLimit = 7.4;   // because rMaxSym = 6.4 (magical number for now)
    }

    // getters
    inline std::map<int, std::vector<double>> getPbc() { return m_pbc; };
    inline int getNumOfTimesteps() { return m_numOfTimesteps; };
    inline double getRVerletListLimit() { return m_rVerletListLimit; };
    inline std::map<int, VerletList> &getVerletLists() { return m_verletLists; };
    inline std::map<int, Timestep> &getTimesteps() { return m_timesteps; };
    inline std::vector<int> &getTimestepsId() { return m_timestepsId; };

    // methods
    void addTimestep(int timestepId);
    void addAtomToTimestep(int timestepId, int atomId, double x, double y, double z);
    void createVerletLists();
    void calculateDescriptors();
    int getNumOfAtoms();
    int getNumOfAtomsInVerletList(int atomId);
    const std::vector<double> &getAtomDescriptors(int timestepId, int atomId);
    const std::vector<double> &getPbcOfTimestep(int timestepId);
    const std::vector<int> &getTimestepAtomsId(int timestepId);
};

#endif //DESCRIPTORS_BOX_H
