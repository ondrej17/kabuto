#ifndef __DESCRIPTORSFUNC__
#define __DESCRIPTORSFUNC__

extern "C" {
#include <Python.h>
}

#define R_MIN_SYM 6.2
#define R_MAX_SYM 6.4
#define R_MIN_STEIN 3.8
#define R_MAX_STEIN 4.0

std::vector<double> listTupleToVector_Float(PyObject *incoming);

PyObject *vectorToTuple_Float(const std::vector<double> &data);

double function_f_c(double r, double r_min, double r_max);

std::vector<double> calculate_descriptors(int id,
                                          std::vector<double> &coords,
                                          std::vector<int> &vector_id,
                                          std::vector <std::vector<double>> &vector_coords,
                                          std::vector<double> pbc);

double symmetry_func_g_2(double eta,
                         double r_s,
                         int id,
                         std::vector<double> &coords,
                         std::vector<int> &vector_id,
                         std::vector <std::vector<double>> &vector_coords,
                         std::vector<double> pbc);

double symmetry_func_g_3(double kappa,
                         int id,
                         std::vector<double> &coords,
                         std::vector<int> &vector_id,
                         std::vector <std::vector<double>> &vector_coords,
                         std::vector<double> pbc);

double steinhardt_func(int l,
                       int id,
                       std::vector<double> &coords,
                       std::vector<int> &vector_id,
                       std::vector <std::vector<double>> &vector_coords,
                       std::vector<double> pbc);

double function_q_lm(int m,
                     int l,
                     int id,
                     std::vector<double> &coords,
                     std::vector<int> &vector_id,
                     std::vector <std::vector<double>> &vector_coords,
                     std::vector<double> pbc);

double function_y_lm(int l, int m, double dx, double dy, double dz);

#endif