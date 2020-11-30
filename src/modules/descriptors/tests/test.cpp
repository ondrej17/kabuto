/**
 * Main test file 
 * 
 * Copyright 2005, Google Inc.
 * All rights reserved.
 */


#include <iostream>
#include <gtest/gtest.h>

using namespace std;
using namespace ::testing;

int main(int argc, char *argv[])
{
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}