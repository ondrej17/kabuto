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
#include <iostream>

class Atom
{
private:
    int m_id;                          // ID of atom
    double m_x;                        // coordinate x
    double m_y;                        // coordinate y
    double m_z;                        // coordinate z
    std::vector<double> m_descriptors; // descriptors of atom

public:
    // constructor
    Atom(int id, double x, double y, double z)
        : m_id{id}, m_x{x}, m_y{y}, m_z{z}
    {
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
                              std::map<int, Atom> &atomsInVerletList,
                              const double rMinSym,
                              const double rMaxSym,
                              const double rMinStein,
                              const double rMaxStein,
                              const std::vector<std::vector<double>> &g2FunctionParameters,
                              const std::vector<double> &g3FunctionParameters,
                              const std::vector<int> &steinhardtFunctionParameters);

    // descriptors-specific methods
    void evaluateSymmetryFunctions(const double pbcX,
                                   const double pbcY,
                                   const double pbcZ,
                                   const std::vector<int> &atomsInVerletListIds,
                                   std::map<int, Atom> &atomsInVerletList,
                                   const double rMinSym,
                                   const double rMaxSym,
                                   const std::vector<std::vector<double>> &g2FunctionParameters,
                                   const std::vector<double> &g3FunctionParameters);
    void evaluateSteinhardtParameters(const double pbcX,
                                      const double pbcY,
                                      const double pbcZ,
                                      const std::vector<int> &atomsInVerletListIds,
                                      std::map<int, Atom> &atomsInVerletList,
                                      const double rMinStein,
                                      const double rMaxStein,
                                      const std::vector<int> &steinhardtFunctionParameters);
//    double symmetryFunctionG2(const double eta,
//                              const double rs,
//                              const double pbcX,
//                              const double pbcY,
//                              const double pbcZ,
//                              const std::vector<int> &atomsInVerletListIds,
//                              std::map<int, Atom> &atomsInVerletList);
//    double symmetryFunctionG3(const double kappa,
//                              const double pbcX,
//                              const double pbcY,
//                              const double pbcZ,
//                              const std::vector<int> &atomsInVerletListIds,
//                              std::map<int, Atom> &atomsInVerletList);
//    double steinhardtFunction(const int l,
//                              const double pbcX,
//                              const double pbcY,
//                              const double pbcZ,
//                              const std::vector<int> &atomsInVerletListIds,
//                              std::map<int, Atom> &atomsInVerletList);
    double fcFunction(const double r,
                      const double rMin,
                      const double rMax);
    double qlmFunction(const int m,
                       const int l,
                       const double pbcX,
                       const double pbcY,
                       const double pbcZ,
                       const std::vector<int> &atomsInVerletListIds,
                       std::map<int, Atom> &atomsInVerletList,
                       const double rMinStein,
                       const double rMaxStein);
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
