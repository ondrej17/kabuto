#include <iostream>
#include <vector>

#include "descriptorsmodule.h"

/*
 *  Functions
 */

// function that computes and returns descriptors for one timestep
static PyObject *descriptors_compute(PyObject* self, PyObject *args) {

    // parse args to atoms
    PyObject *atoms;
    if (!PyArg_ParseTuple(args, "O", &atoms)) {
          return Py_BuildValue("d", 1);
    }

    PyObject    *atom_ids       = PyDict_Keys(atoms);
    PyObject    *coordinates    = PyDict_Values(atoms);
    Py_ssize_t  pos1            = 0;

    std::vector<int>                    vector_atom_id;
    std::vector<std::vector<floadescriptorsmodule.cppt>>     vector_atom_coords;

    // iterate through {atoms_id:coords} and get C vectors
    while (PyDict_Next(atoms, &pos1, &atom_ids, &coordinates)) {

        // get current atom_id and push it to the vector
        vector_atom_id.push_back(PyLong_AsLong(atom_ids));

        // get atom coords and push it to the vector
        std::vector<float> curr_coordinates = listTupleToVector_Float(PyDict_GetItem(atoms, atom_ids));
        vector_atom_coords.push_back(curr_coordinates);

        // print current atom_id and coordinates
        std::cout << PyLong_AsLong(atom_ids) << "\t: ";
        for (std::vector<float>::const_iterator i = curr_coordinates.begin(); i != curr_coordinates.end(); ++i) {
            std::cout << *i << ' ';
        }
        std::cout << std::endl;
    }

    // now, I work with two vectors:
    //  1. atom ids (1, 2, 3, 6, 90, 900, 96, ...)
    //  2. corresponding tuples of coordinates ((3, 4, 5), (3, 5, 7), (6, 7, 0), ...)

    // I need to calculate descriptors!
    // ...


    // return a dictionary {atom_id:descriptors}
    return Py_BuildValue("d", 0);
}

// convert PyObject to C++ Vector
std::vector<float> listTupleToVector_Float(PyObject* incoming) {
	std::vector<float> data;
	if (PyTuple_Check(incoming)) {
		for(Py_ssize_t i = 0; i < PyTuple_Size(incoming); i++) {
			PyObject *value = PyTuple_GetItem(incoming, i);
			data.push_back( PyFloat_AsDouble(value) );
		}
	} else {
		if (PyList_Check(incoming)) {
			for(Py_ssize_t i = 0; i < PyList_Size(incoming); i++) {
				PyObject *value = PyList_GetItem(incoming, i);
				data.push_back( PyFloat_AsDouble(value) );
			}
		} else {
			throw std::logic_error("Passed PyObject pointer was not a list or tuple!");
		}
	}
	return data;
}

/*
 *  Other stuff needed to compile module
 */

static PyMethodDef descriptors_methods[] = {
    // "PythonName",    C-function name,        argument presentation,  description
    {"compute",         descriptors_compute,    METH_VARARGS,           "Compute descriptors"},
    {NULL, NULL, 0, NULL}   /* SENTINEL */
};

static struct PyModuleDef descriptors =
{
    PyModuleDef_HEAD_INIT,
    "decsriptors",      // name of module
    NULL,               // module documentation
    -1,                 // size of per-interpreter state of the module, or -1 if the module keeps state in global variables.
    descriptors_methods
};

PyMODINIT_FUNC PyInit_descriptors(void)
{
    return PyModule_Create(&descriptors);
}


