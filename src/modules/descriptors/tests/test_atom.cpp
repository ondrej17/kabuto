/**
 * Tests for Atom class
 * 
 * Copyright 2005, Google Inc.
 * All rights reserved.
 */

#include "gtest/gtest.h"

#include "../src/descriptors_atom.h"

using namespace ::testing;

int id{1};
double pbcX{6.3}, pbcY{6.3}, pbcZ{6.3};
std::vector<int> atomsInVerletList{2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16};
std::map<int, Atom> atoms = {
    // atoms in pure BCC structure (2x2x2 = 16 atoms)
    //      id      x[A]        y[A]        z[A]
    {1, Atom(1, 0.84986, 0.84986, 0.84986)},
    {2, Atom(2, 2.42493, 2.42493, 2.42493)},
    {3, Atom(3, 4.00000, 0.84986, 0.84986)},
    {4, Atom(4, 5.57507, 2.42493, 2.42493)},
    {5, Atom(5, 0.84986, 4.00000, 0.84986)},
    {6, Atom(6, 2.42493, 5.57507, 2.42493)},
    {7, Atom(7, 4.00000, 4.00000, 0.84986)},
    {8, Atom(8, 5.57507, 5.57507, 2.42493)},
    {9, Atom(9, 0.84986, 0.84986, 4.00000)},
    {10, Atom(10, 2.42493, 2.42493, 5.57507)},
    {11, Atom(11, 4.00000, 0.84986, 4.00000)},
    {12, Atom(12, 5.57507, 2.42493, 5.57507)},
    {13, Atom(13, 0.84986, 4.00000, 4.00000)},
    {14, Atom(14, 2.42493, 5.57507, 5.57507)},
    {15, Atom(15, 4.00000, 4.00000, 4.00000)},
    {16, Atom(16, 5.57507, 5.57507, 5.57507)},
};

TEST(testAtom, id)
{
    Atom test_atom(42, 0.9, 23.4, 5.6);
    ASSERT_EQ(42, test_atom.getId());
}

TEST(testAtom, coordinateX)
{
    Atom test_atom(42, 0.9, 23.4, 5.6);
    ASSERT_EQ(0.9, test_atom.getX());
}

TEST(testAtom, coordinateY)
{
    Atom test_atom(42, 0.9, 23.4, 5.6);
    ASSERT_EQ(23.4, test_atom.getY());
}

TEST(testAtom, coordinateZ)
{
    Atom test_atom(42, 0.9, 23.4, 5.6);
    ASSERT_EQ(5.6, test_atom.getZ());
}

TEST(testAtom, testCutoffFunction1)
{
    Atom atom(1, 0.84986, 0.84986, 0.84986);
    double epsilon{0.0001};
    double result;

    result = 0.0;
    ASSERT_TRUE(fabs(atom.fcFunction(14.0, 10.0, 12.0) - result) < epsilon);
    // what if one or more of the parameter(s) is/are negative?
    // what if rMin > rMax ?
}

TEST(testAtom, testCutoffFunction2)
{
    Atom atom(1, 0.84986, 0.84986, 0.84986);
    double epsilon{0.0001};
    double result;

    result = 0.5;
    ASSERT_TRUE(fabs(atom.fcFunction(11.0, 10.0, 12.0) - result) < epsilon);
    // what if one or more of the parameter(s) is/are negative?
    // what if rMin > rMax ?
}

TEST(testAtom, testCutoffFunction3)
{
    Atom atom(1, 0.84986, 0.84986, 0.84986);
    double epsilon{0.0001};
    double result;

    result = 0.1464;
    ASSERT_TRUE(fabs(atom.fcFunction(11.5, 10.0, 12.0) - result) < epsilon);
    // what if one or more of the parameter(s) is/are negative?
    // what if rMin > rMax ?
}

TEST(testAtom, testCutoffFunction4)
{
    Atom atom(1, 0.84986, 0.84986, 0.84986);
    double epsilon{0.0001};
    double result;

    result = 1.0;
    ASSERT_TRUE(fabs(atom.fcFunction(2.0, 10.0, 12.0) - result) < epsilon);
    // what if one or more of the parameter(s) is/are negative?
    // what if rMin > rMax ?
}

TEST(testAtom, testSphericalCoordinatesR)
{
    Atom atom(1, 0.84986, 0.84986, 0.84986);
    double epsilon{0.00001};
    double result;

    result = 0.0;
    ASSERT_TRUE(fabs(atom.getSphericalR(0.0, 0.0, 0.0) - result) < epsilon);

    result = sqrt(3.0);
    ASSERT_TRUE(fabs(atom.getSphericalR(1.0, 1.0, 1.0) - result) < epsilon);

    result = sqrt(3.0);
    ASSERT_TRUE(fabs(atom.getSphericalR(-1.0, 1.0, 1.0) - result) < epsilon);

    result = sqrt(3.0);
    ASSERT_TRUE(fabs(atom.getSphericalR(1.0, -1.0, 1.0) - result) < epsilon);

    result = sqrt(3.0);
    ASSERT_TRUE(fabs(atom.getSphericalR(1.0, 1.0, -1.0) - result) < epsilon);

    // more tests can be added
}

TEST(testAtom, testSphericalCoordinatesPhi)
{
    Atom atom(1, 0.84986, 0.84986, 0.84986);
    double epsilon{0.00001};
    double result;

    // result = ???;
    // ASSERT_TRUE(fabs(atom.getSphericalPhi(0.0, 0.0, 0.0) - ???) < epsilon);

    result = M_PI_4;
    ASSERT_TRUE(fabs(atom.getSphericalPhi(1.0, 1.0, 1.0) - result) < epsilon);

    result = M_PI - M_PI_4;
    ASSERT_TRUE(fabs(atom.getSphericalPhi(-1.0, 1.0, 1.0) - result) < epsilon);

    result = -M_PI_4;
    ASSERT_TRUE(fabs(atom.getSphericalPhi(1.0, -1.0, 1.0) - result) < epsilon);

    result = M_PI_4;
    ASSERT_TRUE(fabs(atom.getSphericalPhi(1.0, 1.0, -1.0) - result) < epsilon);

    // more tests can be added
}

TEST(testAtom, testSphericalCoordinatesTheta)
{
    Atom atom(1, 0.84986, 0.84986, 0.84986);
    double epsilon{0.00001};
    double result;

    // result = ???;
    // ASSERT_TRUE(fabs(atom.getSphericalTheta(0.0, 0.0, 0.0) - ???) < epsilon);

    result = 0.955317;
    ASSERT_TRUE(fabs(atom.getSphericalTheta(1.0, 1.0, 1.0) - result) < epsilon);

    result = 0.955317;
    ASSERT_TRUE(fabs(atom.getSphericalTheta(-1.0, 1.0, 1.0) - result) < epsilon);

    result = 0.955317;
    ASSERT_TRUE(fabs(atom.getSphericalTheta(1.0, -1.0, 1.0) - result) < epsilon);

    result = 2.186276;
    ASSERT_TRUE(fabs(atom.getSphericalTheta(1.0, 1.0, -1.0) - result) < epsilon);

    // more tests can be added
}

TEST(testAtom, testYlmFunction1)
{
    Atom atom(1, 0.84986, 0.84986, 0.84986);
    double epsilon{0.00001};
    double result;

    result = 0.5 * sqrt(1 / M_PI);
    ASSERT_TRUE(fabs(atom.ylmFunction(0, 0, 1.0, 2.0, 3.0) - result) < epsilon);

    result = sqrt(3 / (4 * M_PI)) * (3.0 / sqrt(14.0));
    ASSERT_TRUE(fabs(atom.ylmFunction(0, 1, 1.0, 2.0, 3.0) - result) < epsilon);

    result = sqrt(3 / (4 * M_PI)) * (1.0 / sqrt(14.0));
    ASSERT_TRUE(fabs(atom.ylmFunction(1, 1, 1.0, 2.0, 3.0) - result) < epsilon);

    result = sqrt(3 / (4 * M_PI)) * (2.0 / sqrt(14.0));
    ASSERT_TRUE(fabs(atom.ylmFunction(-1, 1, 1.0, 2.0, 3.0) - result) < epsilon);

    result = 0.5 * sqrt(15 / M_PI) * (3.0 / 14.0);
    ASSERT_TRUE(fabs(atom.ylmFunction(1, 2, 1.0, 2.0, 3.0) - result) < epsilon);

    // more tests can be added
}

TEST(testAtom, testQlmFunction1)
{
    Atom atom(1, 0.84986, 0.84986, 0.84986);
    double epsilon{0.00001};
    double result;

    result = 0.28209;
    ASSERT_TRUE(fabs(atom.qlmFunction(0, 0, pbcX, pbcY, pbcZ, atomsInVerletList, atoms) - result) < epsilon);

    // more tests can be added
}

TEST(testAtom, evaluateSymmetryFunctions1)
{
    Atom atom(1, 0.84986, 0.84986, 0.84986);
    double epsilon{0.001};
    double result;
    atom.calculateDescriptors(pbcX, pbcY, pbcZ, atomsInVerletList, atoms);

    result = 7.46794;
    ASSERT_TRUE(fabs(atom.getDescriptors().at(0) - result) < epsilon);

    // more tests can be added
}

TEST(testAtom, evaluateSymmetryFunctions2)
{
    Atom atom(1, 0.84986, 0.84986, 0.84986);
    double epsilon{0.001};
    double result;
    atom.calculateDescriptors(pbcX, pbcY, pbcZ, atomsInVerletList, atoms);

    result = -9.86289;
    ASSERT_TRUE(fabs(atom.getDescriptors().at(8) - result) < epsilon);

    // more tests can be added
}
