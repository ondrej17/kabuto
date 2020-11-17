project(descriptors)
cmake_minimum_required(VERSION 3.16)
set(CMAKE_CXX_STANDARD 14)
find_package(Threads)

find_program(PYTHON "python")

if (PYTHON)
    set(SETUP_PY    "${CMAKE_CURRENT_BINARY_DIR}/setup.py")
    set(OUTPUT      "${CMAKE_CURRENT_BINARY_DIR}/build/timestamp")

    add_custom_command(OUTPUT ${OUTPUT}
                       COMMAND ${PYTHON} ${SETUP_PY} build
                       COMMAND ${CMAKE_COMMAND} -E touch ${OUTPUT})

    add_custom_target(target ALL DEPENDS ${OUTPUT})

    install(CODE "execute_process(COMMAND ${PYTHON} ${SETUP_PY} install)")
endif()

set(SOURCE_FILES
        src/descriptors_atom.cpp
        src/descriptors_box.cpp
        src/descriptors_descriptors.cpp
        #src/descriptors_module.cpp
        src/descriptors_timestep.cpp
        #src/descriptors_utility.cpp
        src/descriptors_verlet_list.cpp
)

include_directories("/usr/include/python3.8")

add_executable(test_atom tests/test_atom.cpp ${SOURCE_FILES})
add_executable(test_box tests/test_box.cpp ${SOURCE_FILES})
add_executable(test_boost tests/test_boost.cpp ${SOURCE_FILES})
# TODO: add more tests
