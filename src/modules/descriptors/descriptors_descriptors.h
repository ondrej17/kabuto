/**
 * 
 * 
 * 
 * 
 * 
 * 
 * 
 */

#ifndef DESCRIPTORS_DESCRIPTORS_H
#define DESCRIPTORS_DESCRIPTORS_H

#include <map>
#include <cmath>
#include <boost/math/special_functions/spherical_harmonic.hpp>

#include "descriptors_atom.h"

class Descriptors
{
private:
    int m_id;
    double m_pbcX;
    double m_pbcY;
    double m_pbcZ;

    std::vector<int> m_atomsId;
    std::map<int, Atom> m_atoms;

    // descriptors-specific values
    double m_rMinSym;
    double m_rMaxSym;
    double m_rMinStein;
    double m_rMaxStein;
    std::vector<std::vector<double>> m_g2FunctionParameters;
    std::vector<double> m_g3FunctionParameters;
    std::vector<int> m_steinhardtFunctionParameters;

public:
    // constructor
    Descriptors(int atomId,
                double pbcX,
                double pbcY,
                double pbcZ,
                const std::vector<int> &atomsInVerletListIds,
                const std::map<int, Atom> &atoms)
        : m_id{atomId}, m_pbcX{pbcX}, m_pbcY{pbcY}, m_pbcZ{pbcZ},
          m_atomsId{atomsInVerletListIds}, m_atoms{atoms}
    {
        // set the cutoff parameters
        m_rMinSym = 6.2;
        m_rMaxSym = 6.4;
        m_rMinStein = 3.8;
        m_rMaxStein = 4.0;

        // set the parameters for g2 function
        m_g2FunctionParameters.push_back(std::vector<double>(20.0, 2.8));
        m_g2FunctionParameters.push_back(std::vector<double>(20.0, 3.2));
        m_g2FunctionParameters.push_back(std::vector<double>(20.0, 4.4));
        m_g2FunctionParameters.push_back(std::vector<double>(20.0, 4.8));
        m_g2FunctionParameters.push_back(std::vector<double>(20.0, 5.0));
        m_g2FunctionParameters.push_back(std::vector<double>(20.0, 5.3));
        m_g2FunctionParameters.push_back(std::vector<double>(20.0, 5.7));
        m_g2FunctionParameters.push_back(std::vector<double>(20.0, 6.0));

        // set the parameters for g3 function
        m_g3FunctionParameters.push_back(3.5);
        m_g3FunctionParameters.push_back(4.5);
        m_g3FunctionParameters.push_back(7.0);

        // set the parameters for steinhardt function
        m_steinhardtFunctionParameters.push_back(6);
        m_steinhardtFunctionParameters.push_back(7);
        m_steinhardtFunctionParameters.push_back(8);
    }

    // methods
    std::vector<double> getDescriptors();

    // descriptors-specific methods
    double symmetryFunctionG2(double eta, double rs);
    double symmetryFunctionG3(double kappa);
    double steinhardtFunction(int l);
    double fcFunction(double r, double rMin, double rMax);
    double qlmFunction(int m, int l);
    double ylmFunction(int m, int l, double dx, double dy, double dz);
};

#endif // DESCRIPTORS_DESCRIPTORS_H