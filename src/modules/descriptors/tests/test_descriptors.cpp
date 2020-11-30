/**
 * Tests for Descriptors class
 * 
 * Copyright 2005, Google Inc.
 * All rights reserved.
 */


#include <iostream>
#include <gtest/gtest.h>

#include "../src/descriptors_descriptors.h"

using namespace ::testing;

int id{1};
double pbcX{6.3}, pbcY{6.3}, pbcZ{6.3};
std::vector<int> atomsInVerletList{2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16};
std::map<int, Atom> atoms = {
    // atoms in pure BCC structure (2x2x2 = 16 atoms)
    //      id      x[A]        y[A]        z[AM]
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

// global descriptors object
Descriptors descriptors(id, pbcX, pbcY, pbcZ, atomsInVerletList, atoms);

TEST(test_descriptors, testCutoffFunction)
{
    double epsilon{0.0001};
    ASSERT_TRUE(fabs(descriptors.fcFunction(14.0, 10.0, 12.0) - 0.0) < epsilon);
    ASSERT_TRUE(fabs(descriptors.fcFunction(11.0, 10.0, 12.0) - 0.5) < epsilon);
    ASSERT_TRUE(fabs(descriptors.fcFunction(11.5, 10.0, 12.0) - 0.1464) < epsilon);
    ASSERT_TRUE(fabs(descriptors.fcFunction(2.0, 10.0, 12.0) - 1.0) < epsilon);
    // what if one or more of the parameter(s) is/are negative?
    // what if rMin > rMax ?
}

TEST(test_descriptors, testSphericalCoordinates)
{
    double epsilon{0.00001};

    ASSERT_TRUE(fabs(descriptors.getSphericalR(0.0, 0.0, 0.0) - 0.0) < epsilon);
    // ASSERT_TRUE(fabs(descriptors.getSphericalPhi(0.0, 0.0, 0.0) - ???) < epsilon);
    // ASSERT_TRUE(fabs(descriptors.getSphericalTheta(0.0, 0.0, 0.0) - ???) < epsilon);

    ASSERT_TRUE(fabs(descriptors.getSphericalR(1.0, 1.0, 1.0) - sqrt(3.0)) < epsilon);
    ASSERT_TRUE(fabs(descriptors.getSphericalPhi(1.0, 1.0, 1.0) - M_PI_4) < epsilon);
    ASSERT_TRUE(fabs(descriptors.getSphericalTheta(1.0, 1.0, 1.0) - 0.955317) < epsilon);

    ASSERT_TRUE(fabs(descriptors.getSphericalR(-1.0, 1.0, 1.0) - sqrt(3.0)) < epsilon);
    ASSERT_TRUE(fabs(descriptors.getSphericalPhi(-1.0, 1.0, 1.0) - (M_PI - M_PI_4)) < epsilon);
    ASSERT_TRUE(fabs(descriptors.getSphericalTheta(-1.0, 1.0, 1.0) - 0.955317) < epsilon);

    ASSERT_TRUE(fabs(descriptors.getSphericalR(1.0, -1.0, 1.0) - sqrt(3.0)) < epsilon);
    ASSERT_TRUE(fabs(descriptors.getSphericalPhi(1.0, -1.0, 1.0) - (-M_PI_4)) < epsilon);
    ASSERT_TRUE(fabs(descriptors.getSphericalTheta(1.0, -1.0, 1.0) - 0.955317) < epsilon);

    ASSERT_TRUE(fabs(descriptors.getSphericalR(1.0, 1.0, -1.0) - sqrt(3.0)) < epsilon);
    ASSERT_TRUE(fabs(descriptors.getSphericalPhi(1.0, 1.0, -1.0) - M_PI_4) < epsilon);
    ASSERT_TRUE(fabs(descriptors.getSphericalTheta(1.0, 1.0, -1.0) - 2.186276) < epsilon);

    // more tests can be added
}

TEST(test_descriptors, testYlmFunction)
{
    double epsilon{0.00001};
    double result;

    // int m, int l, double dx, double dy, double dz
    result = 0.5 * sqrt(1 / M_PI);
    ASSERT_TRUE(fabs(descriptors.ylmFunction(0, 0, 1.0, 2.0, 3.0) - result) < epsilon);

    result = sqrt(3 / (4 * M_PI)) * (3.0 / sqrt(14.0));
    ASSERT_TRUE(fabs(descriptors.ylmFunction(0, 1, 1.0, 2.0, 3.0) - result) < epsilon);

    result = sqrt(3 / (4 * M_PI)) * (1.0 / sqrt(14.0));
    ASSERT_TRUE(fabs(descriptors.ylmFunction(1, 1, 1.0, 2.0, 3.0) - result) < epsilon);

    result = sqrt(3 / (4 * M_PI)) * (2.0 / sqrt(14.0));
    ASSERT_TRUE(fabs(descriptors.ylmFunction(-1, 1, 1.0, 2.0, 3.0) - result) < epsilon);

    result = 0.5 * sqrt(15 / M_PI) * (3.0 / 14.0);
    ASSERT_TRUE(fabs(descriptors.ylmFunction(1, 2, 1.0, 2.0, 3.0) - result) < epsilon);

    // more tests can be added
}

TEST(test_descriptors, testQlmFunction)
{
    double epsilon{0.00001};
    double result;

    result = 0.28209;
    ASSERT_TRUE(fabs(descriptors.qlmFunction(0, 0) - result) < epsilon);

    // more tests can be added
}

TEST(test_descriptors, testG2Function)
{
    double epsilon{0.001};
    double result;
    double eta{20.0};
    double rs{2.8};

    result = 7.46794;
    ASSERT_TRUE(fabs(descriptors.symmetryFunctionG2(eta, rs) - result) < epsilon);

    // more tests can be added
}

TEST(test_descriptors, testG3Function)
{
    double epsilon{0.001};
    double result;
    double kappa{3.5};

    result = -9.86289;
    ASSERT_TRUE(fabs(descriptors.symmetryFunctionG3(kappa) - result) < epsilon);

    // more tests can be added
}
