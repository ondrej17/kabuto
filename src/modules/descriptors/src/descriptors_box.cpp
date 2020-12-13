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

int Box::getNumOfAtoms()
{
    return m_timesteps.at(m_timestepsId[0]).getNumOfAtoms();
}

int Box::getNumOfAtomsInVerletList(int atomId)
{
    return m_verletLists.at(atomId).getNumOfAtoms();
}

const std::vector<int> &Box::getTimestepAtomsId(int timestepId)
{
    return m_timesteps.at(timestepId).getAtomsId();
}

const std::vector<double> &Box::getAtomDescriptors(int timestepId, int atomId)
{
    return m_timesteps.at(timestepId).getAtomDescriptors(atomId);
}

const std::vector<double> &Box::getPbcOfTimestep(int timestepId)
{
    return m_pbc.at(timestepId);
}

void Box::createVerletLists()
{
    // TODO: for now, Verlet lists are calculated ONLY on the beginning of simulation
    int timestepId{m_timestepsId[0]};
    std::vector<double> pbc{getPbcOfTimestep(timestepId)};
    std::vector<int> atomsId{m_timesteps.at(timestepId).getAtomsId()};
    std::map<int, Atom> atoms{m_timesteps.at(timestepId).getAtoms()};

    // go through all atoms in the first timestep
    for (int atomId : atomsId)
    {
        std::vector<int> idsInVerletList;
        double myX{atoms.at(atomId).getX()};
        double myY{atoms.at(atomId).getY()};
        double myZ{atoms.at(atomId).getZ()};

        // go through all atoms (except this atom) in the first timestep again
        // add atom to verlet list when condition is true ->
        for (int innerAtomId : atomsId)
        {
            if (innerAtomId != atomId)
            { // skip atomid

                // coordinates of other atom
                double otherX{atoms.at(innerAtomId).getX()};
                double otherY{atoms.at(innerAtomId).getY()};
                double otherZ{atoms.at(innerAtomId).getZ()};

                // components of the vector r_ij
                double x_ij{otherX - myX};
                double y_ij{otherY - myY};
                double z_ij{otherZ - myZ};

                // correction of vector r_ij for PBC (and minimum image convention)
                x_ij -= pbc[0] * std::round(x_ij / pbc[0]);
                y_ij -= pbc[1] * std::round(y_ij / pbc[1]);
                z_ij -= pbc[2] * std::round(z_ij / pbc[2]);

                // calculate the correct length of vector r_ij
                double r_ij{sqrt(pow(x_ij, 2) + pow(y_ij, 2) + pow(z_ij, 2))};

                if (r_ij <= m_rVerletListLimit) // innerAtom is inside of "Verlet sphere" of atom
                {
                    idsInVerletList.push_back(innerAtomId);
                }
            }
        }

        // add verlet list for this atom!
        m_verletLists.insert(std::make_pair(atomId, VerletList(atomId, idsInVerletList)));
    }
}

void Box::calculateDescriptors()
{
    // go through all timesteps
    for (int timestepId : m_timestepsId)
    {
        std::cout << "Calculating timestep #" << timestepId << std::endl;
        std::vector<int> atomsId{m_timesteps.at(timestepId).getAtomsId()};
        std::map<int, Atom> atoms{m_timesteps.at(timestepId).getAtoms()};
        std::vector<double> pbc{getPbcOfTimestep(timestepId)};

        // go through all atoms in given timestep
        for (int atomId : atomsId)
        {
            std::vector<int> atomsInVerletListId{m_verletLists.at(atomId).getAtomIds()};
            // create descriptors vector
            std::vector<double> descriptors{Descriptors(atomId,
                                                        pbc[0], pbc[1], pbc[2],
                                                        atomsInVerletListId,
                                                        atoms)
                                                .getDescriptors()};

            // set descriptors for given atom!
            m_timesteps.at(timestepId).setAtomDescriptors(atomId, descriptors);
        }
    }
}
