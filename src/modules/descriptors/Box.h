#ifndef KABUTO_BOX_H
#define KABUTO_BOX_H

#include <vector>
#include <pair>

#include "Timestep.h"
#include "VerletList.h"

class Box {
private:
    double m_pbcX;
    double m_pbcY;
    double m_pbcZ;
    std::vector <std::pair<int, Timestep>> m_timesteps;
    std::vector <std::pair<int, VerletList>> m_verletLists;
public:
    // constructor
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

    int getTimestepId();

    std::vector<double> getAtomDescriptors(int ithTimestep, int jthAtom);

};


#endif //KABUTO_BOX_H
