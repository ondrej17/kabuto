#ifndef KABUTO_DESCRIPTORS_UTILITY_HPP
#define KABUTO_DESCRIPTORS_UTILITY_HPP

extern "C" {
#include <Python.h>
}

std::vector<double> listTupleToVector_Float(PyObject *incoming);

PyObject *vectorToTuple_Float(const std::vector<double> &data);

#endif //KABUTO_DESCRIPTORS_UTILITY_HPP
