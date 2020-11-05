#ifndef DESCRIPTORS_H
#define DESCRIPTORS_H

#include <iostream>
#include <vector>

extern "C"
{
#include <Python.h>
}

#include "descriptors_utility.h"
#include "Box.h"

/**
  * Function that computes and returns descriptors for all timesteps of the simulation.
  * This function provides interface between Python and C++ extension.
  * This function is callable from Python script using `descriptors.compute(pbc_x, pbc_y, pbc_y, all_timesteps)`.
  *
  * @param self Module that is calling this function (that's me)
  * @param args Arguments needed for a calculation: pbc(x), pbc(y), pbc(z), dict(timestep_id, dict(atom_id, (x, y, z)))

  * @returns result A Python dictionary {timestep_id: {atom_id:(tuple of descriptors)}}
  */
static PyObject *descriptors_compute(PyObject *self, PyObject *args);

#endif // DESCRIPTORS_H