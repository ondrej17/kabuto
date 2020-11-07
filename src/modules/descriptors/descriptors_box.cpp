#include "descriptors_box.h"

void Box::addTimestep(int timestepId)
{
    m_numOfTimesteps++;
    m_timestepsId.push_back(timestepId);
    m_timesteps.insert(std::make_pair(timestepId, Timestep{timestepId}));
}

void Box::addAtomToTimestep(int timestepId, int atomId, double x, double y, double z)
{
    m_timesteps.at(timestepId).addAtom(atomId, x, y, z);
}

std::vector<int> &Box::getTimestepAtomsId(int timestepId)
{
    return m_timesteps.at(timestepId).getAtomsId();
}

void Box::createVerletLists()
{
    // TODO: implement the Verlet lists
    int timestepId{m_timestepsId[0]}; // use the first timestep
    std::vector<int> atomsId{m_timesteps.at(timestepId).getAtomsId()};
    std::map<int, Atom> atoms{m_timesteps.at(timestepId).getAtoms()};

    // go through all atoms in the first timestep
    for (int atomId : atomsId)
    {
        std::vector<int> idsInVerletList;

        // go through all atoms (except this atom) in the first timestep again
        // add atom to verlet list when condition is true ->
        for (int innerAtomId : atomsId)
        {
            if (innerAtomId != atomId)
            {
                if (true)
                {
                    idsInVerletList.push_back(innerAtomId);
                }
            }
        }

        // add verlet list for this atom!
        m_verletLists.insert(std::make_pair(atomId, VerletList(atomId, idsInVerletList)));
    }
}

const std::vector<double> &Box::getAtomDescriptors(int timestepId, int atomId)
{
    return m_timesteps.at(timestepId).getAtomDescriptors(atomId);
}

void Box::calculateDescriptors()
{
    // TODO: implement the calculation of descriptors using functions in descriptors_func_module.h

    // go through all timesteps
    for (int timestepId : m_timestepsId)
    {

        std::vector<int> atomsId{m_timesteps.at(timestepId).getAtomsId()};
        std::map<int, Atom> atoms{m_timesteps.at(timestepId).getAtoms()};

        // go through all atoms in given timestep
        for (int atomId : atomsId)
        {

            // DUMMY calculation of descriptors ->
            std::vector<double> descriptors(14, DUMMY_DOUBLE);
            //  <-

            // set descriptors for given atom!
            m_timesteps.at(timestepId).setAtomDescriptors(atomId, descriptors);
        }
    }
}
