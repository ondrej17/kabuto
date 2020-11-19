project(descriptors)

cmake_minimum_required(VERSION 3.16)
set(CMAKE_CXX_STANDARD 14)

find_program(PYTHON "python")

# compile C++ library for Python
if (PYTHON)
    set(SETUP_PY    "${CMAKE_CURRENT_BINARY_DIR}/setup.py")
    set(OUTPUT      "${CMAKE_CURRENT_BINARY_DIR}/build/timestamp")

    add_custom_command(OUTPUT ${OUTPUT}
                       COMMAND ${PYTHON} ${SETUP_PY} install
                       COMMAND ${CMAKE_COMMAND} -E touch ${OUTPUT})
    # if installing does not work on Maxwell, see: https://docs.python.org/3.8/install/
    # instalation copies the library to system place, e.g. /usr/lib/...

    add_custom_target(target ALL DEPENDS ${OUTPUT})

    install(CODE "execute_process(COMMAND ${PYTHON} ${SETUP_PY} install)")
endif()

# source files for testing
set(SOURCE_FILES

        # files for classes
        src/descriptors_atom.cpp
        src/descriptors_box.cpp
        src/descriptors_descriptors.cpp
        src/descriptors_timestep.cpp
        src/descriptors_verlet_list.cpp

        # files that needs Python.h
        #src/descriptors_module.cpp
        #src/descriptors_utility.cpp
)

# include Python.h
#include_directories("/usr/include/python3.8")

# test executables for each part of descriptors module
add_executable( test_atom            tests/test_atom.cpp            ${SOURCE_FILES})
add_executable( test_box             tests/test_box.cpp             ${SOURCE_FILES})
add_executable( test_descriptors     tests/test_descriptors.cpp     ${SOURCE_FILES})
add_executable( test_timestep        tests/test_timestep.cpp        ${SOURCE_FILES})
add_executable( test_verlet_list     tests/test_verlet_list.cpp     ${SOURCE_FILES})
add_executable( test_boost           tests/test_boost.cpp           ${SOURCE_FILES})
    # TODO: add more tests
