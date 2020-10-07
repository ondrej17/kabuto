#include <iostream>
#include <vector>
#include <cmath>
#include <boost/math/special_functions/spherical_harmonic.hpp>

#include "descriptorsmodule.h"

/**
  * Function that computes and returns descriptors for one timestep
  *
  * @param self Module that is calling this function
  * @param args It is then parsed to a single dictionary {atom_id:(x, y, z)}

  * @returns result Python dictionary {atom_id:(tuple of descriptors)}
  */
static PyObject *descriptors_compute(PyObject *self, PyObject *args) {
    std::cout << "C module begins" << std::endl;

    // parse args to atoms
    PyObject *atoms;
    double pbc_x = 0.0;
    double pbc_y = 0.0;
    double pbc_z = 0.0;
    if (!PyArg_ParseTuple(args, "dddO", &pbc_x, &pbc_y, &pbc_z, &atoms)) {
        return Py_BuildValue("d", 1);
    }

    PyObject *atom_ids = PyDict_Keys(atoms);
    PyObject *coordinates = PyDict_Values(atoms);
    Py_ssize_t pos1 = 0;

    std::vector<int> vector_atom_id;
    std::vector <std::vector<double>> vector_atom_coords;

    // iterate through {atoms_id:coords} and get C vectors
    while (PyDict_Next(atoms, &pos1, &atom_ids, &coordinates)) {

        // get current atom_id and push it to the vector
        vector_atom_id.push_back(PyLong_AsLong(atom_ids));

        // get atom coords and push it to the vector
        std::vector<double> curr_coordinates = listTupleToVector_Float(PyDict_GetItem(atoms, atom_ids));
        vector_atom_coords.push_back(curr_coordinates);

        // print current atom_id and coordinates
        std::cout << PyLong_AsLong(atom_ids) << "\t: ";
        for (std::vector<double>::const_iterator i = curr_coordinates.begin(); i != curr_coordinates.end(); ++i) {
            std::cout << *i << ' ';
        }
        std::cout << std::endl;
    }

    // create a vector of pbc values
    std::cout << "PBC: ";
    std::vector<double> pbc{pbc_x, pbc_y, pbc_z};
    for (std::vector<double>::const_iterator i = pbc.begin(); i != pbc.end(); ++i) {
        std::cout << *i << ' ';
    }
    std::cout << std::endl;

    // now, I work with two vectors:
    //  1. atom ids (1, 2, 3, 6, 90, 900, 96, ...)
    //  2. corresponding tuples of coordinates ((3, 4, 5), (3, 5, 7), (6, 7, 0), ...)

    std::cout << "Before calculating descriptors ..." << std::endl;
    std::vector <std::vector<double>> vector_descriptors;
    // calculate it for each atom:
    for (long unsigned int atom_id = 0; atom_id < vector_atom_id.size(); atom_id++) {
        std::vector<double> descriptors = calculate_descriptors(atom_id,
                                                                vector_atom_coords[atom_id],
                                                                vector_atom_id,
                                                                vector_atom_coords,
                                                                pbc);
        std::cout << "atom #" << atom_id << std::endl;
        for (std::vector<double>::const_iterator j = descriptors.begin(); j != descriptors.end(); ++j) {
            std::cout << *j << ' ';
        }
        std::cout << std::endl;
        vector_descriptors.push_back(descriptors);
    }

    std::cout << "After calculating descriptors ..." << std::endl;
    // now, I have two vectors:
    //  1. atom_ids
    //  2. corresponding tuples of descriptors
    // build a dictionary {atom_id:descriptors} from these two vectors
    PyObject *result = PyDict_New();
    for (long unsigned int i = 0; i < vector_atom_id.size(); i++) {
        // prepare id of atom
        PyObject *id = Py_BuildValue("i", vector_atom_id[i]);

        // prepare descriptors of atom
        PyObject *descriptors = vectorToTuple_Float(vector_descriptors[i]);

        // add new entry to python dictionary
        if (PyDict_SetItem(result, id, descriptors) != 0) {
            return Py_BuildValue("d", 2);
        }
    }

    // return a dictionary {atom_id:descriptors}
    std::cout << "C module ends" << std::endl;
    return result;
}

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
                                          std::vector<double> pbc) {
    // initialise resulting vector
    std::vector<double> result;

    result.push_back(symmetry_func_g_2(20.0, 2.8, id, coords, vector_id, vector_coords, pbc));
    result.push_back(symmetry_func_g_2(20.0, 3.2, id, coords, vector_id, vector_coords, pbc));
    result.push_back(symmetry_func_g_2(20.0, 4.4, id, coords, vector_id, vector_coords, pbc));
    result.push_back(symmetry_func_g_2(20.0, 4.8, id, coords, vector_id, vector_coords, pbc));
    result.push_back(symmetry_func_g_2(20.0, 5.0, id, coords, vector_id, vector_coords, pbc));
    result.push_back(symmetry_func_g_2(20.0, 5.3, id, coords, vector_id, vector_coords, pbc));
    result.push_back(symmetry_func_g_2(20.0, 5.7, id, coords, vector_id, vector_coords, pbc));
    result.push_back(symmetry_func_g_2(20.0, 6.0, id, coords, vector_id, vector_coords, pbc));

    result.push_back(symmetry_func_g_3(3.5, id, coords, vector_id, vector_coords, pbc));
    result.push_back(symmetry_func_g_3(4.5, id, coords, vector_id, vector_coords, pbc));
    result.push_back(symmetry_func_g_3(7.0, id, coords, vector_id, vector_coords, pbc));

    result.push_back(steinhardt_func(6, id, coords, vector_id, vector_coords, pbc));
    result.push_back(steinhardt_func(7, id, coords, vector_id, vector_coords, pbc));
    result.push_back(steinhardt_func(8, id, coords, vector_id, vector_coords, pbc));

    return result;
}

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
                         std::vector<double> pbc) {
    double result = 0.0;

    for (long unsigned int i = 0; i < vector_id.size(); i++) {
        if (id != vector_id[i]) {

            // vector r_ij
            double x_ij = vector_coords[i][0] - coords[0];
            double y_ij = vector_coords[i][1] - coords[1];
            double z_ij = vector_coords[i][2] - coords[2];

            // correction of vector r_ij for PBC (and minimum image convention)
            x_ij -= pbc[0] * std::round(x_ij / pbc[0]);
            y_ij -= pbc[1] * std::round(y_ij / pbc[1]);
            z_ij -= pbc[2] * std::round(z_ij / pbc[2]);

            // calculate the correct length of vector r_ij
            double r_ij = sqrt(pow(x_ij, 2) + pow(y_ij, 2) + pow(z_ij, 2));

            result += function_f_c(r_ij, R_MIN_SYM, R_MAX_SYM) * exp(-eta * pow(r_ij - r_s, 2));
        }
    }

    return result;
}

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
                         std::vector<double> pbc) {
    double result = 0.0;

    for (long unsigned int i = 0; i < vector_id.size(); i++) {
        if (id != vector_id[i]) {

            // vector r_ij
            double x_ij = vector_coords[i][0] - coords[0];
            double y_ij = vector_coords[i][1] - coords[1];
            double z_ij = vector_coords[i][2] - coords[2];

            // correction of vector r_ij for PBC (and minimum image convention)
            x_ij -= pbc[0] * std::round(x_ij / pbc[0]);
            y_ij -= pbc[1] * std::round(y_ij / pbc[1]);
            z_ij -= pbc[2] * std::round(z_ij / pbc[2]);

            // calculate the correct length of vector r_ij
            double r_ij = sqrt(pow(x_ij, 2) + pow(y_ij, 2) + pow(z_ij, 2));

            result += function_f_c(r_ij, R_MIN_SYM, R_MAX_SYM) * cos(kappa * r_ij);
        }
    }

    return result;
}

/**
 * Returns a value of Steinhardt parameter with l = l_param
 *
 * @param id
 * @param coords
 * @param vector_id
 * @param vector_coords
 * @param pbc
 *
 * @return double
 */
double steinhardt_func(int l_param,
                       int id,
                       std::vector<double> &coords,
                       std::vector<int> &vector_id,
                       std::vector <std::vector<double>> &vector_coords,
                       std::vector<double> pbc) {
    double result = 0.;

    for (int m = -l_param; m <= l_param; m++) {
        result += pow(fabs(function_q_lm(m, l_param, id, coords, vector_id, vector_coords, pbc)), 2);
    }

    return sqrt(result * 4 * M_PI / (2 * l_param + 1));
}

/**
 * Returns value of function Q_lm
 *
 * @param m
 * @param l_param
 * @param id
 * @param coords
 * @param vector_id
 * @param vector_coords
 * @param pbc
 *
 * @return double
 */
double function_q_lm(int m,
                     int l_param,
                     int id,
                     std::vector<double> &coords,
                     std::vector<int> &vector_id,
                     std::vector <std::vector<double>> &vector_coords,
                     std::vector<double> pbc) {
    // calculate numerator
    double numerator = 0.;
    for (long unsigned int i = 0; i < vector_id.size(); i++) {
        if (id != vector_id[i]) {

            // vector r_ij
            double x_ij = vector_coords[i][0] - coords[0];
            double y_ij = vector_coords[i][1] - coords[1];
            double z_ij = vector_coords[i][2] - coords[2];

            // correction of vector r_ij for PBC (and minimum image convention)
            x_ij -= pbc[0] * std::round(x_ij / pbc[0]);
            y_ij -= pbc[1] * std::round(y_ij / pbc[1]);
            z_ij -= pbc[2] * std::round(z_ij / pbc[2]);

            // calculate the correct length of vector r_ij
            double r_ij = sqrt(pow(x_ij, 2) + pow(y_ij, 2) + pow(z_ij, 2));

            numerator += function_f_c(r_ij, R_MIN_STEIN, R_MAX_STEIN) * function_y_lm(l_param, m,
                                                                                      x_ij, y_ij, z_ij);
        }
    }

    // calculate denominator
    double denominator = 0.;
    for (long unsigned int i = 0; i < vector_id.size(); i++) {
        if (id != vector_id[i]) {

            // vector r_ij
            double x_ij = vector_coords[i][0] - coords[0];
            double y_ij = vector_coords[i][1] - coords[1];
            double z_ij = vector_coords[i][2] - coords[2];

            // correction of vector r_ij for PBC (and minimum image convention)
            x_ij -= pbc[0] * std::round(x_ij / pbc[0]);
            y_ij -= pbc[1] * std::round(y_ij / pbc[1]);
            z_ij -= pbc[2] * std::round(z_ij / pbc[2]);

            // calculate the correct length of vector r_ij
            double r_ij = sqrt(pow(x_ij, 2) + pow(y_ij, 2) + pow(z_ij, 2));

            denominator += function_f_c(r_ij, R_MIN_STEIN, R_MAX_STEIN);
        }
    }

    return numerator / denominator;
}

/**
 * Returns value of spherical harmonics for given l and m
 * Uses Boost library
 *
 * @param l_param
 * @param m
 * @param dx X-component of vector between two atoms
 * @param dy Y-component of vector between two atoms
 * @param dz Z-component of vector between two atoms
 *
 * @return double
 */
double function_y_lm(int l_param, int m, double dx, double dy, double dz) {
    // spherical coordinates of vector r_ij
    double r {sqrt(pow(dx,2) + pow(dy,2) + pow(dz,2))};
    double phi {atan2(dy, dx)};
    double theta {acos(dz / r)};

    // return real form spherical harmonics in form Y_lm
    //      sph_harm() returns Y_l^m --> wikipedia
    if (m < 0) {
        return pow(-1, m) * M_SQRT2 * (boost::math::spherical_harmonic_i(abs(m), l_param, theta, phi));
    } else if (m == 0) {
        return boost::math::spherical_harmonic_r(0, l_param, theta, phi);
    } else {
        return pow(-1, m) * M_SQRT2 * (boost::math::spherical_harmonic_r(m, l_param, theta, phi));
    }
}

/**
  * Calculates the value of f_c function
  *
  * @param r
  * @param r_min
  * @param r_max
  *
  * @returns double
  */
double function_f_c(double r, double r_min, double r_max) {
    if (r <= r_min) {
        return 1.0;
    } else if ((r_min < r) && (r <= r_max)) {
        return 0.5 + 0.5 * cos(M_PI * (r - r_min) / (r_max - r_min));
    } else {
        return 0.0;
    }
}

/**
 * Converts PyObject(List/Tuple) to C++ Vector
 *
 * @param incoming It is a PyObject (PyTuple, PyList)
 *
 * @returns data Vector
 *
 * @throws Error when incoming was neither PyTuple, nor PyList
 */
std::vector<double> listTupleToVector_Float(PyObject *incoming) {
    std::vector<double> data;
    if (PyTuple_Check(incoming)) {
        for (Py_ssize_t i = 0; i < PyTuple_Size(incoming); i++) {
            PyObject *value = PyTuple_GetItem(incoming, i);
            data.push_back(PyFloat_AsDouble(value));
        }
    } else {
        if (PyList_Check(incoming)) {
            for (Py_ssize_t i = 0; i < PyList_Size(incoming); i++) {
                PyObject *value = PyList_GetItem(incoming, i);
                data.push_back(PyFloat_AsDouble(value));
            }
        } else {
            throw std::logic_error("Passed PyObject pointer was not a list or tuple!");
        }
    }
    return data;
}

/**
 * Converts data (C++ vector) to PyObject (PyTuple)
 *
 * @param incoming It is a C++ vector
 *
 * @returns tuple PyTuple
 *
 * @throws Error when there is not enough memory
 */
PyObject *vectorToTuple_Float(const std::vector<double> &data) {
    PyObject *tuple = PyTuple_New(data.size());
    if (!tuple) throw std::logic_error("Unable to allocate memory for Python tuple");
    for (unsigned int i = 0; i < data.size(); i++) {
        PyObject *num = PyFloat_FromDouble((double) data[i]);
        if (!num) {
            Py_DECREF(tuple);
            throw std::logic_error("Unable to allocate memory for Python tuple");
        }
        PyTuple_SET_ITEM(tuple, i, num);
    }

    return tuple;
}

/**
 * Defines methods that can be called from Python
 */
static PyMethodDef descriptors_methods[] = {
        // "PythonName",    C-function name,        argument presentation,  description
        {"compute", descriptors_compute, METH_VARARGS, "Compute descriptors"},
        {NULL,      NULL,                0,            NULL}   /* SENTINEL */
};

/**
 * Structure that holds information about module
 */
static struct PyModuleDef descriptors =
        {
                PyModuleDef_HEAD_INIT,
                "descriptors",      // name of module
                NULL,               // module documentation
                -1,                 // size of per-interpreter state of the module, or -1 if the module keeps state in global variables.
                descriptors_methods
        };

/**
 * Initialization class of C++ extension for Python
 */
PyMODINIT_FUNC PyInit_descriptors(void) {
    return PyModule_Create(&descriptors);
}


