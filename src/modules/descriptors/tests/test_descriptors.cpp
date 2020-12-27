/**
 * Tests for Descriptors class
 * 
 * Copyright 2005, Google Inc.
 * All rights reserved.
 */

#include "gtest/gtest.h"

#include "../src/descriptors_descriptors.h"

using namespace ::testing;

TEST(testDescriptors, testCutoffFunction1)
{
    double epsilon{0.0001};
    double result;

    result = 0.0;
    ASSERT_TRUE(fabs(descriptors.fcFunction(14.0, 10.0, 12.0) - result) < epsilon);
    // what if one or more of the parameter(s) is/are negative?
    // what if rMin > rMax ?
}

TEST(testDescriptors, testCutoffFunction2)
{
    double epsilon{0.0001};
    double result;

    result = 0.5;
    ASSERT_TRUE(fabs(descriptors.fcFunction(11.0, 10.0, 12.0) - result) < epsilon);
    // what if one or more of the parameter(s) is/are negative?
    // what if rMin > rMax ?
}

TEST(testDescriptors, testCutoffFunction3)
{
    double epsilon{0.0001};
    double result;

    result = 0.1464;
    ASSERT_TRUE(fabs(descriptors.fcFunction(11.5, 10.0, 12.0) - result) < epsilon);
    // what if one or more of the parameter(s) is/are negative?
    // what if rMin > rMax ?
}

TEST(testDescriptors, testCutoffFunction4)
{
    double epsilon{0.0001};
    double result;

    result = 1.0;
    ASSERT_TRUE(fabs(descriptors.fcFunction(2.0, 10.0, 12.0) - result) < epsilon);
    // what if one or more of the parameter(s) is/are negative?
    // what if rMin > rMax ?
}

TEST(testDescriptors, testSphericalCoordinatesR)
{
    double epsilon{0.00001};
    double result;

    result = 0.0;
    ASSERT_TRUE(fabs(descriptors.getSphericalR(0.0, 0.0, 0.0) - result) < epsilon);

    result = sqrt(3.0);
    ASSERT_TRUE(fabs(descriptors.getSphericalR(1.0, 1.0, 1.0) - result) < epsilon);

    result = sqrt(3.0);
    ASSERT_TRUE(fabs(descriptors.getSphericalR(-1.0, 1.0, 1.0) - result) < epsilon);

    result = sqrt(3.0);
    ASSERT_TRUE(fabs(descriptors.getSphericalR(1.0, -1.0, 1.0) - result) < epsilon);

    result = sqrt(3.0);
    ASSERT_TRUE(fabs(descriptors.getSphericalR(1.0, 1.0, -1.0) - result) < epsilon);

    // more tests can be added
}

TEST(testDescriptors, testSphericalCoordinatesPhi)
{
    double epsilon{0.00001};
    double result;

    // result = ???;
    // ASSERT_TRUE(fabs(descriptors.getSphericalPhi(0.0, 0.0, 0.0) - ???) < epsilon);

    result = M_PI_4;
    ASSERT_TRUE(fabs(descriptors.getSphericalPhi(1.0, 1.0, 1.0) - result) < epsilon);

    result = M_PI - M_PI_4;
    ASSERT_TRUE(fabs(descriptors.getSphericalPhi(-1.0, 1.0, 1.0) - result) < epsilon);

    result = -M_PI_4;
    ASSERT_TRUE(fabs(descriptors.getSphericalPhi(1.0, -1.0, 1.0) - result) < epsilon);

    result = M_PI_4;
    ASSERT_TRUE(fabs(descriptors.getSphericalPhi(1.0, 1.0, -1.0) - result) < epsilon);

    // more tests can be added
}

TEST(testDescriptors, testSphericalCoordinatesTheta)
{
    double epsilon{0.00001};
    double result;

    // result = ???;
    // ASSERT_TRUE(fabs(descriptors.getSphericalTheta(0.0, 0.0, 0.0) - ???) < epsilon);

    result = 0.955317;
    ASSERT_TRUE(fabs(descriptors.getSphericalTheta(1.0, 1.0, 1.0) - result) < epsilon);

    result = 0.955317;
    ASSERT_TRUE(fabs(descriptors.getSphericalTheta(-1.0, 1.0, 1.0) - result) < epsilon);

    result = 0.955317;
    ASSERT_TRUE(fabs(descriptors.getSphericalTheta(1.0, -1.0, 1.0) - result) < epsilon);

    result = 2.186276;
    ASSERT_TRUE(fabs(descriptors.getSphericalTheta(1.0, 1.0, -1.0) - result) < epsilon);

    // more tests can be added
}

TEST(testDescriptors, testYlmFunction1)
{
    double epsilon{0.00001};
    double result;

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

TEST(testDescriptors, testQlmFunction1)
{
    double epsilon{0.00001};
    double result;

    result = 0.28209;
    ASSERT_TRUE(fabs(descriptors.qlmFunction(0, 0) - result) < epsilon);

    // more tests can be added
}

TEST(testDescriptors, testG2Function1)
{
    double epsilon{0.001};
    double result;
    double eta{20.0};
    double rs{2.8};

    result = 7.46794;
    ASSERT_TRUE(fabs(descriptors.symmetryFunctionG2(eta, rs) - result) < epsilon);

    // more tests can be added
}

TEST(testDescriptors, testG3Function1)
{
    double epsilon{0.001};
    double result;
    double kappa{3.5};

    result = -9.86289;
    ASSERT_TRUE(fabs(descriptors.symmetryFunctionG3(kappa) - result) < epsilon);

    // more tests can be added
}
