#ifndef __DESCRIPTORSFUNC__
#define __DESCRIPTORSFUNC__

#include <iostream>
#include <vector>
#include <cmath>
#include <boost/math/special_functions/spherical_harmonic.hpp>

extern "C" {
#include <Python.h>
}

#define R_MIN_SYM 6.2
#define R_MAX_SYM 6.4
#define R_MIN_STEIN 3.8
#define R_MAX_STEIN 4.0


/**
 * Calculates descriptors for a given atom_id
 *
 * @param id Id of the atom, for which descriptors will be calculated
 * @param coords Coordinates (x, y, z) of given atom
 * @param vector_id Ids of all atoms
 * @param vector_coords Tuples (x,y,z) of all atoms
 * @param pbc
 *
 * @returns result Tuple of 14 real numbers - descriptors
 */
std::vector<double> calculate_descriptors(int id,
                                          std::vector<double> &coords,
                                          std::vector<int> &vector_id,
                                          std::vector <std::vector<double>> &vector_coords,
                                          std::vector<double> pbc);

/**
 * Symmetry function G_2
 *
 * @param eta
 * @param r_s
 * @param id Id of the atom, for which the function is evaluated
 * @param coords Coordinates (x, y, z) of given atom
 * @param vector_id Ids of all atoms
 * @param vector_coords Tuples (x,y,z) of all atoms
 * @param pbc
 *
 * @returns result
 */
double symmetry_func_g_2(double eta,
                         double r_s,
                         int id,
                         std::vector<double> &coords,
                         std::vector<int> &vector_id,
                         std::vector <std::vector<double>> &vector_coords,
                         std::vector<double> pbc);

/**
* Symmetry function G_3
*
* @param kappa
* @param id Id of the atom, for which the function is evaluated
* @param coords Coordinates (x, y, z) of given atom
* @param vector_id Ids of all atoms
* @param vector_coords Tuples (x,y,z) of all atoms
* @param pbc
*
* @returns result
*/
double symmetry_func_g_3(double kappa,
                         int id,
                         std::vector<double> &coords,
                         std::vector<int> &vector_id,
                         std::vector <std::vector<double>> &vector_coords,
                         std::vector<double> pbc);

/**
 * Returns a value of Steinhardt parameter with l = l
 *
 * @param id
 * @param coords
 * @param vector_id
 * @param vector_coords
 * @param pbc
 *
 * @return double
 */
double steinhardt_func(int l,
                       int id,
                       std::vector<double> &coords,
                       std::vector<int> &vector_id,
                       std::vector <std::vector<double>> &vector_coords,
                       std::vector<double> pbc);

/**
 * Returns value of function Q_lm
 *
 * @param m
 * @param l
 * @param id
 * @param coords
 * @param vector_id
 * @param vector_coords
 * @param pbc
 *
 * @return double
 */
double function_q_lm(int m,
                     int l,
                     int id,
                     std::vector<double> &coords,
                     std::vector<int> &vector_id,
                     std::vector <std::vector<double>> &vector_coords,
                     std::vector<double> pbc);

/**
 * Returns value of spherical harmonics for given l and m
 * Uses Boost library
 *
 * @param l
 * @param m
 * @param dx X-component of vector between two atoms
 * @param dy Y-component of vector between two atoms
 * @param dz Z-component of vector between two atoms
 *
 * @return double
 */
double function_y_lm(int l, int m, double dx, double dy, double dz);

/**
  * Calculates the value of f_c function
  *
  * @param r
  * @param r_min
  * @param r_max
  *
  * @returns double
  */
double function_f_c(double r, double r_min, double r_max);


#endif