#include "descriptors_timestep.h"

void Timestep::addAtom(int atomId, double x, double y, double z)
{
    m_numOfAtoms++;
    m_atomsId.push_back(atomId);
    Atom atom = Atom(atomId, x, y, z);
    m_atoms.insert(std::make_pair(atomId, atom));
}

Atom &Timestep::getAtom(int id)
{
    return m_atoms.at(id);
}

const std::vector<double> &Timestep::getAtomDescriptors(int atom_id)
{
    return  m_atoms.at(atom_id).getDescriptors();
}

void Timestep::setAtomDescriptors(int atom_id, std::vector<double> descriptors)
{
    m_atoms.at(atom_id).setDescriptors(descriptors);
}
