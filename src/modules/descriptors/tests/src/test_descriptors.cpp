/**
 * Tests for Descriptors class
 * 
 * 
 */

#define BOOST_TEST_MODULE test_descriptors

#include "../../src/descriptors_descriptors.h"
#include <boost/test/unit_test.hpp>

int id{1};
double pbcX{6.3}, pbcY{6.3}, pbcZ{6.3};
std::vector<int> atomsInVerletList{2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 16, 14, 15, 16};
std::map<int, Atom> atoms = {
    // atoms in BCC structure (2x2x2 = 16 atoms)
    {1, Atom(1, 0.849862, 0.849862, 0.849862)},
    {2, Atom(2, 2.42493, 2.42493, 2.42493)},
    {3, Atom(3, 4, 0.849862, 0.849862)},
    {4, Atom(4, 5.57507, 2.42493, 2.42493)},
    {5, Atom(5, 0.849862, 4, 0.849862)},
    {6, Atom(6, 2.42493, 5.57507, 2.42493)},
    {7, Atom(7, 4, 4, 0.849862)},
    {8, Atom(8, 5.57507, 5.57507, 2.42493)},
    {9, Atom(9, 0.849862, 0.849862, 4)},
    {10, Atom(10, 2.42493, 2.42493, 5.57507)},
    {11, Atom(11, 4, 0.849862, 4)},
    {12, Atom(12, 5.57507, 2.42493, 5.57507)},
    {13, Atom(13, 0.849862, 4, 4)},
    {14, Atom(14, 2.42493, 5.57507, 5.57507)},
    {15, Atom(15, 4, 4, 4)},
    {16, Atom(16, 5.57507, 5.57507, 5.57507)},
};

// global descriptors object
Descriptors descriptors(id, pbcX, pbcY, pbcZ, atomsInVerletList, atoms);

BOOST_AUTO_TEST_CASE(testCutoffFunction)
{
    double epsilon{0.0001};
    BOOST_TEST(fabs(descriptors.fcFunction(14.0, 10.0, 12.0) - 0.0) < epsilon);
    BOOST_TEST(fabs(descriptors.fcFunction(11.0, 10.0, 12.0) - 0.5) < epsilon);
    BOOST_TEST(fabs(descriptors.fcFunction(11.5, 10.0, 12.0) - 0.1464) < epsilon);
    BOOST_TEST(fabs(descriptors.fcFunction(2.0, 10.0, 12.0) - 1.0) < epsilon);
    // what if one or more of the parameter(s) is/are negative?
    // what if rMin > rMax ?
}

BOOST_AUTO_TEST_CASE(testSphericalCoordinates)
{
    double epsilon{0.00001};

    BOOST_TEST(fabs(descriptors.getSphericalR(0.0, 0.0, 0.0) - 0.0) < epsilon);
    // BOOST_TEST(fabs(descriptors.getSphericalPhi(0.0, 0.0, 0.0) - ???) < epsilon);
    // BOOST_TEST(fabs(descriptors.getSphericalTheta(0.0, 0.0, 0.0) - ???) < epsilon);

    BOOST_TEST(fabs(descriptors.getSphericalR(1.0, 1.0, 1.0) - sqrt(3.0)) < epsilon);
    BOOST_TEST(fabs(descriptors.getSphericalPhi(1.0, 1.0, 1.0) - M_PI_4) < epsilon);
    BOOST_TEST(fabs(descriptors.getSphericalTheta(1.0, 1.0, 1.0) - 0.955317) < epsilon);

    BOOST_TEST(fabs(descriptors.getSphericalR(-1.0, 1.0, 1.0) - sqrt(3.0)) < epsilon);
    BOOST_TEST(fabs(descriptors.getSphericalPhi(-1.0, 1.0, 1.0) - (M_PI - M_PI_4)) < epsilon);
    BOOST_TEST(fabs(descriptors.getSphericalTheta(-1.0, 1.0, 1.0) - 0.955317) < epsilon);

    BOOST_TEST(fabs(descriptors.getSphericalR(1.0, -1.0, 1.0) - sqrt(3.0)) < epsilon);
    BOOST_TEST(fabs(descriptors.getSphericalPhi(1.0, -1.0, 1.0) - (-M_PI_4)) < epsilon);
    BOOST_TEST(fabs(descriptors.getSphericalTheta(1.0, -1.0, 1.0) - 0.955317) < epsilon);

    BOOST_TEST(fabs(descriptors.getSphericalR(1.0, 1.0, -1.0) - sqrt(3.0)) < epsilon);
    BOOST_TEST(fabs(descriptors.getSphericalPhi(1.0, 1.0, -1.0) - M_PI_4) < epsilon);
    BOOST_TEST(fabs(descriptors.getSphericalTheta(1.0, 1.0, -1.0) - 2.186276) < epsilon);

    // more tests can be added
}

BOOST_AUTO_TEST_CASE(testYlmFunction)
{
    double epsilon{0.00001};
    double result;

    // int m, int l, double dx, double dy, double dz
    result = 0.5 * sqrt(1 / M_PI);
    BOOST_TEST(fabs(descriptors.ylmFunction(0, 0, 1.0, 2.0, 3.0) - result) < epsilon);

    result = sqrt(3 / (4 * M_PI)) * (3.0 / sqrt(14.0));
    BOOST_TEST(fabs(descriptors.ylmFunction(0, 1, 1.0, 2.0, 3.0) - result) < epsilon);

    result = sqrt(3 / (4 * M_PI)) * (1.0 / sqrt(14.0));
    BOOST_TEST(fabs(descriptors.ylmFunction(1, 1, 1.0, 2.0, 3.0) - result) < epsilon);

    result = sqrt(3 / (4 * M_PI)) * (2.0 / sqrt(14.0));
    BOOST_TEST(fabs(descriptors.ylmFunction(-1, 1, 1.0, 2.0, 3.0) - result) < epsilon);

    result = 0.5 * sqrt(15 / M_PI) * (3.0 / 14.0);
    BOOST_TEST(fabs(descriptors.ylmFunction(1, 2, 1.0, 2.0, 3.0) - result) < epsilon);

    // more tests can be added
}

BOOST_AUTO_TEST_CASE(testQlmFunction)
{
    double epsilon{0.00001};
    double result;

    // TODO: calculate result for the given atoms with calculation only!
    // result = ...;
    // BOOST_TEST(fabs(descriptors.qlmFunction(0, 0) - result) < epsilon);

    // more tests can be added
}