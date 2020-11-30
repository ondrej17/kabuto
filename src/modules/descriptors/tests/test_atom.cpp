/**
 * Tests for Atom class
 * 
 * Copyright 2005, Google Inc.
 * All rights reserved.
 */


#include <iostream>
#include <gtest/gtest.h>

using namespace std;

#include "../src/descriptors_atom.h"

using namespace ::testing;

TEST(testAtom, id)
{
    Atom test_atom(42, 0.9, 23.4, 5.6);
    ASSERT_EQ(42, test_atom.getId());
}

