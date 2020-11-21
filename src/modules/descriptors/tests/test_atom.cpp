#define BOOST_TEST_MODULE test_atom

#include "../src/descriptors_atom.h"
#include <boost/test/unit_test.hpp>

BOOST_AUTO_TEST_CASE( testAtom1 )
{
    Atom test_atom(42, 0.9, 23.4, 5.6);

    BOOST_CHECK( test_atom.getId() == 42);
}