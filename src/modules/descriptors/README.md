# Descriptors for Kabuto project
---

 * C++ extension for Python used in the [Kabuto](https://github.com/ondrej17/kabuto) project. 
 * Project for Programovanie (3) subject at FMFI UK
---
## About

TBA ...

---
## Visualisation of object relationship

![object-relationship](src/common/images/helix-nebula.jpg)

---
## Project structure

 * `src`
   * `boost`
     * `...`
   * `common`
     * `images`
       * `helix-nebula.jpg`
   * `descriptors_atom.cpp`
   * `descriptors_atom.h`
   * `...`
 * `tests`
   * `googletest`
     * `...`
   * `CMakeLists.txt`
   * `test_atom.cpp`
   * `...`
   * `test.cpp`
 * `install.sh`
 * `setup.py`
 * `README.md`

---
## Building and installing

### Building `boost` library

No building is needed, all header files are already included (`src/boost`).

### Installing `descriptors` library

    (sudo) ./install.sh

### Building `googletest`

No building is needed, all header files are already included (`tests/googletest`).

In case you wanted to build it by yourself, use this:

    cd tests
    git clone https://github.com/google/googletest.git
    cd googletests
    mkdir build 
    cd build
    cmake -Dgtest_build_samples=ON -DCMAKE_BUILD_TYPE=Debug ..
    make -j4

### Building tests
    cd tests 
    mkdir build
    cd build
    cmake ..
    make 

---
## Usage

Run tests using this:

    ./descriptors

Use `descriptors` extension in your Python project using this:

    import descriptors
    ...
    descriptors.compute(pbcX, pbcY, pbcZ, timesteps)