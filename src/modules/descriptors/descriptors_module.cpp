#include <iostream>
#include <vector>

#include "descriptors_module.hpp"
#include "descriptors_func_module.hpp"


/**
  * Function that computes and returns descriptors for one timestep
  *
  * @param self Module that is calling this function
  * @param args It is then parsed to a single dictionary {atom_id:(x, y, z)}

  * @returns result Python dictionary {atom_id:(tuple of descriptors)}
  */
static PyObject *descriptors_compute(PyObject *self, PyObject *args) {
    // parse args to c-variables
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
    std::vector<std::vector<double>> vector_atom_coords;

    // iterate through {atoms_id:coords} and get C vectors
    while (PyDict_Next(atoms, &pos1, &atom_ids, &coordinates)) {
        // get current atom_id and push it to the vector
        vector_atom_id.push_back(PyLong_AsLong(atom_ids));

        // get atom coords and push it to the vector
        std::vector<double> curr_coordinates = listTupleToVector_Float(PyDict_GetItem(atoms, atom_ids));
        vector_atom_coords.push_back(curr_coordinates);
    }

    // create a vector of pbc values
    std::vector<double> pbc{pbc_x, pbc_y, pbc_z};

    // calculate descriptors for each atom:
    std::vector <std::vector<double>> vector_descriptors;
    for (long unsigned int atom_id = 0; atom_id < vector_atom_id.size(); atom_id++) {
        std::vector<double> descriptors = calculate_descriptors(vector_atom_id[atom_id],
                                                                vector_atom_coords[atom_id],
                                                                vector_atom_id,
                                                                vector_atom_coords,
                                                                pbc);
        vector_descriptors.push_back(descriptors);
    }

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
    return result;
}

/**
 * Defines methods that can be called from Python
 */
static PyMethodDef descriptors_methods[] = {
        // "PythonName",    C-function name,        argument presentation,  description
        {"compute", descriptors_compute, METH_VARARGS, "Compute descriptors for one timestep"},
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


