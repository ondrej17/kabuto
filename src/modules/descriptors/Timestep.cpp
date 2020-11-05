#include "Timestep.h"

void Timestep::calculateDescriptors()
{
    std::map<int, Atom>::iterator it;
    for (it = m_atoms.begin(); it != m_atoms.end(); it++)
    {
        (it->second).calculateDescriptors();
    }
}

void Timestep::createVerletLists()
{
    std::map<int, Atom>::iterator it;
    for (it = m_atoms.begin(); it != m_atoms.end(); it++)
    {
        (it->second).createVerletList();
    }
}

void Timestep::addAtom(int id, double x, double y, double z)
{
    m_atoms.insert(std::make_pair(id, Atom(id, x, y, z, m_id)));
}

int Timestep::getNumberOfAtom()
{
    return m_atoms.size();
}

std::vector<double> Timestep::getAtomDescriptors(int atomId)
{
    return m_atoms[atomId].getDescriptors();
}

std::map<int, Atom> Timestep::getAllAtoms()
{
    return m_atoms;
}