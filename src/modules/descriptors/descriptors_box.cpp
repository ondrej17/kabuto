#include "Box.h"

void Box::calculateDescriptors()
{
    std::map<int, Timestep>::iterator it;
    for (it = m_timesteps.begin(); it != m_timesteps.end(); it++)
    {
        (it->second).calculateDescriptors();
    }
}

void Box::createVerletLists()
{
    int indexOffirstTimestep{(m_timesteps.begin())->first};
    m_timesteps[indexOffirstTimestep].createVerletLists();
}

void Box::addTimestep(int id)
{
    m_timesteps.insert(std::make_pair(id, Timestep(id)));
}

void Box::addAtomToTimestep(int timestepId, int atomId, double x, double y, double z)
{
    m_timesteps[timestepId].addAtom(atomId, x, y, z);
}

int Box::getNumberOfTimesteps()
{
    return m_timesteps.size();
}

int Box::getNumberOfAtom()
{
    int indexOffirstTimestep{(m_timesteps.begin())->first};
    return m_timesteps[indexOffirstTimestep].getNumberOfAtom();
}

std::vector<double> Box::getAtomDescriptors(int timestepId, int atomId)
{
    return m_timesteps[timestepId].getAtomDescriptors(atomId);
}

void Box::addToVerletList(int id, int idOfAtomInVerletList)
{
    m_verletLists[id].pushBack(idOfAtomInVerletList);
}