#!/bin/bash
echo "Running tests for \"descriptors\" library"

bin/test_atom --log_level=all
bin/test_descriptors --log_level=all

echo "Done!"