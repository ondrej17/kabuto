/**
 * Name: 
 *      descriptors_atom.h
 * Author: 
 *      Ondrej Bily
 * Description: 
 *      Header file corresponding to class Atom. Object Atom is created for 
 *      each atom in system. Each atom has its id, coordinates and calculated 
 *      descriptors. 
 * 
 *      Since descriptors describe atom's surrounding, they must be chosen 
 *      carefully. Also, not all atoms are accounted in calculation of 
 *      descriptors for given atom, only those that are in "cut-off" sphere
 *      (in Verlet List). Different values for cut-off are used for each 
 *      type of descriptor.
 *       
 *      Descriptors consists of 14 values:
 *      * 8 symmetry function of type G2 (Behler-Parinello)
 *      * 3 symmetry function of type G3 (Behler-Parinello)
 *      * 3 Steinhardt parameters with l = 6, 7, 8   
 *      
 *      Note: periodic boundary conditions (PBC) are implemented as well.
 */

#ifndef DESCRIPTORS_ATOM_H
#define DESCRIPTORS_ATOM_H

#include <vector>
#include <map>
#include <cmath>
#include <chrono>

#include "boost/math/special_functions/spherical_harmonic.hpp"

class Atom
{
private:
    int m_id;                          // ID of atom
    double m_x;                        // coordinate x
    double m_y;                        // coordinate y
    double m_z;                        // coordinate z
    std::vector<double> m_descriptors; // descriptors of atom

    // descriptors-specific values: cutoff values and parameters
    double m_rMinSym;                                        // parameter for fcFunction method
    double m_rMaxSym;                                        // parameter for fcFunction method
    double m_rMinStein;                                      // parameter for fcFunction method
    double m_rMaxStein;                                      // parameter for fcFunction method
    std::vector<std::vector<double>> m_g2FunctionParameters; // parameters for G2 symmetry functions
    std::vector<double> m_g3FunctionParameters;              // parameters for G3 symmetry functions
    std::vector<int> m_steinhardtFunctionParameters;         // parameters for Steinhardt parameters

public:
    // constructor
    Atom(int id, double x, double y, double z)
        : m_id{id}, m_x{x}, m_y{y}, m_z{z}
    {
        // set the cutoff parameters (magical number for now)
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

        // prepare descriptors, i. e. 14 zeros
        m_descriptors.resize(14, 0.0);
    }

    // getters
    inline int getId() { return m_id; };
    inline double getX() { return m_x; };
    inline double getY() { return m_y; };
    inline double getZ() { return m_z; };
    inline std::vector<double> &getDescriptors() { return m_descriptors; };

    // method
    void calculateDescriptors(const double pbcX,
                              const double pbcY,
                              const double pbcZ,
                              const std::vector<int> &atomsInVerletListIds,
                              std::map<int, Atom> &atomsInVerletList);

    // descriptors-specific methods
    void evaluateSymmetryFunctions(const double pbcX,
                                   const double pbcY,
                                   const double pbcZ,
                                   const std::vector<int> &atomsInVerletListIds,
                                   std::map<int, Atom> &atomsInVerletList);
    void evaluateSteinhardtParameters(const double pbcX,
                                      const double pbcY,
                                      const double pbcZ,
                                      const std::vector<int> &atomsInVerletListIds,
                                      std::map<int, Atom> &atomsInVerletList);
    double symmetryFunctionG2(const double eta,
                              const double rs,
                              const double pbcX,
                              const double pbcY,
                              const double pbcZ,
                              const std::vector<int> &atomsInVerletListIds,
                              std::map<int, Atom> &atomsInVerletList);
    double symmetryFunctionG3(const double kappa,
                              const double pbcX,
                              const double pbcY,
                              const double pbcZ,
                              const std::vector<int> &atomsInVerletListIds,
                              std::map<int, Atom> &atomsInVerletList);
    double steinhardtFunction(const int l,
                              const double pbcX,
                              const double pbcY,
                              const double pbcZ,
                              const std::vector<int> &atomsInVerletListIds,
                              std::map<int, Atom> &atomsInVerletList);
    double fcFunction(const double r,
                      const double rMin,
                      const double rMax);
    double qlmFunction(const int m,
                       const int l,
                       const double pbcX,
                       const double pbcY,
                       const double pbcZ,
                       const std::vector<int> &atomsInVerletListIds,
                       std::map<int, Atom> &atomsInVerletList);
    double ylmFunction(const int m,
                       const int l,
                       const double dx,
                       const double dy,
                       const double dz);
    double getSphericalR(const double x,
                         const double y,
                         const double z);
    double getSphericalPhi(const double x,
                           const double y,
                           const double z);
    double getSphericalTheta(const double x,
                             const double y,
                             const double z);

    void print(std::vector<double> const &input);
};

#endif //DESCRIPTORS_ATOM_H
