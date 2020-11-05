#include "descriptors_module.h"

static PyObject *descriptors_compute(PyObject *self, PyObject *args)
{

    // parse args
    PyObject *inputDictionary;
    double pbcX = 0.0;
    double pbcY = 0.0;
    double pbcZ = 0.0;
    if (!PyArg_ParseTuple(args, "dddO", &pbcX, &pbcY, &pbcZ, &inputDictionary))
    {
        // TODO: check for incorrect parsing
        return Py_BuildValue("d", 1);
    }

    // create and fill Box object
    Box box = Box(pbcX, pbcY, pbcZ);

    // parse each timestep in inputDictionary
    PyObject *timestepId = PyDict_Keys(inputDictionary);
    PyObject *timestep = PyDict_Values(inputDictionary);
    Py_ssize_t pos1 = 0;
    while (PyDict_Next(inputDictionary, &pos1, &timestepId, &timestep))
    {
        // get ID of timestep
        long int idOfTimestep{PyLong_AsLong(timestepId)};
        box.addTimestep(idOfTimestep);

        // get timestep
        PyObject *atoms;
        if (!PyArg_ParseTuple(timestep, "O", &atoms))
        {
            // TODO: check for incorrect parsing
            return Py_BuildValue("d", 1);
        }

        // parse each atom in timestep
        PyObject *atomId = PyDict_Keys(atoms);
        PyObject *atomCoords = PyDict_Values(atoms);
        Py_ssize_t pos2 = 0;
        while (PyDict_Next(atoms, &pos2, &atomId, &atomCoords))
        {
            // get current id and coordinates of current atom
            long int idOfAtom = PyLong_AsLong(atomId);
            std::vector<double> coordinates = listTupleToVector_Float(PyDict_GetItem(atoms, atomId));

            // add atom to box
            box.addAtomToTimestep(idOfTimestep, idOfAtom, coordinates[0], coordinates[1], coordinates[2]);
        }
    }

    // create Verlet lists
    box.createVerletLists();

    // calculate descriptors for each atom
    box.calculateDescriptors();

    // create Python dictionary that will be passed back to Python script
    PyObject *result = PyDict_New();

    for (std::pair<int, Timestep> idAndTimestep : box.getAllTimesteps())
    {
        // next timestep
        PyObject *timestepDict = PyDict_New();

        for (std::pair<int, Atom> idAndAtom : (idAndTimestep.second).getAllAtoms())
        {
            // next atom
            int atomId{idAndAtom.first};
            std::vector<double> atomDescriptors{(idAndAtom.second).getDescriptors()};

            // prepare id and descriptors of atom
            PyObject *id = Py_BuildValue("i", atomId);
            PyObject *descriptors = vectorToTuple_Float(atomDescriptors);

            // add new entry to python dictionary
            if (PyDict_SetItem(timestepDict, id, descriptors) != 0)
            {
                // TODO: check for incorrect setting item in PyDict
                return Py_BuildValue("d", 2);
            }
        }
        int timestepIdInt{idAndTimestep.first};
        PyObject *timestepId = Py_BuildValue("i", timestepIdInt);
        if (PyDict_SetItem(result, timestepId, timestepDict) != 0)
        {
            // TODO: check for incorrect setting item in PyDict
            return Py_BuildValue("d", 2);
        }
    }

    // return a Python dictionary {atom_id:descriptors}
    return result;
}

/**
 * PyMethodDef list that defines methods that can be called from Python.
 */
static PyMethodDef descriptors_methods[] = {
    // "PythonName",    C-function name,        argument presentation,  description
    {"compute", descriptors_compute, METH_VARARGS, "Computes descriptors for one timestep."},
    {NULL, NULL, 0, NULL}};

/**
 * Structure that holds information about module.
 */
static struct PyModuleDef descriptors = {
    PyModuleDef_HEAD_INIT, // init function of module
    "descriptors",         // name of module
    NULL,                  // module documentation
    -1,                    // size of per-interpreter state of the module,
    // or -1 if the module keeps state in global variables.
    descriptors_methods // list of methods that can be called from Python
};

/**
 * Initialization function of C++ extension for Python
 */
PyMODINIT_FUNC PyInit_descriptors(void)
{
    return PyModule_Create(&descriptors);
}
