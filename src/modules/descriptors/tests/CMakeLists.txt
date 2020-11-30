cmake_minimum_required(VERSION 3.6.2)
project(descriptors)

set(CMAKE_CXX_STANDARD 14)

add_subdirectory(googletest) # add googletest subdirectory

include_directories(googletest/include) # this is so we can #include <gtest/gtest.h>

set(SOURCE_FILES
        ../src/descriptors_atom.cpp
        #../src/descriptors_box.cpp
        ../src/descriptors_descriptors.cpp
        #../src/descriptors_module.cpp
        #../src/descriptors_timestep.cpp
        #../src/descriptors_utility.cpp
        #../src/descriptors_verlet_list.cpp
        
        test.cpp
        test_atom.cpp
        #test_box.cpp
        test_descriptors.cpp
        #test_timestep.cpp
        #test_verlet_list.cpp
)

add_executable(descriptors ${SOURCE_FILES})
target_link_libraries(descriptors PRIVATE gtest) # link google test to this executable

