/**
 * Name: 
 *      descriptors_module.h
 * Author: 
 *      Ondrej Bily
 * Description: 
 *      Header file corresponding to module descriptors. It is the main
 *      part of C++ extension for Python.
 */

#ifndef DESCRIPTORS_H
#define DESCRIPTORS_H

#include <iostream>
#include <vector>
#include <chrono>

extern "C"
{
#include <Python.h>
}

#include "descriptors_utility.h"
#include "descriptors_box.h"

/**
  * Function that computes and returns descriptors for all timesteps of the simulation.
  * This function provides interface between Python and C++ extension.
  * This function is callable from Python script using `descriptors.compute(pbc_x, pbc_y, pbc_y, all_timesteps)`.
  *
  * @param self Module that is calling this function (that's me)
  * @param args Arguments needed for a calculation: dict(timestep_id, (pbcX, pbcY, pbcZ)), dict(timestep_id, dict(atom_id, (x, y, z)))
  * @returns result A Python dictionary {timestep_id: {atom_id:(tuple of descriptors)}}
  */
static PyObject *descriptors_compute(PyObject *self, PyObject *args);

/**
 * PyMethodDef list that defines methods that can be called from Python.
 * Each method must be defined as:
 *    {<PythonName>, <C-function name>, <argument presentation>, <description>}
 */
static PyMethodDef descriptors_methods[] = {
    {"compute", descriptors_compute, METH_VARARGS,
     "Computes descriptors for given timesteps. Callable from Python script "
     "using `descriptors.compute(pbc_x, pbc_y, pbc_y, all_timesteps)`."},
    {NULL, NULL, 0, NULL}};

/**
 * Structure that holds information about module.
 * Items of structure:
 *    * init function of module,
 *    * name of module,
 *    * module documentation,
 *    * size of per-interpreter state of the module,
 *      or -1 if the module keeps state in global variables,
 *    * list of methods that can be called from Python
 */
static struct PyModuleDef descriptors = {
    PyModuleDef_HEAD_INIT, "descriptors", NULL, -1, descriptors_methods};

/**
 * Initialization function of C++ extension for Python
 */
PyMODINIT_FUNC PyInit_descriptors(void)
{
  return PyModule_Create(&descriptors);
}

#endif // DESCRIPTORS_H