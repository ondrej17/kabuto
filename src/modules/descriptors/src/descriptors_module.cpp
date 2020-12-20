#include "descriptors_module.h"

static PyObject *descriptors_compute(PyObject *self, PyObject *args)
{
    std::cout << std::endl;

    auto start = std::chrono::steady_clock::now();
    std::chrono::duration<double> timeFromStart;

    timeFromStart = std::chrono::steady_clock::now() - start;
    // std::cout << timeFromStart.count() << "s - Parsing arguments ..." << std::endl;
    // parse args
    PyObject *pyTimestepDictionary;
    PyObject *pyPbcDictionary;
    if (!PyArg_ParseTuple(args, "OO", &pyPbcDictionary, &pyTimestepDictionary))
    {
        return Py_BuildValue("d", 1);
    }

    timeFromStart = std::chrono::steady_clock::now() - start;
    // std::cout << timeFromStart.count() << "s - Parsing pbc ..." << std::endl;
    // parse pbc for each timestep in pbcDictionary
    std::map<int, std::vector<double>> pbcMap; // {timestepId:[pbcX, pbcY, pbcZ]}
    PyObject *pyTimestepId = PyDict_Keys(pyPbcDictionary);
    PyObject *pyTimestep = PyDict_Values(pyPbcDictionary);
    Py_ssize_t pos1 = 0;
    while (PyDict_Next(pyPbcDictionary, &pos1, &pyTimestepId, &pyTimestep))
    {
        // get ID of timestep
        long int idOfTimestep{PyLong_AsLong(pyTimestepId)};

        // get pbc's of this timestep
        std::vector<double> pbcs = listTupleToVector_Float(PyDict_GetItem(pyPbcDictionary, pyTimestepId));

        // add entry to pbcMap
        //pbcMap[idOfTimestep] = pbcs;
        pbcMap.insert(std::make_pair<int, std::vector<double>>(idOfTimestep, std::move(pbcs)));
    }

    timeFromStart = std::chrono::steady_clock::now() - start;
    // std::cout << timeFromStart.count() << "s - Creating Box object ..." << std::endl;
    // create Box object
    Box box(std::move(pbcMap));

    timeFromStart = std::chrono::steady_clock::now() - start;
    // std::cout << timeFromStart.count() << "s - Parsing timestep dictionary ..." << std::endl;
    // parse each timestep in pyTimestepDictionary
    pyTimestepId = PyDict_Keys(pyTimestepDictionary);
    pyTimestep = PyDict_Values(pyTimestepDictionary);
    pos1 = 0;
    while (PyDict_Next(pyTimestepDictionary, &pos1, &pyTimestepId, &pyTimestep))
    {
        // get ID of timestep
        long int idOfTimestep{PyLong_AsLong(pyTimestepId)};
        box.addTimestep(idOfTimestep);

        // get atoms in timestep
        PyObject *pyAtoms;
        if (!PyArg_Parse(pyTimestep, "O", &pyAtoms))
        {
            return Py_BuildValue("d", 1);
        }

        // parse each atom in atoms
        PyObject *pyAtomId = PyDict_Keys(pyAtoms);
        PyObject *pyAtomCoords = PyDict_Values(pyAtoms);
        Py_ssize_t pos2 = 0;
        while (PyDict_Next(pyAtoms, &pos2, &pyAtomId, &pyAtomCoords))
        {
            // get current id and coordinates of current atom
            long int idOfAtom = PyLong_AsLong(pyAtomId);
            std::vector<double> coordinates = listTupleToVector_Float(PyDict_GetItem(pyAtoms, pyAtomId));

            // add atom to box (and to correct timestep)
            box.addAtomToTimestep(idOfTimestep, idOfAtom, coordinates.at(0), coordinates.at(1), coordinates.at(2));
        }
    }

    timeFromStart = std::chrono::steady_clock::now() - start;
    // std::cout << timeFromStart.count() << "s - Creating Verlet lists ..." << std::endl;
    // create Verlet lists
    box.createVerletLists();
    // std::cout << "Number of atoms in Box: " << box.getNumOfAtoms() << std::endl;
    // int atomIndex{box.getTimestepAtomsId(box.getTimestepsId().at(0)).at(0)};
    // std::cout << "Number of atoms in Verlet list of atom #" << atomIndex << ": "
            //   << box.getNumOfAtomsInVerletList(atomIndex) << std::endl;

    timeFromStart = std::chrono::steady_clock::now() - start;
    // std::cout << timeFromStart.count() << "s - Calculating descriptors ..." << std::endl;
    // calculate descriptors for each atom
    box.calculateDescriptors();

    timeFromStart = std::chrono::steady_clock::now() - start;
    // std::cout << timeFromStart.count() << "s - Creating result object ..." << std::endl;
    
    // create Python dictionary that will be passed back to Python script
    PyObject *pyResult = PyDict_New();
    std::vector<int> timestepsId{box.getTimestepsId()};

    // go through all timesteps
    for (int timestepId : timestepsId)
    {
        PyObject *pyTimestepDict = PyDict_New();

        std::vector<int> atomsId{box.getTimestepAtomsId(timestepId)};

        for (int atomId : atomsId)
        {
            std::vector<double> atomDescriptors{box.getAtomDescriptors(timestepId, atomId)};

            // prepare id and descriptors of atom
            PyObject *pyId = Py_BuildValue("i", atomId);
            PyObject *pyDescriptors = vectorToTuple_Float(atomDescriptors);

            // add new entry to python dictionary
            if (PyDict_SetItem(pyTimestepDict, pyId, pyDescriptors) != 0)
            {
                return Py_BuildValue("d", 2);
            }
        }

        PyObject *pyTimestepId = Py_BuildValue("i", timestepId);
        if (PyDict_SetItem(pyResult, pyTimestepId, pyTimestepDict) != 0)
        {
            return Py_BuildValue("d", 2);
        }
    }
    timeFromStart = std::chrono::steady_clock::now() - start;
    // std::cout << timeFromStart.count() << "s - Ending ..." << std::endl;
    // std::cout << std::endl;

    // return a Python dictionary {timestepId: {atom_id:descriptors}}
    return pyResult;
}
