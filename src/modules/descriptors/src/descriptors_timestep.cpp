#include "descriptors_timestep.h"

void Timestep::addAtom(int atomId, double x, double y, double z)
{
    m_numOfAtoms++;
    m_atomsId.push_back(atomId);
    m_atoms.insert(std::pair<int, Atom>(atomId, Atom(atomId, x, y, z)));
}

Atom &Timestep::getAtom(int id)
{
    return m_atoms.at(id);
}

const std::vector<double> &Timestep::getAtomDescriptors(int atom_id)
{
    return  m_atoms.at(atom_id).getDescriptors();
}
