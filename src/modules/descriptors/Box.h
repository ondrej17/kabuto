#ifndef DESCRIPTORS_BOX_H
#define DESCRIPTORS_BOX_H

#include <utility>
#include <map>
#include <iterator>

#include "Timestep.h"
#include "VerletList.h"

class Box
{
private:
    double m_pbcX;
    double m_pbcY;
    double m_pbcZ;

protected:
    std::map<int, VerletList> m_verletLists;
    std::map<int, Timestep> m_timesteps;

public:
    // constructor
    Box();
    Box(double pbcX, double pbcY, double pbcZ)
        : m_pbcX{pbcX}, m_pbcY{pbcY}, m_pbcZ{pbcZ} {}

    // getters
    inline double getPbcX() { return m_pbcX; };

    inline double getPbcY() { return m_pbcY; };

    inline double getPbcZ() { return m_pbcZ; };

    // methods
    void calculateDescriptors();

    void createVerletLists();

    void addTimestep(int id);

    void addAtomToTimestep(int timestepId, int atomId, double x, double y, double z);

    int getNumberOfTimesteps();

    int getNumberOfAtom();

    std::vector<double> getAtomDescriptors(int timestepId, int atomId);

    void addToVerletList(int id, int idOfAtomInVerletList);

    const std::map<int, Timestep> getAllTimesteps() { return m_timesteps; };
};

#endif //DESCRIPTORS_BOX_H
