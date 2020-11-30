# Notes

## building googletest
cd tests
git clone https://github.com/google/googletest.git
cd googletests
mkdir build 
cd build
cmake -Dgtest_build_samples=ON -DCMAKE_BUILD_TYPE=Debug ..
make -j4

## building tests
cd tests 
mkdir build
cd build
cmake ..
make 
./descriptors 

## installing descriptors library
(sudo) ./install.sh