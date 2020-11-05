#ifndef DESCRIPTORS_UTILITY_H
#define DESCRIPTORS_UTILITY_H

extern "C" {
#include <Python.h>
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
std::vector<double> listTupleToVector_Float(PyObject *incoming);

/**
 * Converts data (C++ vector) to PyObject (PyTuple)
 *
 * @param incoming It is a C++ vector
 *
 * @returns tuple PyTuple
 *
 * @throws Error when there is not enough memory
 */
PyObject *vectorToTuple_Float(const std::vector<double> &data);

#endif //DESCRIPTORS_UTILITY_H
