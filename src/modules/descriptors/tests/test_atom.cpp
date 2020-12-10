/**
 * Tests for Atom class
 * 
 * Copyright 2005, Google Inc.
 * All rights reserved.
 */

#include <gtest/gtest.h>

#include "../src/descriptors_atom.h"

using namespace ::testing;

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

TEST(testAtom, setGetDescriptors)
{
    Atom test_atom(42, 0.9, 23.4, 5.6);
    std::vector<double> descriptors{1.2, 2.3, 3.5, 4.0, 5.9};

    test_atom.setDescriptors(descriptors);

    ASSERT_EQ(1.2, test_atom.getDescriptors()[0]);
    ASSERT_EQ(2.3, test_atom.getDescriptors()[1]);
    ASSERT_EQ(3.5, test_atom.getDescriptors()[2]);
    ASSERT_EQ(4.0, test_atom.getDescriptors()[3]);
    ASSERT_EQ(5.9, test_atom.getDescriptors()[4]);
}
