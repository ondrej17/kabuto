#include "Atom.h"

void Atom::calculateDescriptors()
{
    // TODO: implement the calculation of the descriptors

    // 8 symmetry function g_2
    m_descriptors.push_back(DUMMY_DOUBLE);
    m_descriptors.push_back(DUMMY_DOUBLE);
    m_descriptors.push_back(DUMMY_DOUBLE);
    m_descriptors.push_back(DUMMY_DOUBLE);
    m_descriptors.push_back(DUMMY_DOUBLE);
    m_descriptors.push_back(DUMMY_DOUBLE);
    m_descriptors.push_back(DUMMY_DOUBLE);
    m_descriptors.push_back(DUMMY_DOUBLE);

    // 3 symmetry function g_3
    m_descriptors.push_back(DUMMY_DOUBLE);
    m_descriptors.push_back(DUMMY_DOUBLE);
    m_descriptors.push_back(DUMMY_DOUBLE);

    // 3 steinhardt parameters
    m_descriptors.push_back(DUMMY_DOUBLE);
    m_descriptors.push_back(DUMMY_DOUBLE);
    m_descriptors.push_back(DUMMY_DOUBLE);
}

void Atom::createVerletList()
{
    for (std::pair<int, Atom> idAndAtom : m_timesteps[m_idOfMasterTimestep].getAllAtoms())
    {
        double x{idAndAtom.second.getX()};
        double y{idAndAtom.second.getY()};
        double z{idAndAtom.second.getZ()};

        // TODO: define valid condition for accepting atom in Verlet list
        // for now, all atoms are put in the Verlet list
        if (true)
        {
            addToVerletList(m_id, idAndAtom.first);
        }
    }
}