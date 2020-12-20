cmake_minimum_required(VERSION 3.6.2)
project(descriptors)

set(CMAKE_CXX_STANDARD 14)

find_package(Threads)

set(GTEST_FILES
        GoogleTest/gtest-death-test.cc
        GoogleTest/gtest-filepath.cc
        GoogleTest/gtest-port.cc
        GoogleTest/gtest-printers.cc
        GoogleTest/gtest-test-part.cc
        GoogleTest/gtest-typed-test.cc
        GoogleTest/gtest.cc
        GoogleTest/gtest_main.cc
)

set(SOURCE_FILES
        ../src/descriptors_atom.cpp
        #../src/descriptors_box.cpp
        #../src/descriptors_descriptors.cpp
        #../src/descriptors_module.cpp
        #../src/descriptors_timestep.cpp
        #../src/descriptors_utility.cpp
        ../src/descriptors_verlet_list.cpp
) 
set(TEST_FILES
        test_atom.cpp
        #test_box.cpp
        #test_descriptors.cpp
        #test_timestep.cpp
        test_verlet_list.cpp
)

include_directories(GoogleTest)
add_executable(descriptors ${SOURCE_FILES} ${TEST_FILES} ${GTEST_FILES})
target_link_libraries(descriptors ${CMAKE_THREAD_LIBS_INIT})
