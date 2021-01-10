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
#include <chrono>

#include "descriptors_timestep.h"
#include "descriptors_atom.h"
#include "descriptors_verlet_list.h"

class Box
{
protected:
    std::map<int, std::vector<double>> m_pbc; // PBCs foreach timestep

    int m_numOfTimesteps;                     // number of timesteps of system
    double m_rVerletListLimit;                // cutoff for atoms in the Verlet List
    std::map<int, VerletList> m_verletLists;  // map of Verlet List for each atom
    std::map<int, Timestep> m_timesteps;      // map of all timesteps of systems
    std::vector<int> m_timestepsId;           // IDs of all timesteps

    double m_rMinSym;       // rMin of cutoff function for symmetry functions
    double m_rMaxSym;       // rMax of cutoff function for symmetry functions
    double m_rMinStein;     // rMin of cutoff function for Steinhardt parameters
    double m_rMaxStein;     // rMax of cutoff function for Steinhardt parameters

    std::vector<std::vector<double>> m_g2FunctionParameters;    // parameters for G2 symmetry functions
    std::vector<double> m_g3FunctionParameters;                 // parameters for G3 symmetry functions
    std::vector<int> m_steinhardtFunctionParameters;            // parameters for Steinhardt parameters

public:
    // constructor
    Box(std::map<int, std::vector<double>> pbcMap)
        : m_pbc{pbcMap}
    {
        m_numOfTimesteps = 0;     // no timesteps at the beginning
        m_rVerletListLimit = 7.4; // because rMaxSym = 6.4 (magical number for now)

        // set the cutoff parameters
        m_rMinSym = 6.2;
        m_rMaxSym = 6.4;
        m_rMinStein = 3.8;
        m_rMaxStein = 4.0;

        // set the parameters for g2 function
        m_g2FunctionParameters.reserve(8);
        m_g2FunctionParameters.push_back(std::vector<double>{20.0, 2.8});
        m_g2FunctionParameters.push_back(std::vector<double>{20.0, 3.2});
        m_g2FunctionParameters.push_back(std::vector<double>{20.0, 4.4});
        m_g2FunctionParameters.push_back(std::vector<double>{20.0, 4.8});
        m_g2FunctionParameters.push_back(std::vector<double>{20.0, 5.0});
        m_g2FunctionParameters.push_back(std::vector<double>{20.0, 5.3});
        m_g2FunctionParameters.push_back(std::vector<double>{20.0, 5.7});
        m_g2FunctionParameters.push_back(std::vector<double>{20.0, 6.0});

        // set the parameters for g3 function
        m_g3FunctionParameters.reserve(3);
        m_g3FunctionParameters.push_back(3.5);
        m_g3FunctionParameters.push_back(4.5);
        m_g3FunctionParameters.push_back(7.0);

        // set the parameters for steinhardt function
        m_steinhardtFunctionParameters.reserve(3);
        m_steinhardtFunctionParameters.push_back(6);
        m_steinhardtFunctionParameters.push_back(7);
        m_steinhardtFunctionParameters.push_back(8);
    }

    // getters
    inline std::map<int, std::vector<double>> getPbc() { return m_pbc; };
    inline int getNumOfTimesteps() { return m_numOfTimesteps; };
    inline double getRVerletListLimit() { return m_rVerletListLimit; };
    inline std::map<int, VerletList> &getVerletLists() { return m_verletLists; };
    inline std::map<int, Timestep> &getTimesteps() { return m_timesteps; };
    inline std::vector<int> &getTimestepsId() { return m_timestepsId; };

    // methods
    /**
     * Adds new timestep to box
     *
     * @param timestepId
     */
    void addTimestep(int timestepId);

    /**
     * Adds new atom to specific timestep
     *
     * @param timestepId
     * @param atomId
     * @param x, y, z
     */
    void addAtomToTimestep(int timestepId, int atomId, double x, double y, double z);

    /**
     * Creates Verlet lists for all atoms based on configuration at first timestep
     */
    void createVerletLists();

    /**
     * Calculates descriptors for all atoms in all timesteps
     */
    void calculateDescriptors();

    /**
     * Returns number of atoms in first timestep
     */
    int getNumOfAtoms();

    /**
     * Returns number of atoms in Verlet list of specific atom
     *
     * @param atomId
     */
    int getNumOfAtomsInVerletList(int atomId);

    /**
     * Returns descriptors of specific atom in specific timestep
     *
     * @param timestepId
     * @param atomId
     */
    const std::vector<double> &getAtomDescriptors(int timestepId, int atomId);

    /**
     * Returns a vector of PBC in specific timestep
     *
     * @param timestepId
     */
    const std::vector<double> &getPbcOfTimestep(int timestepId);

    /**
     * Returns a vector of atoms Ids in specific timestep
     *
     * @param timestepId
     */
    const std::vector<int> &getTimestepAtomsId(int timestepId);
};

#endif //DESCRIPTORS_BOX_H
