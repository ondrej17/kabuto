/**
 * Tests for VerletList class
 * 
 * Copyright 2005, Google Inc.
 * All rights reserved.
 */

#include "gtest/gtest.h"

#include "../src/descriptors_verlet_list.h"

using namespace ::testing;

TEST(testVerletlist, id)
{
    std::vector<int> atomsId{1, 2, 3, 4, 5};
    VerletList test_verlet_list(42, atomsId);

    ASSERT_EQ(42, test_verlet_list.getId());
}

TEST(testVerletlist, numOfAtoms)
{
    std::vector<int> atomsId{1, 2, 3, 4, 5};
    VerletList test_verlet_list(42, atomsId);

    ASSERT_EQ(5, test_verlet_list.getNumOfAtoms());
}

TEST(testVerletlist, getAtomIds)
{
    std::vector<int> atomsId{1, 2, 3, 4, 5};
    VerletList test_verlet_list(42, atomsId);

    ASSERT_EQ(1, test_verlet_list.getAtomIds()[0]);
    ASSERT_EQ(2, test_verlet_list.getAtomIds()[1]);
    ASSERT_EQ(3, test_verlet_list.getAtomIds()[2]);
    ASSERT_EQ(4, test_verlet_list.getAtomIds()[3]);
    ASSERT_EQ(5, test_verlet_list.getAtomIds()[4]);
}